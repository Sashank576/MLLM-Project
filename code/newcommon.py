import numpy as np
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


model_path = "/projects/2/managed_datasets/llama3/8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
#bf16 for faster and more stable inference, float32 if no GPU
dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=dtype, device_map="auto")
#Evaluation mode, disable dropout, consistent results
model.eval()

def lc(t):
    return t.lower()

def uc(t):
    return t.upper()

def mc(t):
    tmp = t.lower()
    return tmp[0].upper() + t[1:]

def gen_variants(toks):
    results = []
    variants = [lc, uc, mc]
    for t in toks:
        for v in variants:
            results.append(" " + v(t))
    return results

def extract_probs(lp):
    lp_keys = list(lp.keys())
    ps = [lp[k] for k in lp_keys]
    vals = [(lp_keys[ind], ps[ind]) for ind in range(len(lp_keys))]
    vals = sorted(vals, key=lambda x: x[1], reverse=True)
    result = {}
    for v in vals:
        result[v[0]] = v[1]
    return result






#TODO: Change to local model, not use API
def do_query(system_prompt, user_prompt, max_tokens=2, engine=model):
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    response = client.chat.completions.create(
        model=engine,
        messages=messages,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def run_prompts(prompts, engine=model):
    results = []
    for prompt in prompts:
        response = do_query(prompt, max_tokens=2, engine=engine)
        results.append(response)
        time.sleep(0.1)
    return results

