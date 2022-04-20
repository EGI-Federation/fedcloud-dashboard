FROM python:3.10

COPY requirements.txt /fedcloud-dashboard/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /fedcloud-dashboard/requirements.txt

COPY ./dashboard /fedcloud-dashboard/dashboard

WORKDIR /fedcloud-dashboard

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dashboard.main:app"]
