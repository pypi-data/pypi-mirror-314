import typer
import rich
from rich.prompt import Confirm
from sqlalchemy.exc import IntegrityError

from port_forward_manager.core.ui import prepare_schema_table, prepare_group_table
from port_forward_manager.core import models, database

app = typer.Typer(no_args_is_help=True)
db = database.get_session()


@app.command()
def index(name=typer.Argument(None, help='Criteria to search')):
    """
    List groups
    """
    table = prepare_group_table()
    for group in models.Group.index(name):
        row = [
            str(group.id),
            group.label,
            group.type,
        ]
        table.add_row(*row)

    rich.print(table)


@app.command()
def schemas(name=typer.Argument(None, help='Criteria to search')):
    """
    List groups
    """
    table = prepare_schema_table()
    for group in models.Group.index(name):
        for schema in group.schemas:
            row = [
                str(schema.id),
                group.label,
                schema.label,
                schema.label
            ]
            table.add_row(*row)

    rich.print(table)


@app.command()
def create(label=typer.Argument(None, help='Group label')):
    """
    Create a group
    """
    group = models.Group(label=label)
    db.add(group)
    try:
        db.commit()
    except IntegrityError as e:
        print(f"Name MUST be unique {e.args}")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


@app.command()
def update(group_id=typer.Argument(None, help="Group ID"),
           label=typer.Option(None, help='Group label')):
    """
    Update a group
    """
    group = models.Group.find_by_id(group_id)
    if not group:
        print("Session ID not found")
        exit(401)

    if label:
        group.label = label

    try:
        models.db_session.commit()
    except IntegrityError as e:
        print(f"Name MUST be unique {e.args}")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


@app.command()
def delete(group_id: str = typer.Argument(None, help='Group ID'),
           force: bool = typer.Option(False, help="Force delete")):
    """Delete session"""

    group = models.Group.find_by_id(group_id)
    if group is None:
        print(f"Group '{group_id}' not found")
        exit()

    if force or Confirm.ask(f"Are you sure you want to delete '{group.label}'?"):
        models.Group.delete(group)
