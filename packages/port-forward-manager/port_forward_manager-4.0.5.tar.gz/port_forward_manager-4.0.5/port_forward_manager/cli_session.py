import typer
import time
from enum import Enum
import rich
from rich.prompt import Confirm

from port_forward_manager.core.autocomplete import ac_schemas
from port_forward_manager.core.ui import get_sessions_table, print_session
from port_forward_manager.core import models, tools, database
from port_forward_manager.core.forward_sessions import update_state, start as start_session, stop as stop_session

app = typer.Typer(no_args_is_help=True)
db = database.get_session()


class SessionTypes(str, Enum):
    local = "local"
    remote = "remote"
    ssh = "ssh"


@app.command()
def index(
    hostname: str = typer.Argument(None, help="Hostname"),
    active: bool = typer.Option(False, help="Active sessions"),
    schema: str = typer.Option(None, help="Filter by schema", autocompletion=ac_schemas),
):
    """
    List sessions
    """
    records = []
    for session in models.Session.index(hostname, schema_id=schema):
        if active and not session.active:
            continue

        records.append(session)

    update_state()
    table = get_sessions_table(records)
    rich.print(table)


@app.command()
def create(
    schema_name: str = typer.Argument(None, help="Schema name"),
    session_type: SessionTypes = typer.Argument(
        SessionTypes.local, help="Session type", case_sensitive=False
    ),
    label: str = typer.Argument(None, help="Session label"),
    hostname: str = typer.Argument(None, help="Session hostname"),
    remote_address: str = typer.Option("127.0.0.1", help="Remote address"),
    remote_port: int = typer.Option(0, help="Remote address", min=0, max=65535),
    local_address: str = typer.Option("127.0.0.1", help="Remote address"),
    local_port: int = typer.Option(0, help="Remote address", min=0, max=65535),
    local_port_dynamic: bool = typer.Option(True, help="Assign local port dynamically"),
    auto_start: bool = typer.Option(True, help="Remote address"),
    url_format: str = typer.Option(
        "http://{hostname}:{local_port}", help="Dynamic URL"
    ),
    schema_id: bool = typer.Option(True, help="Use schema ID instead of name"),
):
    """
    Create session
    """
    if schema_id:
        schema = models.Schema.find_by_id(int(schema_name))
    else:
        schema = models.Schema.find_by_label(schema_name)

    if not schema:
        print(f"Schema '{schema_name}' doesn't exist")
        exit(401)

    session = models.Session()
    session.type = session_type.value
    session.label = label
    session.hostname = hostname
    session.remote_address = remote_address
    session.remote_port = remote_port
    session.local_address = local_address
    session.local_port = local_port
    session.local_port_dynamic = local_port_dynamic
    session.auto_start = auto_start
    session.url_format = url_format
    schema.sessions.append(session)
    models.db_session.commit()
    print_session(session)


@app.command()
def delete(
    session_id: str = typer.Argument(None, help="Session ID"),
    force: bool = typer.Option(False, help="Force delete"),
):
    """Delete session"""
    session = models.Session.find_by_id(session_id)
    if force or Confirm.ask(f"Are you sure you want to delete '{session.label}'?"):
        models.Session.delete(session)


