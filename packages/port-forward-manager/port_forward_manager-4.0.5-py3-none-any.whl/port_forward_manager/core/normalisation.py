import rich

from port_forward_manager.core import models


def base_normalisation(record):
    record_id = str(record.get("id"))
    if len(str(record_id)) != 12:

        record["id"] = models.generate_uid()
        rich.print(f"Creating ID {record_id} vs {record["id"]} {len(record["id"])}")
        record_id = record["id"]


    return record_id


def normalise_import(settings):
    rich.print("Normalise import")

    group_index = {}
    schema_index = {}
    session_index = {}
    ssh_group_index = {}

    for record in settings.get("groups", []):
        record_id = base_normalisation(record)
        group_index[record_id] = models.Group(**record)

    # rich.print("Groups", group_index)

    for record in settings.get("schemas", []):
        record_id = base_normalisation(record)

        previous_group_id = str(record.get("group_id"))
        group = group_index.get(previous_group_id)
        if not group:
            rich.print(f"Error: Group not found {previous_group_id}")
            continue

        record['group_id'] = group.id
        record['active'] = False

        schema_index[record_id] = models.Schema(**record)

    # rich.print("Schemas", schema_index)

    for record in settings.get("sessions", []):
        record_id = base_normalisation(record)

        schema_id = str(record.get("schema_id"))
        schema = schema_index.get(schema_id)

        if not schema:
            rich.print(f"Session parent schema not found {schema_id}")
            continue

        record["schema_id"] = schema.id

        session_index[record_id] = models.Session(**record)

    # rich.print("Sessions", session_index)

    for record in settings.get("ssh_groups", []):
        record_id = str(record.get("id"))

        if len(str(record_id)) == 12:
            record["id"] = models.generate_uid()

        schema_id = str(record.get("schema_id"))
        schema = schema_index.get(schema_id)
        if not schema:
            rich.print(f"Error: SSHGroup schema not found {schema_id}")
            continue

        record["schema_id"] = schema.id
        ssh_group_index[record_id] = models.SSHGroup(**record)

    # rich.print("SSHGroups", ssh_group_index)

    settings["groups"] = list(group_index.values())
    settings["schemas"] = list(schema_index.values())
    settings["sessions"] = list(session_index.values())

    return settings