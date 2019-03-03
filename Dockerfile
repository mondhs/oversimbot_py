FROM python:3
ADD oversimbot /app/oversimbot
WORKDIR /app
CMD [ "python", "-m", "oversimbot.chatbot_engine" ]
