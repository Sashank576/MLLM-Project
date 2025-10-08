import sys
import pandas as pd
import pickle
from tqdm import tqdm
import random
import numpy as np

if sys.argv[1] == '2012':
    from anes2012 import *
if sys.argv[1] == '2016':
    from anes2016 import *
if sys.argv[1] == '2020':
    from anes2020 import *

from common import *

foi_keys = fields_of_interest.keys()

def compute_demographic_distribution(df):
    distributions = {}
    for key in fields_of_interest.keys():
        value_counts = anesdf[key].value_counts(normalize=True).to_dict()
        distributions[key] = value_counts
    return distributions

# generate synthetic subject with randomly extracted demographic information
def generate_fake_respondent(distributions):
    fake_respondent = {}
    for k, v in distributions.items():
        fake_respondent[k] = np.random.choice(list(v.keys()), p=list(v.values()))
    return fake_respondent

def gen_backstory_from_fake_person(fake_person):
    backstory = ""
    for k, anes_val in fake_person.items():
        if anes_val < 0: 
            continue
        elem_template = fields_of_interest[k]['template']
        elem_map = fields_of_interest[k]['valmap']
        if len(elem_map) == 0:
            backstory += " " + elem_template.replace('XXX', str(anes_val))
        elif anes_val in elem_map:
            backstory += " " + elem_template.replace('XXX', elem_map[anes_val])
    if backstory[0] == ' ':
        backstory = backstory[1:]
    return backstory

def generate_query_with_backstory(backstory, question):
    return f"{backstory}. {question}"


anesdf = pd.read_csv(ANES_FN, sep=SEP, encoding='latin-1', low_memory=False)
full_results = []
distributions = compute_demographic_distribution(anesdf)

fake_results = []

# numbers of iteration
MAX_RETRIES = 5
for idx in tqdm(range(len(anesdf))):

    fake_person = generate_fake_respondent(distributions)
    backstory = gen_backstory_from_fake_person(fake_person)
    user_prompt = query
    full_prompt = generate_query_with_backstory(backstory, user_prompt)
    
    fake_id = f"fake_{idx}"  # fake id for synthetic respondents

    retries = 0
    success = False
    while not success and retries < MAX_RETRIES:
        try:
            response = do_query(backstory, user_prompt)
            result_entry = (fake_id, *fake_person.values(), full_prompt, response)
            full_results.append(result_entry)
            success = True 
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        except openai.OpenAIError as e:
            print(f"API Error: {e}")
        retries += 1 

    if not success:
        print(f"Failed to get a response after {MAX_RETRIES} retries for respondent {fake_id}.")


# Save the results
columns = ["ID", *fields_of_interest.keys(), "Prompt", "Response"]
df_results = pd.DataFrame(full_results, columns=columns)
df_results.to_csv(OUTPUT_CSV, index=False)
