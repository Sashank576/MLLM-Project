# Random Silicon Sampling: Simulating Human Sub-Population Opinion Using a Large Language Model Based on Group-Level Demographic Information.
This repository contains the code for the paper "Random Silicon Sampling: Simulating Human Sub-Population Opinion Using a Large Language Model Based on Group-Level Demographic Information." All code has been anonymized for confidentiality.

### Data
Within the data folder, you'll find the ANES data from the years 2012, 2016, and 2020. Additionally, the questionnaire file `ANES_2020_multiple_questions_selected.xlsx`, used for our multiple question experiment, is also included. Each dataset can be downloaded from [American National Election Studies (ANES)](https://electionstudies.org/data-center/).

### Code
We have reproduced and extended the silicon sampling method described in [Argyle et al., (2023)](https://www.cambridge.org/core/journals/political-analysis/article/out-of-one-many-using-language-models-to-simulate-human-samples/035D7C8A55B237942FB6DBAD7CAA4E49#article). The code has been modified and augmented based on the code used by [Argyle et al., (2023)](https://www.cambridge.org/core/journals/political-analysis/article/out-of-one-many-using-language-models-to-simulate-human-samples/035D7C8A55B237942FB6DBAD7CAA4E49#article).

`common.py` is a script for using the OpenAI API. Insert your own OpenAI API key and select the desired model as the `engine` argument. In our experiment, `gpt-3.5-turbo-0613` was adopted.	

`anes2012.py`, `anes2016.py`, and `anes2020.py` are scripts for converting demographic information of respondents from each respective ANES dataset into first-person prompts.

`main.py` is a script for performing random silicon sampling on the U.S. presidential election candidate choice for each year. You can run 
``` 
python main.py <year>
```
to conduct random silicon sampling on the ANES data for the specified year.

`main_st.py` is a script for stratified experiments. It allows for random silicon sampling from 23 subgroups extracted from the ANES 2020 data. 

`main_mq.py` is a script for the multiple question experiment. It facilitates random silicon sampling using ANES 2020 data for 10 surveys selected in our study.

`main_mq_st.py` is a script for stratified experiments on multiple questions. It performs random silicon sampling on 23 subgroups extracted from ANES 2020 data for 10 surveys chosen in our study.

