from fastapi import FastAPI, File, UploadFile
import whisper
import asyncio
import shutil
import os
import sqlite3
import time

app = FastAPI()
model = whisper.load_model("medium", device="cuda")

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file:
        filename = file.filename
        fileobj = file.file
        upload_dir = open(os.path.join("./audio", filename),'wb+')
        shutil.copyfileobj(fileobj, upload_dir)
        upload_dir.close()
        conn = sqlite3.connect("filename")
        db = conn.cursor()
        db.execute('INSERT INTO filename (filename) values("'+ filename +'")')
        conn.commit()
        conn.close()
        return {"filename": filename}
    return {"Error": "アップロードファイルが見つかりません。"}

@app.get("/upload/{filename}")
async def getText(filename: str):
    conn = sqlite3.connect("filename")
    db = conn.cursor()
    db.execute('select * from filename where filename="'+ filename +'"')
    data = db.fetchall()
    if data:
        if len(data[0]) == 3:
            return {"filename": filename, "text": data[0][2]}
        else:
            return {"Error": "そのファイルは現在処理中です"}
    else:
        return {"Error": "そのファイルは見つかりません"}

def transcribe(arg):
    while True:
        conn = sqlite3.connect("filename")
        db = conn.cursor()
        if db.execute('SELECT * FROM filename WHERE text is null').fetchall():
            data = db.execute('SELECT * FROM filename WHERE text is null').fetchall()[0]
            id = str(data[0])
            filename = data[1]
            result = model.transcribe("./audio/" + filename)
            db.execute('UPDATE filename SET text = "'+ result["text"] +'" where id = "'+ id +'"')
            conn.commit()
            conn.close()
        else:
            time.sleep(5)

asyncio.get_event_loop().run_in_executor(None, transcribe, None)