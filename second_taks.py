from telegram import Bot

from sqlmodel import SQLModel, create_engine, Session, select, Field

import schedule
import time


sqlite_url = f"postgresql://point:point@db:5438/point"
engine = create_engine(sqlite_url, echo=True)
session = Session(engine)
bot = Bot(token="5681967080:AAGMkotm9yFcoaR5gjdEewV9Pv5yCb36RHI")


def send_message():
    results = session.exec("""
         select Sum(track.ended_at - track.started_at)
         from track
         """)
    result = results.first()
    total = result.sum.total_seconds() / 60 / 60 if result.sum else 0
    import asyncio
    loop = asyncio.get_event_loop()
    coroutine = bot.send_message(744570127,
                                 f"Davai brat!!!!! ne zdavaisea, o sa se primeasca, mai inca {100 - total:.2f} pina la scopul tau")
    loop.run_until_complete(coroutine)


schedule.every().day.at("05:00").do(send_message)  # timezone utz (chisinau timezone is 08:00)
while True:
    send_message()
    schedule.run_pending()
    time.sleep(1)
