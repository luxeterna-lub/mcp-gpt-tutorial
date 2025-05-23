# server.py  ─ FastAPI で Slack に転送するだけの最小構成
from fastapi import FastAPI
from pydantic import BaseModel
import os, httpx

app = FastAPI()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

class SlackReq(BaseModel):
    text: str

@app.post("/slack/send")
async def slack_send(req: SlackReq):
    async with httpx.AsyncClient() as client:
        await client.post(SLACK_WEBHOOK_URL, json={"text": req.text})
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}
