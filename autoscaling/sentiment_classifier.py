import starlette

from transformers import pipeline

from ray import serve
from ray.serve.handle import DeploymentHandle


from germansentiment import SentimentModel


@serve.deployment(
    # ray_actor_options={"num_cpus": 10},
    max_concurrent_queries=3,
    autoscaling_config={
        "target_num_ongoing_requests_per_replica": 1,
        "min_replicas": 2,
        "initial_replicas": 2,
        "max_replicas": 200
    }
)
class TextClassify_A:
    def __init__(self):
        # Load model
        self.model = SentimentModel()

    def classify(self, text: str) -> str:
        # sentence = Sentence(text)
        x = self.model.predict_sentiment(text)
        return x[0]

    async def __call__(self, http_request: starlette.requests.Request) -> str:
        req: str = await http_request.json()
        text = req["text"]
        sentiment = self.classify(text)
        return sentiment

app = TextClassify_A.options(route_prefix="/classify").bind()
