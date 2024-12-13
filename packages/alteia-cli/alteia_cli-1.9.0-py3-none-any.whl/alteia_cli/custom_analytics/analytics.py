# Hack to circumvent ImportError starting from Python 3.10
# PyInquirer is not maintained anymore and uses a not up-to-date version
# of prompt-toolkit.
import collections.abc
import pkgutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import semver
import typer
import yaml
from alteia.core.errors import ResponseError
from alteia.core.resources.resource import Resource, ResourcesWithTotal
from alteia.core.utils.typing import ResourceId, SomeResourceIds
from alteia.sdk import SDK
from tabulate import tabulate

from alteia_cli import AppDesc, utils
from alteia_cli.sdk import alteia_sdk
from alteia_cli.utils import (blue_bold, green_bold, print_error, print_ok,
                              print_warn)

setattr(collections, 'Iterable', collections.abc.Iterable)
setattr(collections, 'Mapping', collections.abc.Mapping)
from PyInquirer import Separator, Token, prompt, style_from_dict  # noqa: E402

app = typer.Typer()
app_desc = AppDesc(app, name='analytics', help='Interact with analytics.')

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


class Preprocessing:
    def __init__(self, operation: str, *, parameters: Optional[Dict] = None):
        self.operation = operation
        self.parameters = parameters or {}

    def to_dict(self):
        return self.__dict__


class Input:
    def __init__(self, name: str, *, display_name: str, description: str,
                 required: bool, source: Optional[Dict] = None, scheme: Optional[Dict] = None,
                 preprocessings: Optional[List[Preprocessing]] = None):
        self.name = name
        self.display_name = display_name
        self.required = required
        self.description = description
        if source:
            if source.get('scheme'):
                utils.check_json_schema(source['scheme'])
        self.source = source
        if scheme:
            utils.check_json_schema(scheme)
        self.scheme = scheme
        self.preprocessings = preprocessings or []

    def to_dict(self):
        return self.__dict__

    def to_dict_without_preprocessings(self):
        """ Used to match the analytic creation API """
        d = self.__dict__.copy()
        d.pop('preprocessings', None)
        return d

    def get_serialized_preprocessings_with_input_name(self):
        """ Used to match the analytic creation API """
        preprocessings = []
        for p in self.preprocessings:
            preprocessing_dict = p.to_dict()
            preprocessing_dict['input'] = self.name
            preprocessings.append(preprocessing_dict)
        return preprocessings

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        kind = str(yaml_desc.get('kind'))
        scheme: Dict[str, Any]
        source: Dict[str, Any]

        if kind == 'dataset':
            scheme = {
                'type': 'string',
                'pattern': '^[0-9a-f]{24}$'
            }
        elif kind == 'dataset-array':
            scheme = {
                'type': 'array',
                'items': {
                    'type': 'string',
                    'pattern': '^[0-9a-f]{24}$'
                }
            }
        else:
            raise KeyError('kind {!r} not supported'.format(kind))

        source = {
            'service': 'data-manager',
            'resource': 'dataset'
        }

        dataset_schema = yaml_desc.get('schema')
        if dataset_schema:
            source.update({
                'scheme': {
                    'type': 'object',
                    'properties': {},
                    'required': []
                }
            })

            if dataset_schema.get('mission'):
                source['fromMissions'] = dataset_schema.pop('mission')

            for prop_name, possible_values in dataset_schema.items():
                if prop_name == 'categories':
                    if not possible_values:
                        # Ignore categories if empty
                        continue

                    source['scheme']['properties'][prop_name] = {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'contains': {'enum': possible_values}
                    }
                elif prop_name == 'type':
                    source['scheme']['properties'][prop_name] = {
                        'const': possible_values
                    }
                elif prop_name == 'source':
                    source['scheme']['properties']['source'] = {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'const': possible_values
                            }
                        }
                    }
                else:
                    raise KeyError('{!r} not supported'.format(prop_name))
                source['scheme']['required'].append(prop_name)

            preprocessings = None
            if yaml_desc.get('preprocessings'):
                input_preprocessings = yaml_desc.get('preprocessings', [])
                preprocessings = [Preprocessing(operation=p.get('operation'),
                                                parameters=p.get('parameters'))
                                  for p in input_preprocessings]

        return cls(
            name=str(yaml_desc.get('name')),
            display_name=str(yaml_desc.get('display-name')),
            required=bool(yaml_desc.get('required')),
            description=str(yaml_desc.get('description')),
            scheme=scheme,
            source=source,
            preprocessings=preprocessings
        )


class Deliverable(Input):
    pass


class Parameter:
    def __init__(self, name: str, *, display_name: str, description: str,
                 required: bool, scheme: Dict, default_value: Optional[Any]):
        self.name = name
        self.display_name = display_name
        self.required = required
        self.description = description
        if scheme:
            utils.check_json_schema(scheme)
        self.scheme = scheme
        self.default_value = default_value

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        scheme = yaml_desc.get('schema')
        if scheme:
            default_value = scheme.get('default')
        return cls(
            name=str(yaml_desc.get('name')),
            display_name=str(yaml_desc.get('display-name')),
            required=bool(yaml_desc.get('required')),
            description=str(yaml_desc.get('description')),
            scheme=scheme,
            default_value=default_value
        )


