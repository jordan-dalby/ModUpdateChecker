FROM python:3.9

WORKDIR /app

RUN pip install discord.py aiosqlite requests html2text

COPY ./scripts .

ENV API_KEY=""
ENV BOT_TOKEN=""
ENV MOD_IDS=""
ENV CHANNEL_ID=""
ENV DEBUG_CHANNEL_ID=""
ENV ANNOUNCE_MESSAGES=""

CMD ["python", "./bot.py"]