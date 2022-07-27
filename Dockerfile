FROM python:3.10

RUN apt-get update && apt-get install -y supervisor cron

RUN mkdir -p /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY cron-update-endpoints /etc/cron.d/endpoints

RUN rm /etc/cron.daily/*

COPY requirements.txt /fedcloud-dashboard/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fedcloud-dashboard/requirements.txt

COPY ./dashboard /fedcloud-dashboard/dashboard

WORKDIR /fedcloud-dashboard

EXPOSE 8000

CMD ["/usr/bin/supervisord"]
