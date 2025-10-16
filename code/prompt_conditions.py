# Allowed values: "reformulated" (Condition 1a) or "reverse" (Condition 1b)
CONDITION = "reformulated"  # change to "reverse" when you want 1b

# Each entry: code -> {"reformulated": {"q": "...", "answers": [...]},
#                      "reverse": {"q": "...", "answers": [...] or None if N/A}}
PROMPT_BANK = {
    # Race diversity V202371
    "V202371": {
        "reformulated": {
            "q": "How would this respondent describe the impact of the increasing number of people of many different races and ethnic groups on the United States as a place to live?",
            "answers": [
                "1. Improves it as a place to live",
                "2. Worsens it as a place to live",
                "3. Makes no difference",
            ],
        },
        "reverse": {
            "q": "How would this respondent describe the impact of limiting increases in the number of people of many different races and ethnic groups on the United States as a place to live?",
            "answers": [
                "1. Improves it as a place to live",
                "2. Worsens it as a place to live",
                "3. Makes no difference",
            ],
        },
    },

    # Gender role V202287
    "V202287": {
        "reformulated": {
            "q": "How would this respondent describe the impact on the family as a whole if the man works outside the home and the woman takes care of the home and family?",
            "answers": [
                "1. Improves the family as a whole",
                "2. Worsens the family as a whole",
                "3. Makes no difference",
            ],
        },
        "reverse": {
            "q": "How would this respondent describe the impact on the family as a whole if both the man and the woman share work outside the home and take care of the home and family?",
            "answers": [
                "1. Improves the family as a whole",
                "2. Worsens the family as a whole",
                "3. Makes no difference",
            ],
        },
    },

    # Current Economy V201324 
    "V201324": {
        "reformulated": {
            "q": "How would this respondent describe the state of the economy these days in the United States?",
            "answers": [
                "1. Very strong",
                "2. Strong",
                "3. Neither strong nor weak",
                "4. Weak",
                "5. Very weak",
            ],
        },
        "reverse": None,
    },

    # Drug addiction (opioids) V202348
    "V202348": {
        "reformulated": {
            "q": "How would this respondent assess whether the federal government should be doing more about the opioid drug addiction issue, should be doing less, or is it currently doing the right amount?",
            "answers": [
                "1. Should be doing more",
                "2. Should be doing less",
                "3. Is doing the right amount",
            ],
        },
        "reverse": None,
    },

    # Climate change V202332
    "V202332": {
        "reformulated": {
            "q": "How would this respondent assess how much, if at all, climate change is currently affecting severe weather events or temperature patterns in the United States?",
            "answers": [
                "1. Not at all",
                "2. A little",
                "3. A moderate amount",
                "4. A lot",
                "5. A great deal",
            ],
        },
        "reverse": {
            "q": "How much would this respondent agree with the statement that climate change is unrelated to severe weather events or temperature patterns in the United States?",
            "answers": [
                "1. Not at all",
                "2. A little",
                "3. A moderate amount",
                "4. A lot",
                "5. A great deal",
            ],
        },
    },

    # Gay marriage V201416
    "V201416": {
        "reformulated": {
            "q": "Which comes closest to this respondent’s view?",
            "answers": [
                "1. Gay and lesbian couples should be allowed to legally marry.",
                "2. Gay and lesbian couples should be allowed to form civil unions but not legally marry.",
                "3. There should be no legal recognition of gay or lesbian couples’ relationship.",
            ],
        },
        "reverse": {
            "q": "Which one disagrees the most with this respondent’s view?",
            "answers": [
                "1. Gay and lesbian couples should be allowed to legally marry.",
                "2. Gay and lesbian couples should be allowed to form civil unions but not legally marry.",
                "3. There should be no legal recognition of gay or lesbian couples’ relationship.",
            ],
        },
    },

    # Refugee allowing V202234
    "V202234": {
        "reformulated": {
            "q": "What is this respondent’s position on whether refugees who are fleeing war, persecution, or natural disasters in other countries should be allowed to come to live in the U.S.?",
            "answers": [
                "1. Should be allowed",
                "2. Should not be allowed",
                "3. No clear position",
            ],
        },
        "reverse": {
            "q": "What is this respondent’s position on whether refugees who are fleeing war, persecution, or natural disasters in other countries should be prohibited from coming to live in the U.S.?",
            "answers": [
                "1. Should be prohibited",
                "2. Should not be prohibited",
                "3. No clear position",
            ],
        },
    },

    # Health insurance V202378 
    "V202378": {
        "reformulated": {
            "q": "How would this respondent assess if there should be an increase, decrease, or no change in government spending to help people pay for health insurance when people cannot pay for it all themselves?",
            "answers": [
                "1. Increase",
                "2. Decrease",
                "3. No change",
            ],
        },
        "reverse": None,
    },

    # Gun regulation V202337 
    "V202337": {
        "reformulated": {
            "q": "What is this respondent’s position on whether the federal government should make it more difficult for people to buy a gun than it is now, make it easier for people to buy a gun, or keep these rules about the same as they are now?",
            "answers": [
                "1. More difficult",
                "2. Easier",
                "3. Keep these rules about the same",
            ],
        },
        "reverse": None,
    },

    # Income inequality V202257
    "V202257": {
        "reformulated": {
            "q": "How would this respondent assess whether the government should be trying to reduce the difference in incomes between the richest and poorest households?",
            "answers": [
                "1. Should be trying",
                "2. Should not be trying",
                "3. Neither of these",
            ],
        },
        "reverse": {
            "q": "How would this respondent assess whether the government should stop trying to reduce the difference in incomes between the richest and poorest households?",
            "answers": [
                "1. Should stop trying",
                "2. Should not stop trying",
                "3. Neither of these",
            ],
        },
    },
}
