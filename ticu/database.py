



import discord
import sqlalchemy as sa
import sqlalchemy.orm as sao

import ticu.config
import ticu.utils


Base = sao.declarative_base()

class Server(Base):
  __tablename__ = "server"

  id = sa.Column(sa.Integer, primary_key=True)
  name = sa.Column(sa.String(64))
  members = sao.relationship("Member", secondary="server_member", back_populates=False)

  def __repr__(self):
    return f"<Server(name='{self.name}')>"

class Channel(Base):
  __tablename__ = "channel"

  id = sa.Column(sa.Integer, primary_key=True)
  name = sa.Column(sa.String(64))

  def __repr__(self):
    return f"<Channel(name='{self.name}')>"

class Role(Base):
  __tablename__ = "role"

  id = sa.Column(sa.Integer, primary_key=True)
  discord_id = sa.Column(sa.Integer)
  name = sa.Column(sa.String(64))
  members = sao.relationship("Member", secondary="member_role", back_populates=False)

  def __repr__(self):
    return f"<Role(pseudo='{self.pseudo}')>"

class Member(Base):
  __tablename__ = "member"

  id = sa.Column(sa.Integer, primary_key=True)
  auto_kick = sa.Column(sa.Boolean, default=False)
  auto_ban = sa.Column(sa.Boolean, default=False)
  banned = sa.Column(sa.Boolean, default=False)
  kicked = sa.Column(sa.Boolean, default=False)
  notification = sa.Column(sa.Boolean)
  servers = sao.relationship("Server", secondary="server_member")
  roles = sao.relationship("Role", secondary="member_role")

  def __repr__(self):
    return f"<Member(id='{self.id}')>"

class ServerMember(Base):
  __tablename__ = "server_member"

  id = sa.Column(sa.Integer, primary_key=True)
  server_id = sa.Column(sa.Integer, sa.schema.ForeignKey("server.id"))
  member_id = sa.Column(sa.Integer, sa.schema.ForeignKey("member.id"))

class MemberRole(Base):
  __tablename__ = "member_role"

  id = sa.Column(sa.Integer, primary_key=True)
  role_id = sa.Column(sa.Integer, sa.schema.ForeignKey("role.id"))
  member_id = sa.Column(sa.Integer, sa.schema.ForeignKey("member.id"))

def get_or_create(session, model, **kwargs):
  obj = session.query(model).filter_by(**kwargs).first()
  if obj:
    return obj, False
  obj = model(**kwargs)
  session.add(obj)
  session.commit()
  return obj, True

def has_member(member:discord.Member):
  with Session() as session:
    return get_member(member) != None

def get_member(member:discord.Member, session=None):
  if session is None:
    with Session() as session:
      return get_member(member, session)
  return _query_member(member, session).first()

def _query_member(member:discord.Member, session):
  query = session.query(Member)
  query = query.filter(
    Member.id == member.id
  )
  query = query.join((Server, Member.servers))
  query = query.filter(
    Member.id == member.id,
    Server.id == member.guild.id
  )
  return query

def has_server(server:discord.Guild):
  return get_server(server) != None

def get_server(server:discord.Guild, session=None):
  if session is None:
    with Session() as session:
      return get_server(server, session)
  ## would it be better to do a `session.get(Server, server.id)` ??
  return _query_server(server, session).first()

def _query_server(server:discord.Guild, session):
  query = session.query(Server)
  query = query.filter(Server.id == server.id)
  return query

def has_role(role:discord.Role):
  return get_role(role) != None

def get_role(role:discord.Role, session=None):
  if session is None:
    with Session() as session:
      return get_role(role, session)
  ## would it be better to do a `session.get(role, role.id)` ??
  return _query_role(role, session).first()

def _query_role(role:discord.Role, session):
  query = session.query(Role)
  query = query.filter(Role.id == role.id)
  return query

def has_auto_ban(member:discord.Member):
  if (member := get_member(member)) is None:
    return False
  return member.auto_ban

def has_auto_kick(member:discord.Member):
  if (member := get_member(member)) is None:
    return False
  return member.auto_kick

def create_member(member:discord.Member, session=None):
  if session is None:
    with Session() as session:
      return create_member(member, session)
  if not isinstance(member, discord.Member):
    raise TypeError(
      f"Bad member type: expected discord.Member instance,"
      f" got {type(member)}"
    )
  server = member.guild
  database_logger.debug(f"Creating member for id={member.id}...")
  if has_member(member):
    database_logger.debug(f"Member {member.id} already exists.")
    return get_member(member, session)
  db_member, created = get_or_create(session, Member, id=member.id)
  if not has_server(server):
    database_logger.debug(f"Member's server {server.id} does not exist yet.")
    db_server = create_server(server, session)
  else:
    db_server = get_server(server, session)
  db_member.servers.append(db_server)
  database_logger.debug(f"Member added to server {server.id}.")
  session.add(db_member)
  session.commit()
  database_logger.debug(f"Member created.")
  return db_member

def assign_role(member:discord.Member, role:discord.Role, session):
  db_member = create_member(member, session)
  db_role = create_role(role, session)
  if db_role not in db_member.roles:
    db_member.roles.append(db_role)
  session.commit()

def remove_role(member:discord.Member, role:discord.Role, session):
  db_member = create_member(member, session)
  db_role = create_role(role, session)
  if db_role in db_member.roles:
    db_member.roles.remove(db_role)
  session.commit()

def create_server(server:discord.Guild, session=None):
  if session is None:
    with Session() as session:
      return create_server(server, session)
  if not isinstance(server, discord.Guild):
    raise TypeError(
      f"Bad server type: expected discord.Guild instance,"
      f" got {type(server)}"
    )
  database_logger.debug(f"Creating server for id={server.id}...")
  if has_server(server):
    database_logger.debug(f"Server {server.id} already exists.")
    return get_server(server, session)
  db_server = Server(id=server.id)
  session.add(db_server)
  session.commit()
  database_logger.debug(f"Server created.")
  return db_server

def create_role(role:discord.Role, session=None):
  if session is None:
    with Session() as session:
      return create_role(role, session)
  if not isinstance(role, discord.Role):
    raise TypeError(
      f"Bad role type: expected discord.Role instance,"
      f" got {type(role)}"
    )
  database_logger.debug(f"Creating role for id={role.id}...")
  if has_role(role):
    database_logger.debug(f"role {role.id} already exists.")
    return get_role(role, session)
  db_role = Role(id=role.id)
  session.add(db_role)
  session.commit()
  database_logger.debug(f"Role created.")
  return db_role



database_logger = ticu.utils.get_logger(
  __name__,
  filename=f"logs/database.log",
  noprint=True
)

app = sa.create_engine(
  f"sqlite:///{ticu.config.SQLITE_PATH}",
  echo=ticu.config.DEBUG_DATABASE
)

Session = sao.sessionmaker(bind=app)
Base.metadata.drop_all(app)
Base.metadata.create_all(app)

__all__ = [
  "app",
  "Session",
  "Server",
  "Channel",
  "Role",
  "Member",
]