@app.command()
def update(
    session_id: str = typer.Argument(None, help="Session ID"),
    schema_name: str = typer.Option(None, help="Schema name"),
    session_type: SessionTypes = typer.Option(
        None, help="Session type", case_sensitive=False
    ),
    label: str = typer.Option(None, help="Session label"),
    hostname: str = typer.Option(None, help="Session hostname"),
    remote_address: str = typer.Option(None, help="Remote address"),
    remote_port: int = typer.Option(None, help="Remote address", min=0, max=65535),
    local_address: str = typer.Option(None, help="Remote address"),
    local_port: int = typer.Option(None, help="Remote address", min=0, max=65535),
    local_port_dynamic: bool = typer.Option(None, help="Assign local port dynamically"),
    auto_start: bool = typer.Option(None, help="Remote address"),
    url_format: str = typer.Option(None, help="Dynamic URL"),
    schema_id: bool = typer.Option(True, help="Use schema ID instead of name"),
):
    """
    Update session settings
    """

    session = models.Session.find_by_id(session_id)
    if not session:
        print("Session ID not found")
        exit(401)

    if session_type:
        session.type = session_type.value

    if label:
        session.label = label

    if hostname:
        session.hostname = hostname

    if remote_address:
        session.remote_address = remote_address

    if remote_port:
        session.remote_port = remote_port

    if local_address:
        session.local_address = local_address

    if local_port:
        session.local_port = local_port

    if local_port_dynamic:
        session.local_port_dynamic = local_port_dynamic

    if auto_start:
        session.auto_start = auto_start

    if url_format:
        session.url_format = url_format

    if schema_name:
        if schema_id:
            schema = models.Schema.find_by_id(int(schema_name))
        else:
            schema = models.Schema.find_by_label(schema_name)
        if schema is None:
            print(f"Schema '{schema_name}' doesn't exist")
            exit(401)

        session.schema_id = schema.id

    models.db_session.commit()
    print_session(session)


@app.command()
def connect(
    label: str = typer.Argument(..., help="Session label"),
    hostname: str = typer.Argument(..., help="Session hostname"),
    remote_port: int = typer.Argument(..., help="Remote address", min=0, max=65535),
    session_type: SessionTypes = typer.Option(
        SessionTypes.local, help="Session type", case_sensitive=False
    ),
    remote_address: str = typer.Option("127.0.0.1", help="Remote address"),
    local_address: str = typer.Option("127.0.0.1", help="Remote address"),
    local_port: int = typer.Option(0, help="Remote address", min=0, max=65535),
):
    """
    Connect ephemeral session
    """
    settings = tools.settings()

    schema = models.Group.find_by_type('ephemeral').schemas[0]

    if schema is None:
        print(f"Ephemeral schema doesn't exist")
        exit(401)

    session = models.Session()
    session.type = session_type.value
    session.label = label
    session.hostname = hostname
    session.remote_address = remote_address
    session.remote_port = remote_port
    session.local_address = local_address
    session.local_port = local_port
    session.local_port_dynamic = local_port == 0
    session.auto_start = False
    session.url_format = ""
    schema.sessions.append(session)
    models.db_session.commit()

    start(session, False)
    session.active = True
    session.connected = True

    time.sleep(settings.wait_after_start)
    models.db_session.commit()

    print_session(session)


@app.command()
def start(session_id: str = typer.Argument(None, help="Session ID")):
    """
    Start session
    """
    update_state()
    session = models.Session.find_by_id(session_id)

    if not session:
        print("Session doesn't exist")
        exit()

    session.active = True

    start_session(session)
    models.db_session.commit()


@app.command()
def stop(session_id: str = typer.Argument(None, help="Session ID")):
    """
    Disconnect session
    """
    update_state()
    session = models.Session.find_by_id(session_id)

    if not session:
        print("Session doesn't exist")
        exit()

    session.active = False

    stop_session(session)

    if session.schema.group.type == "ephemeral":
        print("Delete ADHOC session")
        models.Session.delete(session)

    stopped = True
    for child in session.schema.sessions:
        if child.active:
            stopped = False

    session.schema.active = stopped

    models.db_session.commit()


@app.command()
def disconnect(session_id: str = typer.Argument(None, help="Session ID")):
    """
    Disconnect session
    """
    update_state()
    session = models.Session.find_by_id(session_id)

    if not session:
        print("Session doesn't exist")
        exit()

    if Confirm.ask(f"Are you sure you want to disconnect '{session.label}'?"):
        stop(session)

        if session.schema.name == "port_forward_manager-ephemeral":
            print("Delete ADHOC session")
            models.Session.delete(session)
