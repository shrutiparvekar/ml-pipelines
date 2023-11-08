from typing import AsyncGenerator, List, Union
import starlette

from transformers import pipeline

from ray import serve
from starlette.responses import StreamingResponse


@serve.deployment
class Translator_A:
    def __init__(self):
        self.model = pipeline("translation_en_to_de", model="t5-small")

    @serve.batch(max_batch_size=8, batch_wait_timeout_s=0.1)
    async def translate(self, text: List[str]) -> List[str]:
        res = []
        # Run inference
        for t in text:
            model_output = self.model(t)
            # Post-process output to return only the summary text
            res.append(model_output[0]["translation_text"])
        return res

    async def __call__(self, req: starlette.requests.Request) -> StreamingResponse:
        req = await req.json()
        text = self.translate(req['text'])
        return StreamingResponse(text, status_code=200, media_type="text/plain")


app = Translator_A.options(route_prefix="/translate").bind()
