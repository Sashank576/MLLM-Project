from common import *

SEP=','
OUTPUT_FN = "./full_results_2016.pkl"
OUTPUT_CSV = "./full_results_2016.csv"
ID_COL = "V160001_orig"
VOTE_COL = "V162062x" 
K2 = "cliton"
tok_sets = {
"trump": gen_variants( [ "trump", "donald", "republican", "conservative" ] ), # the republican, mr trump
"clinton": gen_variants( [ "clinton", "hillary", "rodham", "senator", "democrat", "democratic", "liberal"] ),
}

query = "In the 2016 presidential election, I voted for"
ANES_FN = './anes_timeseries_2016_rawdata.csv'

fields_of_interest = {
    'V161310x': {
        "template": "Racially, I am XXX.",
        "valmap": {1: 'white', 2: 'black', 3: 'asian', 4: 'native American', 5: 'hispanic'}
    },
    'V162174': {
        "template": "XXX",
        "valmap": {
            1: 'I like to discuss politics with my family and friends.',
            2: 'I never discuss politics with my family or friends.'
        }
    },
    'V161126': {
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
    'V161158x': {
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
    'V161244': {
        "template": "I XXX.",
        "valmap": {1: "attend church", 2: "do not attend church"}
    },
    'V161267': {
        "template": "I am XXX years old.",
        "valmap": {}
    },
    'V161342': {
        "template": "I am a XXX.",
        "valmap": {1: "man", 2: "woman"}
    },
    'V162256': {
        "template": "I am XXX interested in politics.",
        "valmap": {1: "very", 2: "somewhat", 3: "not very", 4: "not at all"}
    }
}
