import sys
import pandas as pd
import pickle
from tqdm import tqdm
import random
import numpy as np
import time


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

def filter_dataframe(df, value_set, column):
    if isinstance(value_set, tuple):
        mask = df[column].isin(value_set)
    elif isinstance(value_set, range):
        mask = df[column].between(value_set.start, value_set.stop - 1)
    else:
        mask = (df[column] == value_set)
    return df[mask]

anesdf = pd.read_csv(ANES_FN, sep=SEP, encoding='latin-1', low_memory=False)
anes_2020_questionnaire = pd.read_excel("./ANES_2020_multiple_questions_selected.xlsx")

def generate_prompt_for_question(question, answers):
    return f"Question: {question}\n\nAnswer choices:\n{answers}\n\nMy answer is\n"



# Define the index range this script should process
# [0 ~ 9]
START_INDEX = 0  # The starting index for this iteration (inclusive)
END_INDEX = 9    # The ending index for this iteration (inclusive)
time_date = "Today is November 3, 2020. "


for idx in range(START_INDEX, END_INDEX + 1):
    row = anes_2020_questionnaire.iloc[idx]
    code = row["Code"]
    question = row["Question"]
    answers = row["Answers"]
    
    
    # index for demographic conditions
    # [0 ~ 7]
    CONDITION_START_INDEX = 0  
    CONDITION_END_INDEX = 7  #


    for cond_idx, (column, value_sets) in enumerate(conditions.items()):
        if cond_idx < CONDITION_START_INDEX or cond_idx > CONDITION_END_INDEX:
            continue 

        
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
                user_prompt = generate_prompt_for_question(question, answers)
                system_prompt = time_date + backstory

                full_prompt = generate_query_with_backstory(system_prompt, user_prompt)                
                fake_id = f"fake_{idx}"  
                retries = 0
                success = False
                while not success and retries < MAX_RETRIES:
                    try:
                        response = do_query(system_prompt, user_prompt)
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

                print(full_prompt)
                print(response)
              
            # Save the results
            columns = ["ID", *fields_of_interest.keys(), "Prompt", "Response"]
            df_results = pd.DataFrame(full_results, columns=columns)
            output_csv = f"output_{code}_{label}.csv"
            df_results.to_csv(output_csv, index=False)
