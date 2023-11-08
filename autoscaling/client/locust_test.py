from locust import HttpUser, task, between, events, constant_throughput, constant, constant_pacing
import time
import random

class MyUser(HttpUser):
    wait_time = constant(0)
    # min_wait = 1000
    # max_wait = 3000
    host = "http://localhost:8000"
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None

    def on_start(self):
        with open("./input/input.txt", "r") as f:
            self.lines = f.readlines()
    # def tick(self):
    #     run_time = self.get_run_time()

    #     if run_time < self.time_limit:
    #         # User count rounded to nearest hundred.
    #         return (5, 5)

    #     return None
    @task
    def perform_task(self):
        translation_url = "/summarize"
        text = random.choice(self.lines).strip()
        # response = requests.post(translation_url, json={"text": text, "should_translate": True})

        response = self.client.post(
            translation_url,
            json={"text": text, "should_translate": True}
        )
        output_text = ""
        if response.status_code == 200:
            translated_text = response.text
            output_text = f"Original: {text}\nTranslation: {translated_text}\n----\n"
        else:
            output_text = f"Error translating text: {text}\n"

        # Write the response to an output file
        with open("./output/output.txt", "a") as output_file:
            output_file.write(output_text + "\n")

    # def on_stop(self):
    #     elapsed_time = time.time() - self.start_time
    #     if elapsed_time >= 600:  # Stop the test after 10mins
    #         events.request_success.fire(
    #             request_type="stop",
    #             name="/stop",
    #             response_time=0,
    #             response_length=0,
    #         )