FROM python:3.10

# Get cron
# Do not get picky on exact cron version so ignore DL3008
# hadolint ignore=DL3008
RUN apt-get update \
 && apt-get install --no-install-recommends -y cron \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && rm /etc/cron.daily/*

COPY cron-update-endpoints /etc/cron.d/endpoints

COPY requirements.txt /fedcloud-dashboard/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fedcloud-dashboard/requirements.txt

COPY ./dashboard /fedcloud-dashboard/dashboard

WORKDIR /fedcloud-dashboard

CMD ["cron", "-f"]
