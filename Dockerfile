FROM python:3.10

# Get supervisor and cron
RUN apt-get update \
 && apt-get install --no-install-recommends -y supervisor cron \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir -p /var/log/supervisor \
 && rm /etc/cron.daily/*

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY cron-update-endpoints /etc/cron.d/endpoints

COPY requirements.txt /fedcloud-dashboard/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fedcloud-dashboard/requirements.txt

COPY ./dashboard /fedcloud-dashboard/dashboard

WORKDIR /fedcloud-dashboard

EXPOSE 8000

CMD ["/usr/bin/supervisord"]