class Analytic:
    def __init__(self, name: str, *, display_name: str, description: str,
                 docker_image: str,
                 docker_credentials_name: str,
                 version: Optional[str] = None,
                 instance_type: Optional[str] = None,
                 volume_size: Optional[int] = None,
                 tags: Optional[List[str]] = None,
                 groups: Optional[List[str]] = None,
                 inputs: Optional[List[Input]] = None,
                 parameters: Optional[List[Parameter]] = None,
                 deliverables: Optional[List[Deliverable]] = None):
        self.name = name
        self.display_name = display_name
        self.description = description
        self.docker_image = docker_image
        self.docker_credentials_name = docker_credentials_name
        self.version = version
        self.instance_type = instance_type
        self.volume_size = volume_size
        self.tags = tags
        self.groups = groups
        self.inputs = inputs
        self.parameters = parameters
        self.deliverables = deliverables

    @classmethod
    def from_yaml(cls, yaml_desc: Dict):
        creation_params: Dict[str, Any]
        version = yaml_desc.get('version')
        creation_params = {
            'name': str(yaml_desc.get('name')),
            'display_name': str(yaml_desc.get('display-name')),
            'description': str(yaml_desc.get('description')),
            'docker_image': str(yaml_desc.get('docker-image')),
            'docker_credentials_name': str(yaml_desc.get('docker-credentials-name')),
            'version': str(version) if version else None,
            'volume_size': yaml_desc.get('volume-size'),
            'instance_type': yaml_desc.get('instance-type'),
            'tags': yaml_desc.get('tags'),
            'groups': yaml_desc.get('groups'),
        }
        yaml_inputs = yaml_desc.get('inputs')
        if isinstance(yaml_inputs, list):
            creation_params['inputs'] = [Input.from_yaml(i) for i in yaml_inputs]
        yaml_deliv = yaml_desc.get('deliverables')
        if isinstance(yaml_deliv, list):
            creation_params['deliverables'] = [
                Deliverable.from_yaml(i) for i in yaml_deliv]
        yaml_params = yaml_desc.get('parameters')
        if isinstance(yaml_params, list):
            creation_params['parameters'] = [
                Parameter.from_yaml(i) for i in yaml_params]
        return cls(**creation_params)


def _get_analytic_schema(schema_path: str) -> Dict:
    file_content = pkgutil.get_data(
        __name__,
        schema_path
    )
    if file_content:
        return yaml.load(file_content, Loader=yaml.Loader)
    else:
        raise FileNotFoundError


ANALYTIC_DESC_SCHEMA = _get_analytic_schema('share/analytic_schema.yaml')


@app.command(name='list')
def list_analytics(
    limit: int = typer.Option(
        100, '--limit', '-n', min=1,
        help='Max number of analytics returned.'),
    display_all: bool = typer.Option(
        False, '--all', case_sensitive=False,
        help='If set, display all kinds of analytics '
             '(otherwise only custom analytics are displayed).'
    ),
):
    """
        List the analytics.
    """
    sdk = alteia_sdk()
    with utils.spinner():
        search_filter = {'is_backoffice': {'$ne': True}}
        if not display_all:
            search_filter['external'] = {'$eq': True}

        found_analytics = cast(
            ResourcesWithTotal,
            sdk.analytics.search(
                filter=search_filter,
                return_total=True,
                limit=limit,
                sort={'display_name': 1}
            )
        )
        results = found_analytics.results

    if len(results) > 0:
        table = {
            'Analytic display name': [
                typer.style(r.display_name, fg=typer.colors.GREEN, bold=True)
                for r in results
            ],
            'Name': [r.name for r in results],
            'Version': [r.version if hasattr(r, 'version') else '' for r in results],
            'Identifier': [r.id for r in results]
        }
        typer.secho(tabulate(
            table,
            headers='keys',
            tablefmt='pretty',
            colalign=('left', 'left')
        ))

        print()
        print('{}/{} analytics displayed'.format(
            len(results),
            found_analytics.total
        ))

    else:
        print('No analytic found.')


