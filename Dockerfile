FROM  python:3.9-slim-buster
WORKDIR /apiTest
COPY requirements.txt /apiTest/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /apiTest/
CMD ["python3", "main.py", "--name", "iac"]