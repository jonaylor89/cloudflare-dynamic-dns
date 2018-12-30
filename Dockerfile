FROM python:3.7.1-alpine
COPY . /project
RUN pip install CloudFlare
CMD python -u /project/set-dns.py
