FROM python:2.7

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /output
VOLUME /output

COPY . .
RUN python setup.py install