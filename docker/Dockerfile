FROM ubuntu/apache2

RUN apt-get update && apt-get install --yes \
    libapache2-mod-wsgi-py3 \
    python3-pip && \
    apt-get clean

RUN pip3 install defusedxml requests flask && \
    pip3 cache purge

COPY horizonaggregator.conf /etc/apache2/sites-available/horizonaggregator.conf

RUN a2dissite 000-default && \
    a2ensite horizonaggregator && \
    service apache2 restart
