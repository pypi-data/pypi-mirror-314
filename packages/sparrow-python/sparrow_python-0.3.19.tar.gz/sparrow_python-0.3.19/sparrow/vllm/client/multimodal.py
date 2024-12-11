from openai import OpenAI
import asyncio
from sparrow.vllm.client.image_processor import messages_preprocess
from sparrow import ConcurrentRequester


requester = ConcurrentRequester(
    concurrency_limit=5,
)
# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

models = client.models.list()
print(models)
model = models.data[0].id
print(model)

# Single-image input inference
def run_image() -> None:
    # vllm 启动方式： vllm serve Qwen/Qwen2-VL-2B-Instruct-GPTQ-Int4 --limit-mm-per-prompt image=16 这里-limit-mm-per-prompt 默认image 是1,默认情况下不支持多图

    ## Use image url in the payload
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "这两张图有何不同？"},
            {"type": "image_url", "image_url": {"url": f"{image_url}"}},
            {"type": "image_url", "image_url": {"url": f"{image_url}"}},
        ],
    }]
    messages = asyncio.run(messages_preprocess(messages))
    result, _ = asyncio.run(requester.process_requests(
        request_params=[
            {
                'json': {
                    "model": model,
                    "messages": messages
                },
                'headers': {'Content-Type': 'application/json', 'Authorization': f"Bearer {openai_api_key}"}
            } for _ in range(1)
        ],
        url="http://localhost:8000/v1/chat/completions",
        method="POST",
    ))

    print("Chat completion output from image url:", result)



run_image()