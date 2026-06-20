'''
RenameBot
© Mrvishal2k2
'''
import threading
from sqlalchemy import create_engine, Column, Integer, BigInteger
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
from Bot.config import Config


class Base(DeclarativeBase):
    pass


class Thumbnail(Base):
    __tablename__ = "thumbnail"
    id = Column(BigInteger, primary_key=True)
    msg_id = Column(Integer, nullable=False)

    def __init__(self, id: int, msg_id: int):
        self.id = id
        self.msg_id = msg_id


def _start() -> scoped_session:
    engine = create_engine(Config.DB_URI, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


SESSION = _start()
_LOCK = threading.RLock()


async def save_thumb(user_id: int, msg_id: int) -> None:
    with _LOCK:
        existing = SESSION.get(Thumbnail, user_id)
        if existing:
            existing.msg_id = msg_id
        else:
            SESSION.add(Thumbnail(user_id, msg_id))
        SESSION.commit()


async def delete_thumb(user_id: int) -> None:
    with _LOCK:
        row = SESSION.get(Thumbnail, user_id)
        if row:
            SESSION.delete(row)
            SESSION.commit()


async def get_thumb(user_id: int) -> Thumbnail | None:
    return SESSION.get(Thumbnail, user_id)
