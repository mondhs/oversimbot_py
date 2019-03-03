FROM python:3
ADD oversimbot /app/oversimbot
ADD target /app/target
WORKDIR /app
CMD [ "python", "-m", "oversimbot.chatbot_engine" ]
