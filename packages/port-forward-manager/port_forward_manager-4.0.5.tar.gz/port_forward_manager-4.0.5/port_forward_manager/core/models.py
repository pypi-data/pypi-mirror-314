from typing import List
from uuid import uuid4
import rich

from sqlmodel import Field, Relationship, SQLModel, select
from pydantic import computed_field

from port_forward_manager.core.database import get_session, engine


def generate_uid():
    return uuid4().hex[:12]


class Group(SQLModel, table=True):
    id: str = Field(default_factory=generate_uid, primary_key=True)
    label: str
    visible: bool = Field(default=True)
    order: int = Field(default=-1)
    type: str = Field(default="regular")

    schemas: list["Schema"] = Relationship(back_populates="group", cascade_delete=True)

    @staticmethod
    def delete(record: "Group"):
        db_session.delete(record)
        db_session.commit()

    @staticmethod
    def index(name=None):
        statement = select(Group).order_by(Group.label)

        if name:
            search = "%{}%".format(name)
            statement = statement.where(Group.label.like(search))

        cursor = db_session.exec(statement)
        return cursor.all()

    @staticmethod
    def find_by_id(group_id: str):
        statement = select(Group).where(Group.id == group_id)
        result = None
        try:
            result = db_session.exec(statement).first()
        except Exception as e:
            rich.print(e)
            rich.print(statement, group_id)
            exit()
        return result

    @staticmethod
    def find_by_label(label):
        statement = select(Group).where(Group.label == label)
        return db_session.exec(statement).first()

    @staticmethod
    def find_by_type(group_type: str):
        cursor = db_session.query(Group)
        return cursor.filter(Group.type == group_type).first()

    @staticmethod
    def add(group: "Group"):
        db_session.add(group)
        db_session.commit()

    @staticmethod
    def get_state():
        state = []
        for group in Group.index():
            state.append(group.dict())

        return state


class Schema(SQLModel, table=True):
    id: str = Field(default_factory=generate_uid, primary_key=True)
    label: str = Field(default="")
    environment: str = Field(default="dev")
    active: bool = Field(default=False)
    order: int = Field(default=-1)

    group_id: str = Field(default=None, foreign_key="group.id")
    group: Group = Relationship(back_populates="schemas")

    sessions: list['Session'] = Relationship(cascade_delete=True, back_populates="schema")
    ssh_groups: list['SSHGroup'] = Relationship(cascade_delete=True, back_populates="schema")

    @staticmethod
    def delete(schema: "Schema"):
        db_session.delete(schema)
        db_session.commit()

    @staticmethod
    def index(name=None, group_id=None):
        statement = select(Schema).order_by(Schema.label)

        if name:
            search = "%{}%".format(name)
            statement = statement.filter(Schema.label.like(search))

        if group_id:
            statement = statement.where(Schema.group_id == group_id)

        cursor = db_session.exec(statement)
        return cursor.all()

    @staticmethod
    def find_by_label(label: str):
        cursor = db_session.query(Schema)
        return cursor.filter(Schema.label == label).first()

    @staticmethod
    def find_by_id(schema_id: str):
        cursor = db_session.query(Schema)
        return cursor.filter(Schema.id == schema_id).first()

    def get_session(self, session_type: str, hostname: str, remote_port: int):
        for session in self.sessions:
            # print(session.dict())
            # print(hostname, remote_port)

            if (
                session.hostname == hostname
                and session.remote_port == remote_port
                and session_type == session.type
            ):
                # print(session.dict())
                return session

        # raise Exception(f"Session {hostname} and {remote_port} not found on {self.id}")

    def get_ssh_group(self, label: str):
        for group in self.ssh_groups:
            # print(session.dict())
            # print(hostname, remote_port)

            if group.label == label:
                # print(session.dict())
                return group

    @staticmethod
    def get_state():
        state = []
        for schema in Schema.index():
            schema_state = schema.dict()

            state.append(schema_state)

        return state


class SSHGroup(SQLModel, table=True):
    id: str = Field(default_factory=generate_uid, primary_key=True)
    label: str
    order: int = Field(default=-1)

    schema_id: str = Field(default=None, foreign_key="schema.id")
    schema: Schema = Relationship(back_populates="ssh_groups")

    @staticmethod
    def index(group_name=None) -> List["SSHGroup"]:
        cursor = db_session.query(SSHGroup)
        if group_name:
            search = "%{}%".format(group_name)
            cursor = cursor.filter(SSHGroup.label.like(search))

        return cursor.all()

    @staticmethod
    def find_by_id(group_id: str):
        cursor = db_session.query(SSHGroup)
        return cursor.filter(SSHGroup.id == group_id).first()

    @staticmethod
    def delete(group: "SSHGroup"):
        db_session.delete(group)
        db_session.commit()

    @staticmethod
    def get_state():
        state = []
        for group in SSHGroup.index():
            group_state = group.dict()

            state.append(group_state)

        return state


