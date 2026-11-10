FROM python:3.12-slim
WORKDIR /app
COPY q6g/ ./q6g/
COPY main.py README.md ./
RUN useradd -m q6g && chown -R q6g:q6g /app
USER q6g
ENTRYPOINT ["python", "main.py"]
CMD ["demo"]
