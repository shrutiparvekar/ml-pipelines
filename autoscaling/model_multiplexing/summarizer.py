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
        "min_replicas": 0,
        "initial_replicas": 0,
        "max_replicas": 200
    }
)
class Summarizer:
    def __init__(self, translator, classifier):
        self.translator: DeploymentHandle = translator.options(
            use_new_handle_api=True,
        )
        self.classifier = classifier.options(
            use_new_handle_api=True,
        )
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
        # if req["should_translate"] is True:
        print('getting in here')

        translated_text = await self.translator.translate.remote(summary)
        res = await self.classifier.classify.remote(translated_text)
        print('sentiment derived: ', res)
        return translated_text + " sentiment: " + res

        return summary

@serve.deployment(
    # ray_actor_options={"num_cpus": 10},
    max_concurrent_queries=3,
    autoscaling_config={
        "target_num_ongoing_requests_per_replica": 1,
        "min_replicas": 0,
        "initial_replicas": 0,
        "max_replicas": 200
    }
)
class Translator:
    def __init__(self):
        self.model = pipeline("translation_en_to_de", model="t5-small")

    def translate(self, text: str) -> str:
        return self.model(text)[0]["translation_text"]

@serve.deployment(
    # ray_actor_options={"num_cpus": 10},
    max_concurrent_queries=3,
    autoscaling_config={
        "target_num_ongoing_requests_per_replica": 1,
        "min_replicas": 0,
        "initial_replicas": 0,
        "max_replicas": 200
    }
)
class TextClassify:
    def __init__(self):
        # Load model
        # self.model = pipeline("classification", model="de-offensive-language")
        self.model = SentimentModel()

    def classify(self, text: str) -> str:
        # sentence = Sentence(text)
        x = self.model.predict_sentiment(text)
        # print sentence with predicted labels
        print('x is ', x)
        # print('Sentence above is: ', sentence.labels)
        return x[0]

translator = Translator.bind()
classifier = TextClassify.bind()
lang_summarizer = Summarizer.bind(translator, classifier)
