from importlib.metadata import version as current_version
import os.path
import rich
from rich.prompt import Confirm
from sshconf import read_ssh_config
import time
import typer
import yaml

from port_forward_manager.core import models, tools, forward_sessions
from port_forward_manager.core import autocomplete
from port_forward_manager import cli_group, cli_schema, cli_session, cli_ssh_group
from port_forward_manager.core.normalisation import normalise_import

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)
app.add_typer(cli_group.app, name="group", help="Group management")
app.add_typer(cli_schema.app, name="schema", help="Schema management")
app.add_typer(cli_session.app, name="session", help="Session management")
app.add_typer(cli_ssh_group.app, name="ssh_group", help="SSH group management")
tools.load_settings()


@app.command()
def shutdown():
    """
    Stop all active sessions
    """

    settings = tools.settings()

    forward_sessions.update_state()
    for schema in models.Schema.index():
        for session in schema.sessions:
            if session.connected:
                forward_sessions.stop(session)
            session.active = False
        schema.active = False

    time.sleep(settings.wait_after_stop)
    forward_sessions.show_active_sessions()
    models.db_session.commit()


@app.command()
def status(
    schema: str = typer.Option(None, shell_complete=autocomplete.sc_schemas),
    host: str = typer.Option(None, shell_complete=autocomplete.sc_hosts),
    port: int = None,
    json: bool = typer.Option(False, "--json", "-j", help="Output JSON"),
):
    """
    Show active sessions
    """

    forward_sessions.show_active_sessions(schema, host, port)


@app.command()
def state():
    """
    Show current state in JSON format
    """

    ssh_config = read_ssh_config(os.path.expanduser("~/.ssh/config"))
    ssh_hosts = []
    for host in ssh_config.hosts():
        if "*" in host:
            continue
        hosts = host.split(" ")
        for hostname in hosts:
            ssh_hosts.append(hostname)

    forward_sessions.refresh_state()
    time.sleep(0.5)
    forward_sessions.update_state()
    current_state = {
        "groups": models.Group.get_state(),
        "schemas": models.Schema.get_state(),
        "sessions": models.Session.get_state(),
        "ssh_groups": models.SSHGroup.get_state(),
        "ssh_hosts": ssh_hosts,
    }

    print(yaml.dump(current_state))
    # print(simplejson.dumps(current_state, indent=2))


@app.command()
def version():
    """
    Show PFM version
    """
    version_string = current_version("port_forward_manager")
    rich.print(f"Port Forward Manager [bold white]v{version_string}[/]")


@app.command()
def db_wipe():
    """Wipe the whole database clean"""
    if Confirm.ask(
        "This action will wipe all groups, schemas and sessions, are you sure?"
    ):
        models.reset_database()
        models.init_database()


@app.command()
def yaml_export(
    export_path: str = typer.Argument(None, help="YAML configuration file")
):
    """Import groups, schemas and sessions from configuration file"""
    export_data = {
        "export_format": "db_dump",
        "version": "2.0",
        "groups": models.Group.get_state(),
        "schemas": models.Schema.get_state(),
        "sessions": models.Session.get_state(),
        "ssh_groups": models.SSHGroup.get_state(),
    }

    yaml_string = yaml.dump(export_data)
    if export_path:
        tools.write_file(export_path, yaml_string)
    else:
        print(yaml_string)


