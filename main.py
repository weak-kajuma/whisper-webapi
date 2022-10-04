from fastapi import FastAPI, File, UploadFile
import whisper
import asyncio
import shutil
import os

app = FastAPI()
model = whisper.load_model("medium", device="cpu")

@app.get("/hello")
async def hello():
    return {"message": "hello"}

@app.post("/whisper")
async def transcript(file: UploadFile = File(...)):
    if file:
        filename = file.filename
        fileobj = file.file
        upload_dir = open(os.path.join("./wav", filename),'wb+')
        shutil.copyfileobj(fileobj, upload_dir)
        upload_dir.close()
        print("TASK:     Upload succeed[" + filename + "]")
        result = await asyncio.get_event_loop().run_in_executor(None, model.transcribe, "./wav/" + filename)
        print("TASK:     " + filename + ": " + result["text"])
        return {"filename": filename, "result": result}
    return {"Error": "アップロードファイルが見つかりません。"}