class Session(SQLModel, table=True):
    id: str = Field(default_factory=generate_uid, primary_key=True)
    label: str

    active: bool = Field(default=False)
    connected: bool = Field(default=False)

    hostname: str
    type: str = Field(default="local")
    remote_address: str = Field(default="127.0.0.1")
    remote_port: int = Field(default=0)
    local_address: str = Field(default="127.0.0.1")
    local_port: int = Field(default=0)
    local_port_dynamic: bool = Field(default=True)
    url_format: str = Field(default="http://{hostname}:{local_port}")
    auto_start: bool = Field(default=True)
    order: int = Field(default=-1)

    schema_id: str = Field(default=None, foreign_key="schema.id")
    schema: Schema = Relationship(back_populates="sessions")

    @staticmethod
    def clone(row):
        data = {}
        for column in row.__table__.columns:
            if column.name in ["id"]:
                continue

            data[column.name] = getattr(row, column.name)

        return Session(**data)

    @staticmethod
    def delete(session: "Session"):
        db_session.delete(session)
        db_session.commit()

    @staticmethod
    def find_by_id(session_id: str):
        statement = select(Session).where(Session.id == session_id)
        return db_session.exec(statement).first()

    @staticmethod
    def index(hostname=None, schema_id=None):
        statement = select(Session)

        if schema_id:
            statement = statement.where(Session.schema_id == schema_id)

        if hostname:
            search = "%{}%".format(hostname)
            statement = statement.filter(Session.hostname.like(search))

        cursor = db_session.exec(statement)
        return cursor.all()

    @computed_field(return_type=str)
    @property
    def cli_name(self) -> str:
        if self.schema and self.schema.group:
            return f"{self.schema.group.label}-{self.schema.label}".lower()
        return "Unnamed"

    @property
    def tmux_id(self) -> str:
        fields = [
            "pfm_session",
            "{schema_id}",
            "{hostname}",
            "{remote_address}",
            "{remote_port}",
            "{local_address}",
            "{local_port}",
            "{type}",
        ]

        data = {
            "schema_id": self.schema.id,
            "hostname": self.hostname,
            "remote_address": self.remote_address,
            "remote_port": self.remote_port,
            "local_address": self.local_address,
            "local_port": self.local_port,
            "type": self.type,
        }

        return "|".join(fields).format(**data).replace(".", "_")

    @property
    def url(self):
        if not self.url_format:
            return ""

        session_data = self.dict()

        return self.url_format.format(**session_data)

    @property
    def command(self):
        ssh_options = [
            "-o ExitOnForwardFailure=yes",
            "-o ServerAliveCountMax=3",
            "-o ServerAliveInterval=10",
        ]

        session_data = self.dict()

        session_data["tmux_id"] = self.tmux_id
        session_data["shell_command"] = "ping localhost"
        session_data["options"] = " ".join(ssh_options)

        if self.type == "remote":
            ssh = "ssh {options} -R {local_address}:{local_port}:{remote_address}:{remote_port} {hostname}"
        else:
            ssh = "ssh {options} -L {local_address}:{local_port}:{remote_address}:{remote_port} {hostname}"

        session_data["ssh_command"] = ssh.format(**session_data)

        # start_command = "screen -dmS '{name}' {ssh_command}  -- {shell_command}"
        start_command = "tmux new-session -d -s '{tmux_id}' '{ssh_command} -- {shell_command}'".format(
            **session_data
        )
        # inspect(session_definition)
        return start_command

    @staticmethod
    def get_state():
        state = []
        for session in Session.index():
            session_state = session.dict()
            session_state["connected"] = session.connected
            session_state["url"] = session.url
            state.append(session_state)
        return state


def init_database():
    # print("# Initialising database")
    label = "Ephemeral"
    SQLModel.metadata.create_all(engine)
    group = Group.find_by_label(label)
    if not group:
        # print(f"# Creating system group 'port_forward_manager-system'")
        group = Group(label=label, visible=False, type='system')
        schema = Schema(label="TunnelMate Ephemeral sessions")
        group.schemas.append(schema)
        Group.add(group)
        db_session.commit()


def reset_database():
    print("Resetting database")
    SQLModel.metadata.drop_all(engine)


db_session = get_session()
init_database()