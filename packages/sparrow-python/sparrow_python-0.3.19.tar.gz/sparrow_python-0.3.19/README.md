# sparrow-python
[![image](https://img.shields.io/badge/Pypi-0.1.7-green.svg)](https://pypi.org/project/sparrow-python)
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-kunyuan-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)


-------------------------
## TODO
- [ ]  from mod_base.cv.image.image_processor import messages_preprocess 添加是否对网络url替换为base64的控制；添加对video切帧的支持

识别下面链接的滚动截图：  
https://sjh.baidu.com/site/dzfmws.cn/da721a31-476d-42ed-aad1-81c2dc3a66a3 


vllm 异步推理示例：

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.sampling_params import SamplingParams
import torch

# Define request data model
class RequestData(BaseModel):
    prompts: List[str]
    max_tokens: int = 2048
    temperature: float = 0.7

# Initialize FastAPI app
app = FastAPI()

# Determine device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize AsyncLLMEngine
engine_args = AsyncEngineArgs(
    model="your-model-name",  # Replace with your model name
    dtype="bfloat16",
    gpu_memory_utilization=0.8,
    max_model_len=4096,
    trust_remote_code=True
)
llm_engine = AsyncLLMEngine.from_engine_args(engine_args)

# Define the inference endpoint
@app.post("/predict")
async def generate_text(data: RequestData):
    sampling_params = SamplingParams(
        max_tokens=data.max_tokens,
        temperature=data.temperature
    )
    request_id = "unique_request_id"  # Generate a unique request ID
    results_generator = llm_engine.generate(data.prompts, sampling_params, request_id)
    
    final_output = None
    async for request_output in results_generator:
        final_output = request_output
    
    assert final_output is not None
    text_outputs = [output.text for output in final_output.outputs]
    return {"responses": text_outputs}

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

## 待添加脚本



## Install

```bash
pip install sparrow-python
# Or dev version
pip install sparrow-python[dev]
# Or
pip install -e .
# Or
pip install -e .[dev]
```

## Usage

### Multiprocessing SyncManager

Open server first:

```bash
$ spr start-server
```

The defualt port `50001`.

(Process1) productor:

```python
from sparrow.multiprocess.client import Client

client = Client(port=50001)
client.update_dict({'a': 1, 'b': 2})
```

(Process2) consumer:

```python
from sparrow.multiprocess.client import Client

client = Client(port=50001)
print(client.get_dict_data())

>> > {'a': 1, 'b': 2}
```

### Common tools

- **Kill process by port**

```bash
$ spr kill {port}
```

- **pack & unpack**  
  support archive format: "zip", "tar", "gztar", "bztar", or "xztar".

```bash
$ spr pack pack_dir
```

```bash
$ spr unpack filename extract_dir
```

- **Scaffold**

```bash
$ spr create awosome-project
```

### Some useful functions

> `sparrow.relp`  
> Relative path, which is used to read or save files more easily.

> `sparrow.performance.MeasureTime`  
> For measuring time (including gpu time)

> `sparrow.performance.get_process_memory`  
> Get the memory size occupied by the process

> `sparrow.performance.get_virtual_memory`  
> Get virtual machine memory information

> `sparrow.add_env_path`  
> Add python environment variable (use relative file path)

### Safe logger in `multiprocessing`

```python
from sparrow.log import Logger
import numpy as np

logger = Logger(name='train-log', log_dir='./logs', )
logger.info("hello", "numpy:", np.arange(10))

logger2 = Logger.get_logger('train-log')
print(id(logger2) == id(logger))
>> > True
```
