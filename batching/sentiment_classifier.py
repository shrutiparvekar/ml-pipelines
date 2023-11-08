import starlette

from transformers import pipeline

from ray import serve
from ray.serve.handle import DeploymentHandle


from germansentiment import SentimentModel


class TextClassify_A:
    def __init__(self):
        # Load model
        self.model = SentimentModel()
    
    @serve.batch(max_batch_size=8, batch_wait_timeout_s=0.1)
    def classify(self, text: List[str]) -> List[str]:
        res = []
        # Run inference
        for t in text:
            x = self.model.predict_sentiment(t)
            res.append(x[0])
        return res

    async def __call__(self, http_request: starlette.requests.Request) -> StreamingResponse:
        req: str = await http_request.json()
        text = req["text"]
        sentiment = self.classify(text)
        return StreamingResponse(sentiment, status_code=200, media_type="text/plain")

app = TextClassify_A.options(route_prefix="/classify").bind()
