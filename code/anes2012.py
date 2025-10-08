from common import *

SEP=','
OUTPUT_FN = "./full_results_2016.pkl"
OUTPUT_CSV = "./full_results_2016.csv"
ID_COL = "caseid"
VOTE_COL = "presvote2012_x" 
K1 = "romney"
K2 = "obama"

tok_sets = {
"romney": gen_variants( [ "romney", "mitt", "republican", "conservative" ] ),
"obama": gen_variants( [ "obama", "barack", "democrat", "democratic", "liberal"] ),
}

query = "In the 2012 presidential election, I voted for"
ANES_FN = './anes_timeseries_2012_rawdata.csv'

fields_of_interest = {
    'dem_raceeth_x': {
        "template": "Racially, I am XXX.",
        "valmap": {1: 'white', 2: 'black', 3: 'asian', 4: 'native American', 5: 'hispanic'}
    },
    'discuss_disc': {
        "template": "XXX",
        "valmap": {
            1: 'I like to discuss politics with my family and friends.',
            2: 'I never discuss politics with my family or friends.'
        }
    },
    'libcpre_self': {
        "template": "Ideologically, I am XXX.",
        "valmap": {
            1: "extremely liberal",
            2: "liberal",
            3: "slightly liberal",
            4: "moderate",
            5: "slightly conservative",
            6: "conservative",
            7: "extremely conservative"
        }
    },
    'pid_x': {
        "template": "Politically, I am XXX.",
        "valmap": {
            1: "a strong democrat",
            2: "a weak Democrat",
            3: "an independent who leans Democratic",
            4: "an independent",
            5: "an independent who leans Republican",
            6: "a weak Republican",
            7: "a strong Republican"
        }
    },
    'relig_church': {
        "template": "I XXX.",
        "valmap": {1: "attend church", 2: "do not attend church"}
    },
    'dem_age_r_x': {
        "template": "I am XXX years old.",
        "valmap": {}
    },
    'gender_respondent_x': {
        "template": "I am a XXX.",
        "valmap": {1: "man", 2: "woman"}
    },
    'paprofile_interestpolit': {
        "template": "I am XXX interested in politics.",
        "valmap": {1: "very", 2: "somewhat", 3: "not very", 4: "not at all"}
    }
}
