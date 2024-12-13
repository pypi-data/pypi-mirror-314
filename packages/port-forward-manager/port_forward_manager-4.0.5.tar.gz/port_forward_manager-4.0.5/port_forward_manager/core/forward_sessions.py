import subprocess
import random
from rich import print

from port_forward_manager.core.ui import prepare_sessions_table
from port_forward_manager.core import models, tools


def execute(command):
    # print(command)
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # inspect(result)
    # exit(1)
    if result.returncode != 0:
        print(f"Command [b]{command}[/] failed:\n {result.stderr}")
        exit(3)

    return result


def stop(session: models.Session):
    if session.connected:
        print("Stop session {tmux_id}.".format(tmux_id=session.tmux_id))
        stop_command = "tmux kill-session -t '{tmux_id}'".format(
            tmux_id=session.tmux_id
        )
        execute(stop_command)


def in_active_sessions(definition, active_sessions):
    for session in active_sessions:
        shared_items = {
            k: session[k]
            for k in session
            if k in definition and session[k] == definition[k]
        }
        # print(len(shared_items))
        if len(shared_items) >= 7:
            return True

    return False


def generate_new_port(port_list):
    while True:
        port = str(random.randint(9100, 9500))
        if port not in port_list:
            port_list.append(port)
            return port


def start(session, reconnect: bool = False):
    settings = tools.settings()
    if reconnect and session.connected:
        # print(f"[b]Stopping '{session_name}'[/b]")
        stop(session)

    if not session.connected:
        generate_port = False

        if not session.local_port:
            generate_port = True

        if session.local_port in settings.ports_active:
            if session.local_port_dynamic:
                print(
                    f"[b]Warning[/b]: Local port {session.local_port} already in use, assigning new port"
                )
                generate_port = True
            else:
                print(f"[b]Warning[/b]: Local port {session.local_port} already in use")
                exit()

        if generate_port:
            session.local_port = generate_new_port(settings.ports_active)

        result = execute(session.command)
        return result
    else:
        print(
            "Ignoring {type} forward on [b]{hostname}[/b] {remote_address}:{remote_port}.".format(
                **session.dict()
            )
        )


def refresh_state():
    update_state()
    for session in models.Session.index():
        if not session.active or session.connected:
            continue

        start(session)


def update_state():
    settings = tools.settings()

    # Reset state
    settings.ports_active = []
    for schema in models.Schema.index():
        schema.active = False

        for session in schema.sessions:
            session.connected = False

    # Update state from tmux sessions
    command = "tmux ls | grep 'pfm_session' | cut -d ':' -f 1"
    result = execute(command)

    session_id_list = result.stdout.split("\n")

    for session_id in session_id_list:
        if len(session_id) == 0:
            continue

        session_data = session_id.replace("_", ".").replace(":", "")
        # print(f"Active -> {session_id}")
        values = session_data.split("|")

        if len(values) == 8:
            (
                filler,
                schema_id,
                hostname,
                remote_host,
                remote_port,
                local_address,
                local_port,
                forward_type,
            ) = values

            schema = models.Schema.find_by_id(schema_id)
            if schema:
                # schema.active = True
                session = schema.get_session(forward_type, hostname, int(remote_port))
                if not session:
                    # print(f"missing session definition {hostname} {remote_port} {forward_type}")
                    continue

                session.connected = True
                schema.active = True
                # session.local_address = local_address
                session.local_port = int(local_port)
                settings.ports_active.append(session.local_port)
            else:
                continue
                # print("TMUX session active but missing session definition.")


def filter_session(
    session: models.Session, schema_id: str = None, host: str = None, port: str = None
):
    if schema_id and schema_id != session.schema_id:
        return True
    if host and host not in session.hostname:
        return True
    if port and port != session.remote_port:
        return True


def list_from_active(key, filter_string: str = ""):
    items = []

    for schema in models.Schema.index():
        for session in schema.sessions:
            if not session.active:
                continue

            item = session.label
            if filter_string not in item:
                continue

            if item not in items:
                items.append(item)

    return items


def show_active_sessions(schema: str = None, host: str = None, port: int = None):
    update_state()

    table = prepare_sessions_table(True)
    session_count = 0
    for schema in models.Schema.index():
        schema_rows = False
        for session in schema.sessions:
            if not session.connected:
                continue

            schema_rows = True

            row = [
                f"{schema.label}",
                session.hostname,
                session.type,
                session.local_address,
                "auto" if session.local_port_dynamic else session.local_port.__str__(),
                session.remote_address,
                session.remote_port.__str__(),
                session.url,
            ]

            table.add_row(*row)
            session_count += 1

        if schema_rows:
            table.rows[table.row_count - 1].end_section = True

    if session_count > 0:
        print(table)
    else:
        print("Nothing to see here")
