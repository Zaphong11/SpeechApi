from pydantic import BaseModel

class TextRequest(BaseModel):
    text_to_speech: str