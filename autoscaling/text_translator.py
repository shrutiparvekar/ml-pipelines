import starlette

from transformers import pipeline

from ray import serve

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
class Translator_A:
    def __init__(self):
        self.model = pipeline("translation_en_to_de", model="t5-small")

    def translate(self, text: str) -> str:
        return self.model(text)[0]["translation_text"]

    async def __call__(self, req: starlette.requests.Request) -> str:
        req = await req.json()
        translated_text = self.translate(req['text'])
        return translated_text

app = Translator_A.options(route_prefix="/translate").bind()
