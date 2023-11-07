FROM python:3.10-slim

COPY ./ ./

RUN pip install -r ./requirements.txt

CMD ["python", "-m", "pytest", "-l", "--color=yes", "-p", "no:cacheprovider", "./tests"]