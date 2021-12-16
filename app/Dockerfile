FROM python:3.9

WORKDIR /usr/src/app

RUN apt update &&\
  apt install -y netcat &&\
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
ENV PORT=8000

ENTRYPOINT [ "./entrypoint.sh" ]