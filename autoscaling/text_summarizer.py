import starlette

from transformers import pipeline

from ray import serve
from ray.serve.handle import DeploymentHandle

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
class Summarizer_A:
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
        if req["should_translate"] is True:
            #translator handle
            handle: DeploymentHandle = serve.get_app_handle("translator")
            translated_text = await handle.translate.remote(summary)
            #sentiment analysis
            classifyhandle: DeploymentHandle = serve.get_app_handle("classify")
            res = await classifyhandle.classify.remote(translated_text)
            return translated_text + " sentiment: " + res

        return summary


app = Summarizer_A.options(route_prefix="/summarize").bind()
