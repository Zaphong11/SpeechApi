from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import Response
import soundfile as sf
from schema import speechSchema
from vieneu import Vieneu
import asyncio
import os
import uuid
import io

os.environ["HF_HUB_OFFLINE"] = "0"
app = FastAPI()
router = APIRouter()

tts = Vieneu(
    mode='turbo',
    model_name="pnnbao-ump/VieNeu-TTS"
)
SAMPLE_RATE = tts.sample_rate
audio_store = {}

async def delete_token(token: str, live_time: int = 60):
    await asyncio.sleep(live_time)
    if token in audio_store:
        del audio_store[token]
        print(f"Token {token} has been deleted")


@router.post("/tao-giong-noi")
async def tao_giong_noi(request: speechSchema.TextRequest, background_tasks: BackgroundTasks):
    audio_array = tts.infer(text=request.text_to_speech)

    virtual_file = io.BytesIO()
    sf.write(virtual_file, audio_array, samplerate = SAMPLE_RATE, format="WAV")
    audio_bytes = virtual_file.getvalue()

    token = str(uuid.uuid4())

    audio_store[token] = audio_bytes

    background_tasks.add_task(delete_token,token, 60)

    return {
        "status": "success",
        "token": token,
        "message": "Voice has been created successfully"
    }

@router.get("/nghe/{token}")
async def nghe_get(token: str):
    try:
        if token not in audio_store:
            raise HTTPException(status_code=404, detail="Token not found")
        audio_bytes = audio_store[token]

        # del audio_store[token]

        return Response(content=audio_bytes, media_type="audio/wav")
    except Exception as e:
        print(e)