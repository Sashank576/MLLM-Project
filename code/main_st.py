import sys
import pandas as pd
import pickle
from tqdm import tqdm
import random
import numpy as np
import time


if sys.argv[1] == '2012':
    from anes2012 import *
if sys.argv[1] == '2016':
    from anes2016 import *
if sys.argv[1] == '2020':
    from anes2020 import *

from common import *

foi_keys = fields_of_interest.keys()
conditions = {
    'V201200': {
            (1, 2, 3): "liberal",
            4: "moderate",
            (5, 6, 7): "conservative"
    },
    'V201231x': {
            (1, 2, 3): "democrat",
            4: "independent",
            (5, 6, 7): "republican"
    },
    'V201507x': {
            range(18, 31): "18~30",
            range(31, 46): "31~45",
            range(46, 61): "46~60",
            range(61, 200): "over_60"  # Assuming 200 as a reasonable upper age limit
    },
    'V201600': {
            1: "man",
            2: "woman"
    },
    'V202406': {
            (1, 2): "interest",
            (3, 4): "no_interest"
    },
    'V201549x': {1: 'white', 2: 'black', 3: 'asian', 4: 'native American', 5: 'hispanic'},
    'V202022': {
            1: 'like_to_discuss',
            2: 'never_discuss'
        },
    'V201452':  {1: "attend_church", 2: "do_not_attend"}
}

def compute_demographic_distribution(df):
    distributions = {}
    for key in fields_of_interest.keys():
        value_counts = df[key].value_counts(normalize=True).to_dict()
        distributions[key] = value_counts
    return distributions

def generate_fake_respondent(distributions):
    fake_respondent = {}
    for k, v in distributions.items():
        fake_respondent[k] = np.random.choice(list(v.keys()), p=list(v.values()))
    return fake_respondent

def gen_backstory_from_fake_person(fake_person):
    backstory = ""
    for k, anes_val in fake_person.items():
        if anes_val < 0:  # 음수 값은 backstory에 포함되지 않습니다.
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

# Filter ANES data using demographic condition
def filter_dataframe(df, value_set, column):
    if isinstance(value_set, tuple):
        mask = df[column].isin(value_set)
    elif isinstance(value_set, range):
        mask = df[column].between(value_set.start, value_set.stop - 1)
    else:
        mask = (df[column] == value_set)
    return df[mask]

anesdf = pd.read_csv(ANES_FN, sep=SEP, encoding='latin-1', low_memory=False)

for column, value_sets in conditions.items():
    for value_set, label in value_sets.items():
        if isinstance(value_set, tuple) or isinstance(value_set, range):
            value_set_description = f"{' '.join(map(str, value_set))}"
        else:
            value_set_description = str(value_set)
          
        print(f"Running experiment for {column} with condition: {label} for values {value_set_description}")
        
        filtered_df = filter_dataframe(anesdf, value_set, column)
        full_results = []
        distributions = compute_demographic_distribution(filtered_df)

        MAX_RETRIES = 5
        for idx in tqdm(range(len(filtered_df))):

            fake_person = generate_fake_respondent(distributions)
            backstory = gen_backstory_from_fake_person(fake_person)
            user_prompt = query
            full_prompt = generate_query_with_backstory(backstory, user_prompt)
            
            fake_id = f"fake_{idx}"  

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
        output_csv = f"output_{column}_{label}.csv"
        df_results.to_csv(output_csv, index=False)
