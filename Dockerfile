FROM nvcr.io/nvidia/pytorch:22.02-py3

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt .
COPY setup.py .
RUN apt-get update && apt-get install -y ffmpeg git && pip install --no-cache-dir --upgrade -r /app/requirements.txt && pip install git+https://github.com/openai/whisper.git && python setup.py

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
