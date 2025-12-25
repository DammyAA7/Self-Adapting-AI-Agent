import argparse
import os
import json
from tqdm import tqdm
import copy
import openai
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

# Setting API parameters
# MODIFIED FOR AZURE OPENAI
# openai.api_base = "https://api.aiohub.org/v1"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# MODIFIED FOR SELFEVOLVE COMPARISON
# dataset = load_dataset("openai_humaneval",split="test")
# dataset = [entry for entry in dataset]

# MODIFIED: Switch between non-compositional and compositional
# For non-compositional (8 tasks):
# print("Loading 8 non-compositional SelfEvolve tasks...")
# with open("./dataset/non_compositional_tasks.jsonl", "r") as f:
#     dataset = [json.loads(line) for line in f]
# print(f"Loaded {len(dataset)} non-compositional tasks")

# For compositional Session 2 (3 tasks with Session 1 code in context):
# Session 1:
# print("Loading Compositional Session 1 tasks...")
# with open("./dataset/compositional_session1.jsonl", "r") as f:
#     dataset = [json.loads(line) for line in f]
# Session 2:
print("Loading Compositional Session 2 tasks...")
with open("./dataset/compositional_session2.jsonl", "r") as f:
    dataset = [json.loads(line) for line in f]
# print(f"Loaded {len(dataset)} compositional Session 1 tasks")
print(f"Loaded {len(dataset)} compositional Session 2 tasks")
# print(f"Loaded {len(dataset)} integrational tasks")

for task in dataset[:3]:
    ctx_len = len(task.get("codebase_context", ""))
    task_name = task.get('_original_task', 'unknown')
    print(f"  - {task_name}: {ctx_len} chars context")

prompt_path = "./prompts/humaneval_prompt_update.txt"
with open(prompt_path, "r") as f:
    construct_few_shot_prompt = f.read()

def preprocess_data(completion_string):
    if f"```python" in completion_string:
        completion_string = completion_string[completion_string.find(f"```python")+len(f"```python"):]
        completion_string = completion_string[:completion_string.find("```")]
    else:
        print("Error: No code block found")
    return completion_string

# Function to fetch completion
def fetch_completion(data_entry, model,lg,times = 5):
    global construct_few_shot_prompt
    if "need_reproduce" in data_entry.keys() and data_entry["need_reproduce"]==False:
        return data_entry
    prompt = data_entry["prompt"]

    # MODIFIED: Add codebase context in USER message (same as SelfEvolve does)
    codebase_context = data_entry.get("codebase_context", "")

    if codebase_context:
        # With context (integration/data tasks)
        text = f"""
{construct_few_shot_prompt}

**AVAILABLE CODEBASE/DATA:**
{codebase_context}

**Input Code Snippet**:
```python
{prompt}
```
## Completion 3:
"""
    else:
        # Without context (original AgentCoder behavior)
        text = f"""
{construct_few_shot_prompt}

**Input Code Snippet**:
```python
{prompt}
```
## Completion 3:
"""
    completions_code = []
    for i in range(times):
        while True:
            try:
                completions = openai.ChatCompletion.create(
                    # MODIFIED: Azure requires 'engine' not 'model'
                    # model=model,
                    engine=model,  # Azure deployment name
                    stream=False,
                    messages=[
                {"role": "system", "content": "You are a software programmer."},
                {"role": "user", "content":text},
                    ],
                    request_timeout=100,
                )
                completion = completions.choices[0]["message"]["content"]
                completion = preprocess_data(completion)

            except Exception as e:
                print(e)
                time.sleep(10)
                completion = ""
            if completion!="":
                break
        completions_code.append(completion)
    data_entry["completion_list"] = completions_code
    return data_entry


def call_fetch_completion_helper(dataset, model,lg):
    print("Fixing bug...")
    # MODIFIED: Reduce parallelism to avoid rate limits (large context per task)
    # with ThreadPoolExecutor(max_workers=5) as executor:
    with ThreadPoolExecutor(max_workers=1) as executor:
        future_to_entry = {executor.submit(fetch_completion, copy.deepcopy(entry), model, lg): entry for entry in tqdm(dataset)}
        for future in tqdm(concurrent.futures.as_completed(future_to_entry)):
            entry = future_to_entry[future]
            try:
                updated_entry = future.result()
                idx = dataset.index(entry)
                dataset[idx] = updated_entry
            except Exception as e:
                print(repr(e))
    return dataset

if __name__ == "__main__":
    # MODIFIED: Use Azure deployment name
    # model_list = ["gpt-3.5-turbo-1106"]
    model_list = ["gpt-4.1"]  # Azure deployment name
    language = ["python"]
    for model in model_list:
        for lg in language:
            # MODIFIED: Use already loaded SelfEvolve dataset
            # from datasets import load_dataset
            # dataset = load_dataset("openai_humaneval",split="test")
            # dataset = [entry for entry in dataset]
            # Dataset already loaded at top of file
            # MODIFIED: Reduce parallelism to avoid rate limits
            # with ThreadPoolExecutor(max_workers=5) as executor:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future_to_entry = {executor.submit(fetch_completion, copy.deepcopy(entry), model, lg): entry for entry in tqdm(dataset)}
                for future in tqdm(concurrent.futures.as_completed(future_to_entry)):
                    entry = future_to_entry[future]
                    try:
                        updated_entry = future.result()
                        idx = dataset.index(entry)
                        dataset[idx] = updated_entry
                    except Exception as e:
                        print(repr(e))
            # MODIFIED: Save results
            # For non-comp:
            # with open(f"./dataset/{model}_{lg}_noncomp.json", "w") as f:
            # For comp S1:
            # with open(f"./dataset/{model}_{lg}_comp_s1.json", "w") as f:
            # For comp S2:
            with open(f"./dataset/{model}_{lg}_comp_s2.json", "w") as f:
                json.dump(dataset, f, indent=4)
