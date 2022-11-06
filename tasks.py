import datetime
from datetime import timedelta

from sqlmodel import select, Session, SQLModel, cast, Date
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from main import Track, engine

session = Session(engine)


SQLModel.metadata.create_all(engine)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    statement = select(Track).where(Track.started_at.cast(Date) == today)
    results = session.exec(statement)
    user = results.first()
    if not user:
        started_at = datetime.datetime.now()
        user = Track(started_at=started_at)
        session.add(user)
        session.commit()
        await update.effective_message.reply_text(
            f'Am inceput sa logez orele lucrate cu success, ora: {(started_at + timedelta(hours=2)).strftime("%H:%M:%S")}')
    elif not user.ended_at:
        await update.effective_message.reply_text(
            f'Nu ai inchis logare orelor pentru ora: {(user.started_at + timedelta(hours=2)).strftime("%H:%M:%S")}')
    else:
        started_at = datetime.datetime.now()
        track = Track(started_at=datetime.datetime.now())
        session.add(track)
        session.commit()
        await update.effective_message.reply_text(
            f'Am inceput sa logez orele lucrate cu success, ora: {(started_at + timedelta(hours=2)).strftime("%H:%M:%S")}')


async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.date.today()
    statement = select(Track).where(Track.started_at.cast(Date) == today, Track.ended_at == None)
    results = session.exec(statement)
    user = results.first()
    if user:
        user.ended_at = datetime.datetime.now()
        session.add(user)
        session.commit()
        worked_time = (user.ended_at - user.started_at).total_seconds() / 60 / 60
        results = session.exec("""
            select Sum(track.ended_at - track.started_at)
            from track
            """)
        result = results.first()
        total = result.sum.total_seconds() / 60 / 60 if result.sum else 0
        await update.effective_message.reply_text(
            f'Bravo! Ai incheiat studiul cu succes, azi ai lucrat {worked_time:.2f} mai ai inca {(100 - total):.2f} pina indeplinesti scopul de 100 ore studiate')
    if not user:
        await update.effective_message.reply_text(
            f'Nu ai inceput studiul azi, pentru a incepe lucrul scrie /start_study')


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results = session.exec("""
        select Sum(track.ended_at - track.started_at)
        from track
        where Date(started_at) = Date(now());
    """)
    result = results.first()
    today = result.sum.total_seconds() / 60 / 60 if result.sum else 0
    results = session.exec("""
        select Sum(track.ended_at - track.started_at)
        from track
        where Date(started_at) BETWEEN Date(now())- interval '1 week' and Date(now());
    """)
    result = results.first()
    week = result.sum.total_seconds() / 60 / 60 if result.sum else 0
    results = session.exec("""
        select Sum(track.ended_at - track.started_at)
        from track
        where Date(started_at) BETWEEN Date(now())- interval '1 month' and Date(now());
    """)
    result = results.first()
    month = result.sum.total_seconds() / 60 / 60 if result.sum else 0
    results = session.exec("""
        select Sum(track.ended_at - track.started_at)
        from track
        """)
    result = results.first()
    total = result.sum.total_seconds() / 60 / 60 if result.sum else 0
    await update.effective_message.reply_text(
        f'Ai lucrat azi {today:.2f}h\nSaptamina aceasta {week:.2f}h\nLuna aceasta{month:.2f}h\nTotal ai lucrat {total:.2f}')


def main():
    application = ApplicationBuilder().token("5681967080:AAGMkotm9yFcoaR5gjdEewV9Pv5yCb36RHI").build()
    application.add_handler(CommandHandler("start_study", start))
    application.add_handler(CommandHandler("finish_study", finish))
    application.add_handler(CommandHandler("statistics", stats))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

dsadsa
dsasdas
dasd
asd
asd
asdas

main()
