FROM ubuntu/apache2

ENV DEBIAN_FRONTEND="noninteractive"
RUN apt-get update && apt-get install --yes \
    libapache2-mod-wsgi-py3 \
    python3-pip

RUN pip3 install defusedxml requests flask

COPY apache/horizonaggregator.conf /etc/apache2/sites-available/horizonaggregator.conf

RUN a2ensite horizonaggregator && \
    a2dissite 000-default && \
    service apache2 restart
