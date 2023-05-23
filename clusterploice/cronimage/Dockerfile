FROM python:3.9-slim


WORKDIR /app


COPY clusterpolice.py .


RUN pip install kubernetes


ENTRYPOINT ["python", "clusterpolice.py"]
