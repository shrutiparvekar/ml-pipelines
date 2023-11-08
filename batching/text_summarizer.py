from typing import AsyncGenerator, List, Union
import starlette
import requests


from transformers import pipeline

from ray import serve
from ray.serve.handle import DeploymentHandle
from starlette.responses import StreamingResponse

@serve.deployment
class Summarizer_A:
    def __init__(self):
        # Load model
        self.model = pipeline("summarization", model="t5-small")

    @serve.batch(max_batch_size=8, batch_wait_timeout_s=0.1)
    async def summarize(self, text: List[str]) -> AsyncGenerator[List[Union[str, StopIteration]], None]:
        res = []
        # Run inference
        for t in text:
            model_output = self.model(t, min_length=5, max_length=15)
            # Post-process output to return only the summary text
            res.append(model_output[0]["summary_text"])
        print('returning: ', res)
        yield res

    async def __call__(self, http_request: starlette.requests.Request) -> StreamingResponse:
        translation_url = "http://localhost:8000/translate"
        print('printing: ', http_request)
        req: str = await http_request.json()
        print('translating: ', req)
        english_text = req["text"]
        summary = self.summarize(english_text)
        print('summary is ', summary)

        if req["should_translate"] is True:
            handle: DeploymentHandle = serve.get_app_handle("translator")
            sentimentHandle: DeploymentHandle = serve.get_app_handle("classify")
            res = []
            async for item_list in summary:
                if item_list is StopIteration:
                    break
                print('string to be translated is: ', item_list)
                translated_text = await handle.translate.remote(item_list)
                sentiment = await sentimentHandle.classify.remote(translated_text)
                res.append(translated_text + " sentiment " + sentiment)
            print('result is ', res)
            return res
        return StreamingResponse(summary, status_code=200, media_type="text/plain")


app = Summarizer_A.options(route_prefix="/summarize").bind()
