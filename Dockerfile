FROM python:3-alpine

WORKDIR /usr/bin/getnotified

COPY requirements.txt ./
COPY getnotified ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "/usr/bin/getnotified"]

