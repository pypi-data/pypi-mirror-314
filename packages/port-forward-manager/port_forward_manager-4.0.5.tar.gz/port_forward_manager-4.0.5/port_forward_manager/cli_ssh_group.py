import typer
import rich
from rich.prompt import Confirm
from sqlalchemy.exc import IntegrityError

from port_forward_manager.core.ui import prepare_ssh_group_table
from port_forward_manager.core import models, database

app = typer.Typer(no_args_is_help=True)
db = database.get_session()


@app.command()
def index(name=typer.Argument(None, help='Group name criteria to search')):
    """
    List SSH groups
    """
    table = prepare_ssh_group_table()
    for group in models.SSHGroup.index(name):
        row = [
            str(group.id),
            group.schema.name,
            group.group_name,
            group.label,
        ]
        table.add_row(*row)

    rich.print(table)


@app.command()
def create(schema_id=typer.Argument(..., help='Schema ID'),
           name=typer.Argument(..., help='Group unique name'),
           label=typer.Argument(..., help='Group label')):
    """
    Create SSH group
    """
    schema = models.Schema.find_by_id(schema_id)
    if not schema:
        print(f"Group '{schema_id}' doesn't exist")
        exit(401)

    ssh_group = models.SSHGroup(group_name=name, label=label)
    schema.ssh_groups.append(ssh_group)
    models.db_session.commit()

    try:
        models.db_session.commit()
    except IntegrityError as e:
        print(f"Name MUST be unique {e.args}")
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


@app.command()
def update(group_id=typer.Argument(..., help="Group ID"),
           name=typer.Option(None, help='Group unique name'),
           label=typer.Option(None, help='Group label')):
    """
    Update SSH group
    """
    group = models.SSHGroup.find_by_id(group_id)
    if not group:
        print("Group ID not found")
        exit(401)

    if name:
        group.name = name

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
def delete(group_id: int = typer.Argument(None, help='Group name'),
           force: bool = typer.Option(False, '-f', help="Force delete")):
    """Delete SSH group"""

    group = models.SSHGroup.find_by_id(group_id)
    if group is None:
        print(f"Group '{group_id}' not found")
        exit()

    if force or Confirm.ask(f"Are you sure you want to delete '{group.label}'?"):
        models.SSHGroup.delete(group)
