FROM public.ecr.aws/lambda/python:3.11.2023.11.18.02

RUN  pip3 install httpx==0.25.2 beautifulsoup4==4.12.3 python-telegram-bot==20.7 --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}/app.py
COPY parse_olx.py ${LAMBDA_TASK_ROOT}/parse_olx.py
COPY ai_parser.py ${LAMBDA_TASK_ROOT}/ai_parser.py
COPY bot_telegram.py ${LAMBDA_TASK_ROOT}/bot_telegram.py
COPY read_config.py ${LAMBDA_TASK_ROOT}/read_config.py
COPY persistence.py ${LAMBDA_TASK_ROOT}/persistence.py
COPY config.json ${LAMBDA_TASK_ROOT}/config.json

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
