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
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

dataset = load_dataset("openai_humaneval",split="test")
dataset = [entry for entry in dataset]

prompt_path = "./prompts/test_designer_humaneval_prompt_update.txt"
with open(prompt_path, "r") as f:
    construct_few_shot_prompt = f.read()

def preprocess_data(test_case_string):
    if f"```python" in test_case_string:
        test_case_string = test_case_string[test_case_string.find(f"```python")+len(f"```python"):]
        test_case_string = test_case_string[:test_case_string.find("```")]

    return test_case_string

# Function to fetch completion
def fetch_completion(data_entry, model, lg,times=10):
    global construct_few_shot_prompt
    if "need_reproduce" in data_entry.keys() and data_entry["need_reproduce"]==False:
        return data_entry
    prompt = data_entry["prompt"]
    entry_point = data_entry["entry_point"]
    
    text = f"""
{construct_few_shot_prompt}

**Input Code Snippet**:
```python
{prompt}
```
"""
    test_case_list = []
    for i in range(times):
        while True:
            try:
                completions = openai.ChatCompletion.create(
                    # MODIFIED: Use engine for Azure, and parameter instead of hardcoded
                    # model="gpt-3.5-turbo-1106",
                    engine=model,  # Azure deployment name from parameter
                    stream=False,
                    messages=[
                {"role": "system", "content": "You are a code developer assistant."},
                {"role": "user", "content":text},
                    ],
                    request_timeout=100,
                )
                test_case = completions.choices[0]["message"]["content"]
                test_case = preprocess_data(test_case)
            except Exception as e:
                time.sleep(20)
                print(e)
                test_case = ""
            if test_case!="":
                break
        test_case_list.append(test_case)
    data_entry["test_case_list"] = test_case_list
    return data_entry

def call_fetch_test_completion_helper(dataset, model,lg):
    print("Fixing bug...")
    with ThreadPoolExecutor(max_workers=5) as executor:
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
    # MODIFIED: Use same model as programmer
    # model_list = ["gpt-3.5-turbo-1106"]
    model_list = ["gpt-4.1"]
    language = ["python"]
    for model in model_list:
        for lg in language:
            # MODIFIED: Load dataset
            # For non-comp:
            # with open(f"./dataset/{model}_{lg}_noncomp.json", "r") as f:
            # For comp S1:
            # with open(f"./dataset/{model}_{lg}_comp_s1.json", "r") as f:
            # For comp S2:
            with open(f"./dataset/{model}_{lg}_comp_s2.json", "r") as f:
                dataset = json.load(f)
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
