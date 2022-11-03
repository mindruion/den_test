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
    results = session.exec("""
        select Sum(track.ended_at - track.started_at)
        from track
        where Date(started_at) BETWEEN Date(now())- interval '1 day' and Date(now());
    """)
    result = results.first()
    yesterday = result.sum.total_seconds() / 60 / 60 if result.sum else 0
    import asyncio
    loop = asyncio.get_event_loop()
    if yesterday:
        message = f"Krasava brat!!!!! ne zdavaisea, o sa se primeasca, ieri ai lucrat {yesterday:2.f} mai numai {100 - total:.2f} pina la scopul tau"
    else:
        message = f"Brat ce za huinea??!!!!! ne zdavaisea, o sa se primeasca, ieri ai lucrat {yesterday:2.f} mai tuhma {100 - total:.2f} pina la scopul tau"
    coroutine = bot.send_message(744570127,
                                 message)
    loop.run_until_complete(coroutine)


schedule.every().day.at("05:00").do(send_message)  # timezone utz (chisinau timezone is 08:00)
while True:
    schedule.run_pending()
    time.sleep(1)