@app.command()
def create(
    description: Path = typer.Option(
        ...,   # '...' in typer.Option() makes the option required
        exists=True,
        readable=True,
        help='Path of the Analytic description (YAML file).'),
    company: str = typer.Option(default=None, help='Company identifier.'),
):
    """
        Create a new analytic.
    """
    analytic_desc = parse_analytic_yaml(description)
    analytic = Analytic.from_yaml(analytic_desc)
    typer.secho('✓ Analytic description is valid', fg=typer.colors.GREEN)

    sdk = alteia_sdk()

    if not company:
        company_shortname = analytic.name.split('/')[0]
        found = cast(
            ResourcesWithTotal,
            sdk.companies.search(
                filter={'short_name': {'$eq': company_shortname}},
                limit=1,
                return_total=True
            )
        )
        if found.total != 1:
            typer.secho(
                f'✖ Impossible to find company with shortname {company_shortname}:',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)

        company = found.results[0]._id

    if not semver.VersionInfo.isvalid(analytic.version):
        typer.secho(
            '✖ The version {} does not respect the SemVer format'.format(
                analytic.version
            ),
            fg=typer.colors.RED
        )
        raise typer.Exit(2)

    check_credentials(sdk, company, analytic.docker_credentials_name)

    found_analytics = find_analytics(sdk, analytic.name, analytic.version,
                                     raise_if_not_found=False)
    if len(found_analytics) != 0:
        typer.secho(
            '⚠ {} {} already exists on {}'.format(
                analytic.name, analytic.version, sdk._connection._base_url
            ),
            fg=typer.colors.YELLOW
        )
        replace_confirm_msg = typer.style(
            'Would you like to replace it?', fg=typer.colors.YELLOW)
        typer.confirm(replace_confirm_msg, abort=True)
        sdk.analytics.delete(analytic=found_analytics[0].id)
    else:
        typer.secho(
            '✓ No analytic with the name {!r} and version {!r} on {!r}'.format(
                analytic.name, analytic.version, sdk._connection._base_url
            ),
            fg=typer.colors.GREEN
        )

    analytic_creation_params = {
        'name': analytic.name,
        'version': analytic.version,
        'display_name': analytic.display_name,
        'description': analytic.description,
        'docker_image': analytic.docker_image,
        'docker_credentials_name': analytic.docker_credentials_name,
    }

    inputs = None
    deliverables = None
    parameters = None
    preprocessings: Optional[List[Preprocessing]] = None

    if analytic.inputs:
        inputs = []
        preprocessings = []
        for i in analytic.inputs:
            inputs.append(i.to_dict_without_preprocessings())
            if i.preprocessings:
                preprocessings.extend(i.get_serialized_preprocessings_with_input_name())

        if not preprocessings:
            preprocessings = None

    if analytic.parameters:
        parameters = [p.to_dict() for p in analytic.parameters]
    if analytic.deliverables:
        deliverables = [d.to_dict_without_preprocessings()
                        for d in analytic.deliverables]

    for sdk_param, obj_val in (('instance_type', analytic.instance_type),
                               ('volume_size', analytic.volume_size),
                               ('inputs', inputs),
                               ('parameters', parameters),
                               ('deliverables', deliverables),
                               ('tags', analytic.tags),
                               ('groups', analytic.groups),
                               ('preprocessings', preprocessings)):
        if obj_val is not None:
            analytic_creation_params[sdk_param] = obj_val

    created_analytic = sdk.analytics.create(company=cast(ResourceId, company),
                                            **analytic_creation_params)
    typer.secho('✓ Analytic created successfully', fg=typer.colors.GREEN)
    return created_analytic


