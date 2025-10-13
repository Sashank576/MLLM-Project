import os   
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

#Make sure it doesnt connect to huggingface (online)
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

#Path to the local model
model_path = os.environ.get("LLAMA_MODEL_PATH", "/projects/2/managed_datasets/Meta-Llama-3.1-8B-Instruct")
datatype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True, local_files_only=True)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    dtype=datatype,
    device_map="auto",
    local_files_only=True,
)

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



def do_query(system_prompt, user_prompt, max_tokens=2, engine=model):
    #Same output = same input
    #temperature=0.0
    #top_p = 1.0 #uncomment if do_sample is True
    messages = [{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}]
    #Format messages to Llama format
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    #Tokenize prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(engine.device)
    input_tokens = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    #Keep this so you dont store gradients and computional graphs, save memory
    with torch.no_grad():
        #Get model output
        outputs = engine.generate(
            input_ids=input_tokens,
            attention_mask=attention_mask,
            max_new_tokens=max_tokens,
            do_sample=False, #Deterministic, no randomness
            pad_token_id=tokenizer.eos_token_id,
        )
    #Get newly generated tokens
    response_tokens = outputs[0][input_tokens.shape[1]:]
    text = tokenizer.decode(response_tokens, skip_special_tokens=True)
    text = text.strip()
    return text