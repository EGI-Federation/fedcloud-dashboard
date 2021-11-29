FROM python:3.9

COPY requirements.txt /dashboard/requirements.txt

COPY dashboard /dashboard

RUN pip install --no-cache-dir --upgrade -r /dashboard/requirements.txt

COPY ./dashboard /dashboard/dashboard

WORKDIR /dashboard

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dashboard.main:app"]