@app.command()
def yaml_import(
    export_path: str = typer.Argument(..., help="YAML configuration file"),
    wipe: bool = typer.Option(False, help="Wipe DB"),
    force: bool = typer.Option(False, help="Force wipe"),
    prune: bool = typer.Option(False, help="Prune missing entries"),
):
    """Import groups, schemas and sessions from configuration file"""
    settings = tools.load_yaml_file(export_path)

    change_count = 0

    if settings.get("export_format") != "db_dump":
        rich.print("[red]Invalid export file format[/]")
        exit()

    if wipe and not force:
        if Confirm.ask(
            "This action will wipe all groups, schemas and sessions, are you sure?"
        ):
            models.reset_database()
            models.init_database()
    elif wipe and force:
        models.reset_database()
        models.init_database()

    settings = normalise_import(settings)
    rich.print("Importing PFM DB DUMP")

    groups = {}
    schemas = {}
    sessions = {}

    # Import groups
    for group_definition in settings.get("groups", []):
        group = models.Group.find_by_id(group_definition.id)
        if not group:
            group = models.Group.find_by_label(group_definition.label)

        if not group:
            change_count += 1
            rich.print(f"* Creating group {group_definition.label} {group_definition.id}")
            models.Group.add(group_definition)
        else:
            for key, value in group_definition.dict().items():
                if key == "id":
                    group_definition.id = group.id
                    continue
                setattr(group, key, value)

        groups[group_definition.id] = group_definition

    # rich.print(f"Group insert: { groups }")
    if prune:
        for group in models.Group.index():
            # rich.print(f"* Checking group {group.label}")
            if group.id not in groups.keys():
                if not group.visible:
                    continue

                rich.print(f"  * Deleting group {group.label} - {group.id}")
                models.Group.delete(group)

    rich.print(f"Imported {change_count} groups")
    models.db_session.commit()

    # Import schemas
    for schema_definition in settings.get('schemas', []):
        # rich.print(f"Handling schema {schema_definition.id}")
        tmp_group = groups.get(schema_definition.group_id, {})

        # rich.print(f"  * Group", schema_definition.group_id, groups)
        group = models.Group.find_by_id(schema_definition.group_id)

        if not group:
            group = models.Group.find_by_label(tmp_group.get('label'))

        if not group:
            rich.print(f"IGNORING schema - Error could not find group {schema_definition.group_id}")
            continue

        schemas[schema_definition.id] = schema_definition.label

        schema = models.Schema.find_by_id(schema_definition.id)
        if not schema:
            change_count += 1
            # rich.print(f"* Importing schema {schema_definition.label}")
            group.schemas.append(schema_definition)
        elif not schema.active:
            # rich.print(f"* Update schema {schema_definition.label} {schema_definition.id}")
            for key, value in schema_definition.dict().items():
                setattr(schema, key, value)

    rich.print("Schemas prune")
    if prune:
        for schema in models.Schema.index():
            # rich.print(f"* Checking schema {schema.label}")
            if schema.id not in schemas.keys() and not schema.active:
                rich.print(f"  * Deleting schema {schema.id} {schema.label}")
                models.Schema.delete(schema)

    models.db_session.commit()

    # Import sessions
    for session_definition in settings.get("sessions"):
        schema_label = schemas.get(session_definition.schema_id)
        # rich.print(f"(yaml-import) Schema: {schema_label} '{session_definition.schema_id}'")

        schema = models.Schema.find_by_id(session_definition.schema_id)
        if not schema:
            rich.print(
                f"IGNORING session - Error could not find schema '{schema_label}'"
            )
            continue

        session = models.Session.find_by_id(session_definition.id)

        if not session:
            session = schema.get_session(
                session_definition.type,
                session_definition.hostname,
                session_definition.remote_port
            )

        if not session:
            change_count += 1
            print(f"    * Importing session {session_definition.type} {session_definition.hostname} {session_definition.remote_port}")
            if session_definition.local_port == 0:
                session_definition.local_port_dynamic = True

            schema.sessions.append(session_definition)
        else:
            for key in session.__fields__.keys() - ['connected', 'active']:
                value = getattr(session_definition, key)
                setattr(session, key, value)

        sessions[session_definition.id] = session_definition

    if prune:
        for session in models.Session.index():
            # rich.print(f"* Checking session {session.label}")
            if session.id not in sessions.keys() and not session.connected:
                rich.print(f"  * Deleting session")
                models.Session.delete(session)

    models.db_session.commit()

    # Import SSH groups
    for ssh_group in settings.get("sshGroups", []):
        schema = models.Schema.find_by_id(ssh_group.schema_id)
        if not schema:
            rich.print(
                f"IGNORING session - Error could not find schema '{ssh_group.schema_id}'"
            )
            continue

        group = schema.get_ssh_group(ssh_group.label)
        if not group:
            change_count += 1
            print(f"    * Importing SSH group {ssh_group.label}")

            schema.ssh_groups.append(ssh_group)

    models.db_session.commit()

    if change_count == 0:
        rich.print("No changes...")
    else:
        rich.print("There were {} items imported.".format(change_count))


def run():
    app()

