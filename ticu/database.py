

import sqlalchemy
import sqlalchemy.orm


import ticu.config
import ticu.utils


Base = sqlalchemy.orm.declarative_base()


class TipouiChannel(Base):
  __tablename__ = "channel"

  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  discord_id = sqlalchemy.Column(sqlalchemy.Integer)
  name = sqlalchemy.Column(sqlalchemy.String(64))

  def __repr__(self):
    return f"<TiPouiChannel(pseudo='{self.pseudo}')>"


class TipouiRole(Base):
  __tablename__ = "role"

  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  discord_id = sqlalchemy.Column(sqlalchemy.Integer)
  name = sqlalchemy.Column(sqlalchemy.String(64))

  def __repr__(self):
    return f"<TipouiRole(pseudo='{self.pseudo}')>"


class TipouiMember(Base):
  __tablename__ = "member"

  id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
  discord_id = sqlalchemy.Column(sqlalchemy.Integer)
  auto_kick = sqlalchemy.Column(sqlalchemy.Boolean)
  auto_ban = sqlalchemy.Column(sqlalchemy.Boolean)
  banned = sqlalchemy.Column(sqlalchemy.Boolean)
  kicked = sqlalchemy.Column(sqlalchemy.Boolean)
  notification = sqlalchemy.Column(sqlalchemy.Boolean)

  def __repr__(self):
    return f"<TiPouiMember(pseudo='{self.pseudo}')>"


database_logger = ticu.utils.get_logger(
  __name__,
  filename=f"logs/database.log",
  noprint=True
)

app = sqlalchemy.create_engine(
  f"sqlite:///{ticu.config.SQLITE_PATH}",
  echo=True
)

Session = sqlalchemy.orm.sessionmaker(bind=app)

__all__ = [
  "app",
  "Session",
  "TipouiChannel",
  "TipouiRole",
  "TipouiMember",
]

