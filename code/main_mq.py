import sys
import pandas as pd
import pickle
from tqdm import tqdm
import random
import numpy as np

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

def generate_prompt_for_question(question, answers):
    user_prompt = \
f"""Question: {question}

Answer choices:
{answers}

My answer is
"""
    return user_prompt

anesdf = pd.read_csv(ANES_FN, sep=SEP, encoding='latin-1', low_memory=False)
anes_2020_questionnaire = pd.read_excel("./ANES_2020_multiple_questions_selected.xlsx")
distributions = compute_demographic_distribution(anesdf)
time_date = "Today is November 3, 2020. "
fake_results = []


# Define the index range of questions this iteration should process
# [0:9]
START_INDEX = 0  # The starting index for this iteration (inclusive)
END_INDEX = 9    # The ending index for this iteration (inclusive)


for idx in range(START_INDEX, END_INDEX + 1):
    row = anes_2020_questionnaire.iloc[idx]
    full_results = []

    code = row["Code"]
    question = row["Question"]
    answers = row["Answers"]
    user_prompt = generate_prompt_for_question(question, answers)
    MAX_RETRIES = 5
    for idx in tqdm(range(len(anesdf))):
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
        
        
    # Save the results
    output_filename = f"full_results_2020_{code}.csv"
    columns = ["ID", *fields_of_interest.keys(), "Prompt", "Response"]
    df_results = pd.DataFrame(full_results, columns=columns)
    df_results.to_csv(output_filename, index=False)
