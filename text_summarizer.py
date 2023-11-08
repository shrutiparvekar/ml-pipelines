import starlette

from transformers import pipeline

from ray import serve
from ray.serve.handle import DeploymentHandle

@serve.deployment
class Summarizer:
    def __init__(self):
        # Load model
        self.model = pipeline("summarization", model="t5-small")

    def summarize(self, text: str) -> str:
        # Run inference
        model_output = self.model(text, min_length=5, max_length=15)

        # Post-process output to return only the summary text
        summary = model_output[0]["summary_text"]

        return summary

    async def __call__(self, http_request: starlette.requests.Request) -> str:
        req: str = await http_request.json()
        english_text = req["text"]
        summary = self.summarize(english_text)
        print('translating: ', req)
        if req["should_translate"] is True:
            handle: DeploymentHandle = serve.get_app_handle("app2")
            # json={"text": summary}
            # print('input is ', json)
            return await handle.translate.remote(summary)

        return summary


app = Summarizer.options(route_prefix="/summarize").bind()
