FROM python:3.12-alpine
WORKDIR /ppc
COPY server.py /ppc/server.py
CMD ["python", "server.py"]