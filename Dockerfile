FROM python:3.9

WORKDIR /app

RUN pip install discord.py aiosqlite requests html2text

COPY ./scripts .

CMD ["python", "./bot.py"]