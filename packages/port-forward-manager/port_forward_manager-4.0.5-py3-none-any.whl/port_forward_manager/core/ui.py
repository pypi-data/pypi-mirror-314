import rich
from rich.table import Table

from port_forward_manager.core import models


def prepare_schema_table(
    show_alias: bool = False,
    show_link: bool = False,
    show_schema: bool = True,
    title: str = "Schemas",
):

    table = Table(show_edge=False)

    table.add_column("ID", justify="right", style="green", width=12)
    table.add_column("Group", justify="left", style="yellow", width=20)
    table.add_column("Label", justify="left", style="yellow", width=30)
    table.add_column("Active", justify="right", style="yellow", width=30)
    return table


def prepare_group_table(
        show_alias: bool = False,
        show_link: bool = False,
        show_schema: bool = True,
        title: str = 'Schemas'
):

    table = Table(show_edge=False)

    table.add_column("ID", justify="right", style="yellow", width=12)
    table.add_column("Label", justify="left", style="green", width=30)
    table.add_column("Type", justify="center", style="yellow", width=15)

    return table


def prepare_ssh_group_table():

    table = Table(show_edge=False)

    table.add_column("ID", justify="right", style="green", width=12)
    table.add_column("Schema", justify="left", style="yellow", width=30)
    table.add_column("Label", justify="left", style="yellow", width=30)

    return table


def prepare_sessions_table(show_link: bool = False):
    table = Table(show_edge=False, pad_edge=False, expand=True)

    table.add_column("ID", justify="right", style="yellow", width=12)
    table.add_column("Label", style="green", width=30)
    table.add_column("Schema", style="green", width=30)
    table.add_column("Hostname", justify="left", style="yellow", width=30)
    table.add_column("Type", justify="center", style="yellow", width=7)
    table.add_column("Local binding", justify="left", style="white", width=22)
    table.add_column("Remote binding", justify="left", style="blue", width=22)

    if show_link:
        table.add_column("URL", justify="left", style="cyan", width=60)

    return table


def get_sessions_table(records: list) -> Table:
    table = prepare_sessions_table()
    for session in records:
        port = "auto" if session.local_port_dynamic else session.local_port.__str__()

        row = [
            session.id,
            session.label,
            session.schema.label,
            session.hostname,
            session.type,
            f"{session.local_address}:{port}",
            f"{session.remote_address}:{session.remote_port.__str__()}",
        ]

        table.add_row(*row)

    if table.row_count > 0:
        table.rows[table.row_count - 1].end_section = True

    return table


def print_session(session: models.Session):
    table = prepare_sessions_table()
    row = [
        str(session.id),
        session.schema.name,
        session.hostname,
        session.type,
        session.local_address,
        "auto" if session.local_port_dynamic else session.local_port.__str__(),
        session.remote_address,
        session.remote_port.__str__(),
        session.label,
    ]

    table.add_row(*row)

    table.rows[table.row_count - 1].end_section = True
    rich.print(table)
