from fastapi import FastAPI
from routers import textToSpeech
app = FastAPI()

app.include_router(textToSpeech.router, prefix="/v1/text-to-speech")
