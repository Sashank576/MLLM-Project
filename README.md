#TODO: Change ReadME

# (Our Paper Name).
This repository contains the code for the paper "." All code has been anonymized for confidentiality.

### Data
Within the data folder, you'll find the ANES data from the years 2012, 2016, and 2020. Additionally, the questionnaire file `ANES_2020_multiple_questions_selected.xlsx`, used for the multiple question experiment, is also included. Each dataset can be downloaded from [American National Election Studies (ANES)](https://electionstudies.org/data-center/).

### Code
We have reproduced and modified the user prompts described in [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144). The code has been modified and augmented based on the code used by [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144).

`common.py` is a script for using the OpenAI API. Insert your own OpenAI API key and select the desired model as the `engine` argument. In [Sun et al. (2024)](https://arxiv.org/pdf/2402.18144), `gpt-3.5-turbo-0613` was adopted.	

`newcommon.py` is a script for using the Llama model. In our experiments, the Llama 3.1-8B-instruct model was adopted. The model and required python packages were downloaded locally in the same directory.

`anes2012.py`, `anes2016.py`, and `anes2020.py` are scripts for converting demographic information of respondents from each respective ANES dataset into first-person prompts.

`main.py` is a script for performing random silicon sampling on the U.S. presidential election candidate choice for each year. You can run 
``` 
python main.py <year>
```
to conduct random silicon sampling on the ANES data for the specified year.

`main_st.py` is a script for stratified experiments. It allows for random silicon sampling from 23 subgroups extracted from the ANES 2020 data. 

`main_mq.py` is a script for the multiple question experiment. It facilitates random silicon sampling using ANES 2020 data for 10 surveys selected in our study.

`main_mq_st.py` is a script for stratified experiments on multiple questions. It performs random silicon sampling on 23 subgroups extracted from ANES 2020 data for 10 surveys chosen in our study.

