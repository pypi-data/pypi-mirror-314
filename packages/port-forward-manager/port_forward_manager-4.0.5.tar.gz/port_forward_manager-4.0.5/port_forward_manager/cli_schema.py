import time
import rich
from rich.prompt import Confirm
import typer

from port_forward_manager.core import models, tools, database, forward_sessions
from port_forward_manager.core import autocomplete
from port_forward_manager.core.ui import prepare_sessions_table, prepare_schema_table
from port_forward_manager.core.forward_sessions import show_active_sessions

app = typer.Typer(no_args_is_help=True)
db = database.get_session()


@app.command()
def create(
    group_id: str = typer.Argument(..., help="Group name"),
    label: str = typer.Argument(..., help="Schema label"),
):
    """
    Create a schema
    """
    group = models.Group.find_by_id(group_id)
    if group is None:
        print(f"Group '{group_id}' doesn't exist")
        exit(401)

    schema = models.Schema(label=label, group_id=group.id)
    group.schemas.append(schema)

    models.db_session.commit()


@app.command()
def update(
    schema_id: str = typer.Argument(..., help="Schema ID"),
    group_id: str = typer.Option(None, help="Group ID"),
    label: str = typer.Option(None, help="Schema label"),
):
    """
    Create a schema
    """
    schema = models.Schema.find_by_id(schema_id)
    if schema is None:
        print(f"Schema '{schema_id}' doesn't exist")
        exit(401)

    if group_id:
        group = models.Group.find_by_id(group_id)
        if not group:
            print("Group is invalid")
        else:
            schema.group_id = group_id

    if label:
        schema.label = label

    models.db_session.commit()


@app.command()
def index(
        schema_filter: str = typer.Argument(None, shell_complete=autocomplete.sc_schemas),
        gid: str = typer.Option(None, help="Group ID", autocompletion=autocomplete.ac_groups)
    ):
    """
    List configured schemas
    """
    settings = tools.settings()
    table = prepare_schema_table(True, settings.show_schema_link, True)

    print(f"Group: {gid}")

    for schema in models.Schema.index(schema_filter, gid):
        if schema.group_id is None:
            print(f"Schema #{schema.id} group is INVALID")
            row = [
                str(schema.id),
                "INVALID GROUP",
                schema.label,
                "Yes" if schema.active else "No",
            ]
        else:
            row = [
                str(schema.id),
                schema.group.label,
                schema.label,
                "Yes" if schema.active else "No",
            ]
        table.add_row(*row)

    if table.row_count > 0:
        table.rows[table.row_count - 1].end_section = True

    rich.print(table)


@app.command()
def clone(
    schema_id: str = typer.Argument(..., help="Schema ID"),
    group_id: str = typer.Option(None, help="Group ID"),
    label: str = typer.Option(None, help="Schema label"),
):

    schema_original = models.Schema.find_by_id(schema_id)
    if schema_original is None:
        print(f"Schema {schema_id} not found")
        exit(3)

    if group_id is None:
        group_id = schema_original.group_id

    group = models.Group.find_by_id(group_id)
    if not group:
        print(f"Group {group_id} not found")
        exit(3)

    if not label:
        label = f"{schema_original.label} clone"

    schema_clone = models.Schema(label=label)
    group.schemas.append(schema_clone)

    for session_original in schema_original.sessions:
        session_clone = models.Session.clone(session_original)

        print(f"Clone session {session_clone.label}")
        if session_clone.local_port_dynamic:
            session_clone.local_port = 0

        schema_clone.sessions.append(session_clone)

    models.db_session.commit()


@app.command()
def delete(
    schema_id: str = typer.Argument(None, help="Schema ID"),
    force: bool = typer.Option(False, help="Force delete"),
):
    """Delete session"""

    schema = models.Schema.find_by_id(schema_id)
    if schema is None:
        print("Schema not found")
        exit()

    if force or Confirm.ask(f"Are you sure you want to delete '{schema.label}'?"):
        models.Schema.delete(schema)


@app.command()
def sessions(schema_filter: str = typer.Argument(None, autocompletion=autocomplete.ac_schemas)):
    """
    List configured schemas
    """
    table = prepare_sessions_table()

    for schema in models.Schema.index(schema_filter):
        for session in schema.sessions:
            row = [
                str(schema.id),
                session.hostname,
                session.type,
                session.local_address,
                "-----" if session.local_port_dynamic else session.local_port.__str__(),
                session.remote_address,
                session.remote_port.__str__(),
                session.label,
            ]
            table.add_row(*row)
        if table.row_count > 0:
            table.rows[table.row_count - 1].end_section = True

    rich.print(table)


@app.command()
def start(
    schema_id: str = typer.Argument(..., autocompletion=autocomplete.ac_schemas),
    force: bool = typer.Option(None, help="Force sessions reconnection"),
):
    """
    Start a schema of forwarding sessions
    """
    settings = tools.settings()
    forward_sessions.update_state()

    schema = models.Schema.find_by_id(schema_id)

    if schema is None:
        print("[b]Schema '{0}' is unknown[/b]".format(schema_id))
        exit(-1)

    schema.active = True

    for session in schema.sessions:
        session.schema_id = schema.id
        if session.auto_start:
            forward_sessions.start(session, force)
            session.active = True

    time.sleep(settings.wait_after_start)
    show_active_sessions()
    models.db_session.commit()


@app.command()
def stop(
    schema_id: str = typer.Argument(None, autocompletion=autocomplete.ac_active_schemas),
    hostname: str = typer.Option(None, shell_complete=autocomplete.sc_active_hosts),
    port: str = typer.Option(None, shell_complete=autocomplete.sc_active_remote_port),
):
    """
    Stop sessions from active schema, host or port
    """

    if not schema_id and not hostname and not port:
        print("[b]Pick a schema, host or host and port or --all[/b]")
        exit(-1)

    settings = tools.settings()
    forward_sessions.update_state()

    if schema_id:
        schema = models.Schema.find_by_id(schema_id)

        if not schema:
            print("[b]Schema not found")
            exit(-1)

        for session in schema.sessions:

            forward_sessions.stop(session)
            session.active = False
        schema.active = False

    time.sleep(settings.wait_after_stop)
    show_active_sessions()
    models.db_session.commit()
