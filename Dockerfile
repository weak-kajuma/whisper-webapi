FROM nvcr.io/nvidia/pytorch:22.02-py3

WORKDIR /app

COPY requirements.txt .
RUN apt update && apt install -y git ffmpeg
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install git+https://github.com/openai/whisper.git
COPY setup.py .
RUN python setup.py

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]