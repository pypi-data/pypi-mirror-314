# Prompt Evaluator

`prompt-evaluator` is a Python package that evaluates prompts using OpenAI and google models based on criteria like clarity, specificity, relevance, and more.

It can do below tasks.

1) prompt evaluation 

```bash
from prompt-evaluator import PromptEvaluator
evaluator = PromptEvaluator(openai_api_key="your_api_key",model="model_name")
evaluator.evaluate_prompt(model="model_name",prompt=prompt)
```

2) Finding the number of tokens in prompt.

```bash
from prompt-evaluator import PromptEvaluator
evaluator = PromptEvaluator(openai_api_key="your_api_key",model="model_name")
evaluator.token_length(prompt,model="model_name")
```

3) Prompt enhancement as per the use-case - In dev.
4) Prompt token reducer to lower the prompt tokens - In dev.

## Installation

```bash
pip install prompt-evaluator
