# server.py ─ FastAPI で Slack に転送する最小構成
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi   # ← 追加
from pydantic import BaseModel
import os, httpx

app = FastAPI()

# OpenAPI を公開（GPTS のアクション取り込み用）
@app.get("/openapi.json", include_in_schema=False)
def custom_openapi():
    return get_openapi(
        title="Slack Notifier",
        version="1.0.0",
        routes=app.routes
    )

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
