from click.shell_completion import CompletionItem, Context
from sshconf import read_ssh_config
from os.path import expanduser

from port_forward_manager.core import models, forward_sessions


# Auto completion
def ac_groups(incomplete):
    result = []

    for group in models.Group.index():
        if incomplete not in group.label:
            continue

        item = (group.id, f"{len(group.schemas)} schema(s) for {group.label}")
        result.append(item)
    return result


def ac_schemas(incomplete):
    schemas = models.Schema.index()
    result = []

    for schema in schemas:
        if not schema.label.startswith(incomplete):
            continue

        item = (schema.id, f"{len(schema.sessions)} session(s) for {schema.group.label} - {schema.label}")
        result.append(item)
    return result


def ac_active_schemas(incomplete):
    items = []
    for schema in models.Schema.index():
        if schema.active:
            items.append(schema.name)

    return items


def ac_hosts(incomplete):
    result = []
    c = read_ssh_config(expanduser("~/.ssh/config"))
    for host in c.hosts():
        if "*" not in host and host.startswith(incomplete):
            hosts = host.split(" ")
            for hostname in hosts:
                result.append(hostname)

    return result


# Shell completion
def sc_schemas(ctx: Context, param, incomplete):
    result = []

    group_id = ctx.params.get("gf")
    schemas = models.Schema.index(group_id=group_id)

    item = CompletionItem("Hello", help=f"{ctx.params}")
    result.append(item)
    for schema in schemas:
        if not group_id and incomplete not in schema.label:
            continue

        item = CompletionItem(schema.label, help=f"{len(schema.sessions)} session(s) for {schema.label} {ctx.params}")
        result.append(item)

    return result


def sc_active_schemas(ctx, param, incomplete):
    return forward_sessions.list_from_active('schema', incomplete)


def sc_active_remote_port(ctx, param, incomplete):
    return forward_sessions.list_from_active('remote_port')


def sc_active_hosts(ctx, param, incomplete):
    return forward_sessions.list_from_active('hostname')


def sc_hosts(ctx, param, incomplete):
    from sshconf import read_ssh_config
    from os.path import expanduser
    result = []
    c = read_ssh_config(expanduser("~/.ssh/config"))
    for host in c.hosts():
        if "*" not in host and host.startswith(incomplete):
            hosts = host.split(" ")
            for hostname in hosts:
                item = CompletionItem(hostname)
                result.append(item)

    return result
