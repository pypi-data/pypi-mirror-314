# LLM Evaluation


Example of usage:

```
import os

from llm_eval.evaluator import Evaluator
from dotenv import load_dotenv

load_dotenv()

evaluator = Evaluator(os.getenv('LANGFUSE_SECRET_KEY'), os.getenv('LANGFUSE_PUBLIC_KEY'), os.getenv('LANGFUSE_HOST'),
                      os.getenv('OPENAI_INTERFACE_KEY'), os.getenv('LLM_AS_A_JUDGE_PRIVATE_KEY'), 'experiments/biomedical/input/gpt4o_mini_dataset_100.json')

evaluator.run() 
```