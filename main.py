import datetime
from typing import Optional
from telegram import Bot

from sqlmodel import SQLModel, create_engine, Session, select, Field



class Track(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    started_at: datetime.datetime
    ended_at: Optional[datetime.datetime]


sqlite_url = f"postgresql://point:point@db:5438/point"

engine = create_engine(sqlite_url, echo=True)
session = Session(engine)
test = 744570127
bot = Bot(token="5681967080:AAGMkotm9yFcoaR5gjdEewV9Pv5yCb36RHI")