def parse_analytic_yaml(analytic_yaml_path: Path) -> Dict:
    with open(analytic_yaml_path) as f:
        analytic = yaml.load(f, Loader=yaml.Loader)

    # Specific message in case no version in the definition
    # as analytic versioning is a new feature
    if 'version' not in analytic:
        typer.secho(
            '⚠ From now on, you must specify an analytic version '
            f'in your description file "{analytic_yaml_path.name}".\n\n'
            'For instance, you can add under the "display-name: ..." line:\n'
            'version: 1.0.0\n\n'
            'Version must follow the SemVer syntax. See https://semver.org/.',
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(2)

    errors = utils.validate_against_schema(
        analytic,
        json_schema=ANALYTIC_DESC_SCHEMA
    )
    if errors:
        typer.secho(
            '✖ Cannot create the analytic with the supplied YAML file. '
            'Found error(s):',
            fg=typer.colors.RED
        )
        typer.secho(errors)
        raise typer.Exit(2)
    else:
        return analytic


def find_analytics(sdk, analytic_name: str, version_range: Optional[str] = None,
                   raise_if_not_found: bool = True):
    search_filter = {'name': {'$eq': analytic_name}}
    if version_range:
        search_filter['version'] = {'$satisfies': version_range}

    with utils.spinner():
        results = list(sdk.analytics.search_generator(
            filter=search_filter,
            fields={'exclude': [
                'algorithm',
                'inputs',
                'outputs',
                'deliverables']}))

    if raise_if_not_found and len(results) == 0:
        msg = '✖ Cannot find the analytic {!r} {!r}'\
            if version_range else '✖ Cannot find the analytic {!r}'
        typer.secho(msg.format(analytic_name, version_range),
                    fg=typer.colors.RED
                    )
        raise typer.Exit(2)

    return results


def check_credentials(sdk, company: str, credential_name: str, raise_if_not_found: bool = True):
    search_filter = {'name': {'$eq': credential_name}, 'company': {'$eq': company}}

    with utils.spinner():
        results = list(sdk.credentials.search(
            filter=search_filter))

    if raise_if_not_found and len(results) == 0:
        msg = '✖ Credentials {!r} not fount in company {!r}'
        typer.secho(msg.format(credential_name, company), fg=typer.colors.RED)
        raise typer.Exit(2)

    return results


def get_companies_hierarchy(sdk: SDK, permission_name: str):
    user = sdk.users.describe()
    company_ids = cast(SomeResourceIds,
                       get_companies_where_permission(sdk, permission_name))

    user_companies = [c.__dict__ for c in cast(List[Resource],
                                               sdk.companies.describe(company_ids))]
    # The user does not necessarily have the permission to describe
    # companies available for sharing. In this case, we can only show the id
    # of the company.
    root_company_id = get_root_company(sdk)
    for cid in company_ids:
        if not any(c['_id'] == cid for c in user_companies):
            if cid == root_company_id:
                company = {
                    '_id': cid,
                    'name': 'Root company'
                }
            else:
                company = {
                    '_id': cid,
                    'name': cid,
                    'root_company': root_company_id
                }
            user_companies.append(company)

    companies_by_id = {c['_id']: c for c in user_companies}
    hierarchised_companies = list()
    # Build a hierarchy of company (company object with property children)
    for c in user_companies:
        root_company = companies_by_id.get(c.get('root_company'))
        if root_company:
            children = root_company.get('children')
            if children is None:
                children = list()
                root_company['children'] = children
            children.append(c)
        else:
            hierarchised_companies.append(c)
    # Sort children by name
    for hierarchised_company in hierarchised_companies:
        if 'children' not in hierarchised_company:
            continue
        hierarchised_company['children'] = sorted(
            hierarchised_company['children'],
            key=lambda c: c['name'])

    return (user_companies, hierarchised_companies, user)


def get_companies_where_permission(sdk: SDK, permission_name) -> List[ResourceId]:
    def filter_have_scope_where_permission(have_scope):
        if have_scope is None:
            return
        for has_scope in have_scope:
            scope = has_scope.get('scope')
            if scope is None:
                continue
            service_perms = scope.get('analytics-service')
            if service_perms is None:
                continue
            for p in service_perms:
                if p == permission_name:
                    yield has_scope

    token = sdk._connection._token_manager.describe_token()
    user_in_token = token['user']
    companies = set()
    for has_scope in filter_have_scope_where_permission(
            user_in_token.get('permissions')):
        companies.update(has_scope['companies'])
    for has_scope in filter_have_scope_where_permission(
            user_in_token.get('companies')):
        companies.add(has_scope['id'])

    return list(companies)  # convert to list to be JSON serializable


def get_root_company(sdk: SDK, permission_name: Optional[str] = None) -> ResourceId:
    # Assuming a user can only belong to one domain
    user = sdk.users.describe()
    first_company_id = cast(ResourceId, user.companies[0]['id'])
    first_company = cast(Resource, sdk.companies.describe(first_company_id))
    root_company_id = getattr(first_company, 'root_company', None)
    if root_company_id is None:
        root_company_id = first_company._id

    # Ensure the user has the given permission
    # in the context of the root company
    if permission_name is not None:
        user_company_ids = get_companies_where_permission(sdk, permission_name)
        if root_company_id not in user_company_ids:
            typer.secho(
                '✖ No sufficient permissions to access the root company '
                'of your domain.',
                fg=typer.colors.RED
            )
            raise typer.Exit(2)

    return root_company_id


@app.command()
def unshare(
        analytic_name: str = typer.Argument(...),
        version: str = typer.Option(default=None,
                                    help='Range of versions in SemVer format. '
                                    'If not provided, '
                                    'all the versions will be unshared.'),
        company: str = typer.Option(
            default=None,
            help='Identifier of the company to unshare the analytic with.'),
        domain: bool = typer.Option(
            default=False,
            help='''To unshare the analytic with the root company of your domain.

This is equivalent to using the --company option providing
the id of the root company.
Note that if you specifically shared the analytic with a company
of your domain, the analytic will still be shared with that company.'''
        )):
    """ Unshare an analytic (DEPRECATED: use unexpose instead) """
    print_warn(
        'Deprecation Warning: '
        'Do not use this command `analytics unshare`. '
        'Use `analytics unexpose` command instead. '
    )
    sdk = alteia_sdk()
    analytics = find_analytics(sdk, analytic_name=analytic_name,
                               version_range=version)
    for analytic in analytics:
        if not analytic.external:
            typer.secho(
                '✖ Cannot unshare the non-custom analytic {!r} {!r}'
                .format(analytic_name, analytic.version),
                fg=typer.colors.RED
            )
            raise typer.Exit(2)

    permission_name = 'unshare-analytic-with-company:external'

    def company_selection(analytic_current_companies):
        def validate_answer(answer):
            if len(answer):
                return True
            return 'You must choose at least company.'

        companies, hierarchised_companies, _ = \
            get_companies_hierarchy(sdk, permission_name)
        questions = [
            {
                'type': 'checkbox',
                'message': 'Select companies to unshare analytics',
                'name': 'form',
                'choices': [
                    Separator('The analytic will be unshared with :')
                ],
                'validate': validate_answer
            }
        ]

        number_of_comp_unshared = 0

        def create_company_choice(comp, is_child, is_last_child):
            nonlocal number_of_comp_unshared
            name = comp['name']
            choice = {
                'name': f"└─ {name}" if is_last_child
                else f"├─ {name}" if is_child
                else name,
                'value': comp['_id']
            }
            no_versions_shared_with_company = True
            all_versions_owned_by_company = True
            for version in analytics:
                if comp['_id'] in getattr(version, 'companies', []):
                    no_versions_shared_with_company = False
                if comp['_id'] != version.company:
                    all_versions_owned_by_company = False
            if no_versions_shared_with_company or all_versions_owned_by_company:
                number_of_comp_unshared += 1
                choice['checked'] = True
                choice['disabled'] = 'owns the analytic'\
                    if all_versions_owned_by_company\
                    else 'already not shared'
            questions[0]['choices'].append(choice)

        for comp in hierarchised_companies:
            create_company_choice(comp, False, False)
            if 'children' in comp:
                children = comp['children']
                for i, child in enumerate(children):
                    create_company_choice(child, True, i == len(children)-1)

        if number_of_comp_unshared == len(companies):
            companies_ids = []
        else:
            form_answers = prompt(questions, style=style)
            # if user cancels, form_answers.get('form') will be None
            companies_ids = form_answers.get('form')
        return companies_ids

    if company:
        companies = [company]
    elif domain:
        companies = [get_root_company(sdk, permission_name)]
    else:
        companies = company_selection(analytics)
        if companies is None:
            # User cancelled
            return

    for analytic in analytics:
        companies_to_unshare_with = cast(
            List[ResourceId],
            [c for c in companies if c in getattr(analytic, 'companies', [])]
        )
        try:
            for company in companies_to_unshare_with:
                sdk.analytics.unshare_with_company(
                    analytic=analytic.id,
                    company=company)
        except ResponseError as e:
            typer.secho(
                '✖ Cannot unshare the analytic {!r} {!r}'
                .format(analytic_name, analytic.version),
                fg=typer.colors.RED
            )
            typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
            raise typer.Exit(2)

        if len(companies_to_unshare_with) > 0:
            typer.secho(
                '✓ Analytic {!r} {!r} unshared successfully'
                .format(analytic_name, analytic.version),
                fg=typer.colors.GREEN
            )
        else:
            typer.secho(
                'ℹ No companies to unshare the analytic {!r} {!r} with'.format(
                    analytic_name, analytic.version),
                fg=typer.colors.BLUE
            )


@app.command()
def share(
        analytic_name: str = typer.Argument(...),
        version: str = typer.Option(default=None,
                                    help='Range of versions in SemVer format. '
                                    'If not provided, '
                                    'all the versions will be shared.'),
        company: str = typer.Option(
            default=None,
            help='''Identifier of the company to share the analytic with.

When providing the identifier of the root company of your domain,
the analytic is shared with all the companies of the domain
(equivalent to using the --domain option)'''),
        domain: bool = typer.Option(
            default=False,
            help='''To share the analytic with the root company of your domain.

This has the effect to share the analytic with all the
companies of your domain and is equivalent to using the
--company option providing the id of the root company.'''
        )):
    """ Share an analytic (DEPRECATED: use expose instead) """
    print_warn(
        'Deprecation Warning: '
        'Do not use this command `analytics share`. '
        'Use `analytics expose` command instead. '
    )
    sdk = alteia_sdk()

    permission_name = 'share-analytic-with-company:external'

    def company_selection(analytics):
        def validate_answer(answer):
            if len(answer):
                return True
            return 'You must choose at least one company.'

        companies, hierarchised_companies, _ = \
            get_companies_hierarchy(sdk, permission_name)
        questions = [
            {
                'type': 'checkbox',
                'message': 'Select companies to share the analytic with',
                'name': 'form',
                'choices': [
                    Separator('The analytic will be shared with :')
                ],
                'validate': validate_answer
            }
        ]

        number_of_comp_shared = 0

        def create_company_choice(comp, is_child, is_last_child,
                                  all_versions_of_root_shared_with_company):
            nonlocal number_of_comp_shared
            name = comp['name']
            choice = {
                'name': f"└─ {name}" if is_last_child
                else f"├─ {name}" if is_child
                else f'{name}  (and all its attached companies)'
                if comp.get('children')
                else name,
                'value': comp['_id']
            }
            all_versions_shared_with_company = True
            if all_versions_of_root_shared_with_company is False:
                for version in analytics:
                    if comp['_id'] not in getattr(version, 'companies', []):
                        all_versions_shared_with_company = False
                        break
            if all_versions_shared_with_company:
                number_of_comp_shared += 1
                choice['checked'] = True
                choice['disabled'] = 'already shared'
            questions[0]['choices'].append(choice)
            return all_versions_shared_with_company

        for comp in hierarchised_companies:
            root_is_shared = create_company_choice(comp, False, False, False)
            if 'children' in comp:
                children = comp['children']
                for i, child in enumerate(children):
                    create_company_choice(child, True, i == len(children)-1,
                                          root_is_shared)
        if number_of_comp_shared == len(companies):
            companies_ids = []
        else:
            form_answers = prompt(questions, style=style)
            # if user cancels, form_answers.get('form') will be None
            companies_ids = form_answers.get('form')
        return companies_ids

    analytics = find_analytics(sdk, analytic_name=analytic_name,
                               version_range=version)
    for analytic in analytics:
        if not analytic.external:
            typer.secho(
                '✖ Cannot share the non-custom analytic {!r} {!r}'
                .format(analytic_name, analytic.version),
                fg=typer.colors.RED
            )
            raise typer.Exit(2)

    if company:
        companies = [company]
    elif domain:
        companies = [get_root_company(sdk, permission_name)]
    else:
        companies = company_selection(analytics)
        if companies is None:
            # User cancelled
            return

    for analytic in analytics:
        companies_to_share_with = cast(
            List[ResourceId],
            [c for c in companies if c not in getattr(analytic, 'companies', [])]
        )
        try:
            for company in companies_to_share_with:
                sdk.analytics.share_with_company(
                    analytic=analytic.id,
                    company=company)
        except ResponseError as e:
            typer.secho(
                '✖ Cannot share the analytic {!r} {!r}'
                .format(analytic_name, analytic.version),
                fg=typer.colors.RED
            )
            typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
            raise typer.Exit(2)

        if len(companies_to_share_with) > 0:
            typer.secho(
                '✓ Analytic {!r} {!r} shared successfully with {} companies'
                .format(analytic_name, analytic.version,
                        len(companies_to_share_with)),
                fg=typer.colors.GREEN
            )
        else:
            typer.secho(
                'ℹ Analytic {!r} {!r} is already shared'.format(
                    analytic_name, analytic.version),
                fg=typer.colors.BLUE
            )


@app.command()
def delete(analytic_name: str = typer.Argument(...),
           version: str = typer.Option(default=None,
                                       help='Version range of the analytic '
                                       'in SemVer format. If not provided, '
                                       'all the versions will be deleted.')):
    """
        Delete an analytic.
    """
    sdk = alteia_sdk()
    analytics = find_analytics(sdk, analytic_name=analytic_name,
                               version_range=version)

    if len([a for a in analytics if a.external]) != len(analytics):
        deletion_confirm_msg = typer.style(
            'Analytic {!r} is NOT a custom analytic. '
            'Are you sure you want to delete it anyway?'.format(analytic_name),
            fg=typer.colors.YELLOW)
        typer.confirm(deletion_confirm_msg, abort=True)
    for analytic in analytics:
        try:
            analytic_id = analytic.id
            sdk.analytics.delete(analytic=analytic_id)
        except ResponseError as e:
            typer.secho(
                '✖ Cannot delete the analytic {!r} {!r}'
                .format(analytic_name, analytic.version),
                fg=typer.colors.RED
            )
            typer.secho('details: {}'.format(str(e)), fg=typer.colors.RED)
            raise typer.Exit(2)

        typer.secho(
            '✓ Analytic {!r} {!r} deleted successfully'
            .format(analytic_name, analytic.version),
            fg=typer.colors.GREEN
        )


def get_domain_root_company_from_current_user(sdk: SDK) -> Tuple[str, ResourceId]:
    # Assuming a user can only belong to one domain
    user = sdk.users.describe()
    first_company_id = user.companies[0]['id']
    first_company = cast(Resource, sdk.companies.describe(first_company_id))
    root_company_id = getattr(first_company, 'root_company', None)
    if root_company_id is None:
        root_company_id = first_company.id

    # companies always have a domain, which is same as their root company
    domain_name = first_company.domain

    return domain_name, root_company_id


def get_root_companies_of_domains(
        sdk: SDK,
        domain_names: Optional[Union[List[str], str]] = None,
        raise_if_not_found: bool = True,
) -> List[Tuple[str, ResourceId]]:
    if domain_names is None:
        # no given domains, return the user one
        return [get_domain_root_company_from_current_user(sdk)]

    if isinstance(domain_names, str):
        # assume you give many domains separated by comma
        domain_names = domain_names.split(',')

    filters = {
        'domain': {'$in': domain_names},
        'root_company': {'$eq': None},
    }
    fields = {'include': ['_id', 'domain']}
    found_root_companies = cast(
        List[Resource],
        sdk.companies.search(filter=filters, fields=fields)
    )
    # it must have same number of domains than number of found root companies
    found_domains = [c.domain for c in found_root_companies]
    not_found_domains = list(set(domain_names).difference(set(found_domains)))

    if len(not_found_domains) > 0:
        if len(domain_names) == 1:
            # One wanted domain but no root company found ?
            # It can be a user who cannot search directly the root company
            # So, get the domain from user describe and compare to the wanted one
            user_domain_root_company = get_domain_root_company_from_current_user(sdk)
            if user_domain_root_company[0] == domain_names[0]:
                return [user_domain_root_company]

        if raise_if_not_found:
            msg = f'Bad domain(s) or no sufficient permissions to access the ' \
                  f'root company of: {", ".join(not_found_domains)}'
            print_error(msg, raise_exit=True)

    return [(c.domain, c.id) for c in found_root_companies]


@app.command()
def expose(
    analytic_name: str = typer.Argument(...),
    domain: str = typer.Option(
        default=None,
        help='To expose the analytic on the specified domains (comma separated values) '
             'if you have the right permissions on these domains.\n\n'
             'By default, without providing this option, the analytic will be exposed '
             'on your domain if you have the right permissions on it.',
    ),
):
    """Expose an analytic"""
    sdk = alteia_sdk()

    # check the analytic name, will raise error if not found
    find_analytics(sdk, analytic_name=analytic_name)

    # check domains and get root companies, will raise error if at least one not found
    domains_root_companies = get_root_companies_of_domains(sdk, domain_names=domain)

    # do expose to each domain one by one
    for domain_name, root_company_id in domains_root_companies:
        try:
            with utils.spinner():
                sdk.analytics.expose(analytic_name, root_companies=root_company_id)
            print_ok(f'Analytic "{analytic_name}" exposed successfully '
                     f'on "{domain_name}" domain')
        except ResponseError as e:
            print_error(f'Cannot expose the analytic "{analytic_name}" '
                        f'on "{domain_name}" domain: {e}')


@app.command()
def unexpose(
    analytic_name: str = typer.Argument(...),
    domain: str = typer.Option(
        default=None,
        help='To unexpose the analytic from the specified domains (comma separated '
             'values) if you have the right permissions on these domains.\n\n'
             'By default, without providing this option, the analytic will be '
             'unexposed from your domain if you have the right permissions on it.',
    ),
):
    """Unexpose an analytic"""
    sdk = alteia_sdk()

    # check the analytic name, will raise error if not found
    find_analytics(sdk, analytic_name=analytic_name)

    # check domains and get root companies, will raise error if at least one not found
    domains_root_companies = get_root_companies_of_domains(sdk, domain_names=domain)

    # do expose to each domain one by one
    for domain_name, root_company_id in domains_root_companies:
        try:
            with utils.spinner():
                sdk.analytics.unexpose(analytic_name, root_companies=root_company_id)
            print_ok(f'Analytic "{analytic_name}" unexposed successfully '
                     f'from "{domain_name}" domain')
        except ResponseError as e:
            print_error(f'Cannot unexpose the analytic "{analytic_name}" '
                        f'from "{domain_name}" domain: {e}')


@app.command(name='list-exposed')
def list_exposed(
    display_all: bool = typer.Option(
        False, '--all', case_sensitive=False,
        help='If set, display all kinds of analytics '
             '(otherwise only custom analytics are displayed).'
    ),
    domain: str = typer.Option(
        default=None,
        help='If set, filters exposed analytics on the specified domains (comma '
             'separated values) if you have the right permissions on these domains.'
             '\n\nBy default, without providing this option, '
             'it filters on your domain.',
    ),
):
    """List exposed analytics"""
    sdk = alteia_sdk()

    domains_root_companies = get_root_companies_of_domains(sdk, domain_names=domain)

    search_filter = {'is_backoffice': {'$ne': True}}
    if not display_all:
        search_filter['external'] = {'$eq': True}

    found_analytics: Dict[str, dict] = {}
    try:
        for domain, root_company in domains_root_companies:
            # do not make one request with all root companies, because we
            # do not want Intersection results
            with utils.spinner():
                results = sdk.analytics.search_generator(
                    filter=search_filter,
                    exposed_on_root_companies=[root_company],
                    fields={'include': ['name', 'display_name', 'external']},
                )
            for analytic in results:
                lower_name = analytic.name.lower()  # for future sorting
                if not found_analytics.get(lower_name):
                    found_analytics[lower_name] = {
                        'name': analytic.name,
                        'external': getattr(analytic, 'external', False),
                        'display_name': analytic.display_name,
                        'domains': set(),
                    }
                found_analytics[lower_name]['domains'].add(domain)
    except ResponseError as e:
        print_error(f'Cannot search for analytics: {e}', raise_exit=True)

    kind = '' if display_all else 'custom '

    if len(found_analytics) > 0:
        table: Dict[str, list] = {
            'Analytic display name': [],
            'Name': [],
            'Kind': [],
            'Exposed domains': [],
        }
        for _, a in sorted(found_analytics.items()):  # alphabetic sort on keys
            table['Analytic display name'].append(green_bold(a['display_name']))
            table['Name'].append(blue_bold(a['name']))
            table['Kind'].append('Custom' if a['external'] else 'Catalog')
            table['Exposed domains'].append(', '.join(sorted(a['domains'])))

        typer.secho(tabulate(
            table,
            headers='keys',
            tablefmt='pretty',
            colalign='left'
        ))

        print()
        print(f'{len(found_analytics)} {kind}analytics displayed')

    else:
        print(f'No {kind}exposed analytic found.')


@app.command()
def enable(
    analytic_name: str = typer.Argument(...),
    company: str = typer.Option(
        default=None,
        help='Identifier of the company to enable the analytic, or list of such '
             'identifiers (comma separated values).\n\n'
             'When providing the identifier of the root company of your domain, '
             'the analytic is enabled by default for all the companies of the '
             'domain (equivalent to using the --domain option).',
    ),
    domain: str = typer.Option(
        default=None,
        help='Use this option to make the analytic enabled by default for all '
             'companies of the specified domains (comma separated values) '
             '(equivalent to using the --company option providing the '
             'root company identifier(s) of these domains).\n\n'
             'Apart from this default behavior on domain, the analytic can be '
             'enabled or disabled separately on each company of the domain.',
    ),
):
    """Enable an analytic on companies"""
    if company and domain:
        print_error('Dot not use both options --company and --domain',
                    raise_exit=True)

    sdk = alteia_sdk()

    # check the analytic name, will raise error if not found
    find_analytics(sdk, analytic_name=analytic_name)

    if company:
        # enable directly from company IDs
        for company in company.split(','):
            try:
                sdk.analytics.enable(analytic_name, company)
                print_ok(f'Analytic "{analytic_name}" successfully enabled '
                         f'on the company "{company}".')
            except ResponseError as e:
                print_error(f'Cannot enable the analytic "{analytic_name}" '
                            f'on the company "{company}": {e}')
    elif domain:
        # check domains and get root companies to enable on them,
        # will raise error if at least one not found
        domains_root_companies = get_root_companies_of_domains(sdk, domain_names=domain)
        for domain_name, root_company_id in domains_root_companies:
            try:
                with utils.spinner():
                    sdk.analytics.enable(analytic_name, root_company_id)
                print_ok(f'Analytic "{analytic_name}" successfully enabled '
                         f'by default on domain "{domain_name}" '
                         f'(root company: {root_company_id})')
            except ResponseError as e:
                print_error(f'Cannot enable the analytic "{analytic_name}" '
                            f'on domain "{domain_name}" '
                            f'(root company: {root_company_id}): {e}')
    else:
        print_error('At least one option --company or --domain must be used',
                    raise_exit=True)


@app.command()
def disable(
    analytic_name: str = typer.Argument(...),
    company: str = typer.Option(
        default=None,
        help='Identifier of the company to disable the analytic, or list of such '
             'identifiers (comma separated values).\n\n'
             'When providing the identifier of the root company of your domain, '
             'the analytic is disabled by default for all the companies of the '
             'domain (equivalent to using the --domain option).',
    ),
    domain: str = typer.Option(
        default=None,
        help='Use this option to make the analytic disabled by default for all '
             'companies of the specified domains (comma separated values) '
             '(equivalent to using the --company option providing the '
             'root company identifier(s) of these domains).\n\n'
             'Apart from this default behavior on domain, the analytic can be '
             'enabled or disabled separately on each company of the domain.',
    ),
):
    """Disable an analytic on companies"""
    if company and domain:
        print_error('Dot not use both options --company and --domain',
                    raise_exit=True)

    sdk = alteia_sdk()

    # check the analytic name, will raise error if not found
    find_analytics(sdk, analytic_name=analytic_name)

    if company:
        # disable directly from company IDs
        for company in company.split(','):
            try:
                sdk.analytics.disable(analytic_name, company)
                print_ok(f'Analytic "{analytic_name}" successfully disabled '
                         f'on the company "{company}".')
            except ResponseError as e:
                print_error(f'Cannot disable the analytic "{analytic_name}" '
                            f'on the company "{company}": {e}')
    elif domain:
        # check domains and get root companies to enable on them,
        # will raise error if at least one not found
        domains_root_companies = get_root_companies_of_domains(sdk, domain_names=domain)
        for domain_name, root_company_id in domains_root_companies:
            try:
                with utils.spinner():
                    sdk.analytics.disable(analytic_name, root_company_id)
                print_ok(f'Analytic "{analytic_name}" successfully disabled '
                         f'by default on domain "{domain_name}" '
                         f'(root company: {root_company_id})')
            except ResponseError as e:
                print_error(f'Cannot disable the analytic "{analytic_name}" '
                            f'on domain "{domain_name}" '
                            f'(root company: {root_company_id}): {e}')
    else:
        print_error('At least one option --company or --domain must be used',
                    raise_exit=True)


@app.command(name='list-orderable')
def list_orderable(
    company_id: str = typer.Argument(...),
    display_all: bool = typer.Option(
        False, '--all', case_sensitive=False,
        help='If set, display all kinds of analytics '
             '(otherwise only custom analytics are displayed).'
    ),
):
    """List orderable analytics on a company"""
    sdk = alteia_sdk()

    search_filter = {'is_backoffice': {'$ne': True}}
    if not display_all:
        search_filter['external'] = {'$eq': True}

    found_analytics: Dict[str, dict] = {}
    try:
        with utils.spinner():
            results = sdk.analytics.search_generator(
                filter=search_filter,
                can_be_ordered_by_companies=[company_id],
                fields={'include': ['name', 'display_name', 'external']},
                sort={'name': 1},
            )
        for analytic in results:
            # group because of versions
            if not found_analytics.get(analytic.name):
                found_analytics[analytic.name] = {
                    'external': getattr(analytic, 'external', False),
                    'display_name': analytic.display_name,
                }
    except ResponseError as e:
        print_error(f'Cannot search for analytics: {e}', raise_exit=True)

    kind = '' if display_all else 'custom '

    if len(found_analytics) > 0:
        table: Dict[str, list] = {
            'Analytic display name': [],
            'Name': [],
            'Kind': [],
        }
        for a_name, a in found_analytics.items():
            table['Analytic display name'].append(green_bold(a['display_name']))
            table['Name'].append(blue_bold(a_name))
            table['Kind'].append('Custom' if a['external'] else 'Catalog')

        typer.secho(tabulate(
            table,
            headers='keys',
            tablefmt='pretty',
            colalign=('left', 'left', 'left'),
        ))

        print()
        print(f'{len(found_analytics)} {kind}analytics displayed')
    else:
        print(f'No {kind}orderable analytic found.')


@app.command(name="set-docker-credentials-name")
def set_docker_credentials_name(
    name: str = typer.Argument(...),
    version: str = typer.Option(
        ...,
        help='Version of the analytic to update.',
    ),
    company: str = typer.Option(
        ...,
        help='Short name of the company owning the analytic.',
    ),
    docker_credentials_name: str = typer.Option(
        ...,
        help='Name of the credentials to use to pull the docker'
             'image from the registry. The credentials must have been created'
             'beforehand using the credentials API',
    ),
):
    """
    Set docker credentials name.
    """

    sdk = alteia_sdk()

    if not version:
        typer.secho(
            '✖ A version is required',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    found_analytics = find_analytics(sdk, analytic_name=name, version_range=version)

    if not company:
        typer.secho(
            '✖ A company shortname is required',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)

    if len(found_analytics) != 0:
        for analytic in found_analytics:
            found = cast(
                ResourcesWithTotal,
                sdk.companies.search(
                    filter={'short_name': {'$eq': company}},
                    limit=1,
                    return_total=True
                )
            )
            if found.total != 1:
                typer.secho(
                    f'✖ Impossible to find company with shortname {company}:',
                    fg=typer.colors.RED
                )
                raise typer.Exit(1)

            company = found.results[0]._id
            check_credentials(sdk, company=company, credential_name=docker_credentials_name)

            try:
                sdk.analytics.set_docker_credentials(
                    name=name,
                    version=version,
                    company=company,
                    docker_credentials_name=docker_credentials_name
                )

                print_ok(f'Docker credentials name "{docker_credentials_name}" '
                         f'was successfully set on the analytic {name} with id "{analytic._id}".')
            except Exception as ex:
                print_error(
                    f'Impossible to set docker credentials name "{name}" with error {ex}'
                )
                raise typer.Exit(code=1)
