import random

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/get-all-verbs")
def get_all_verbs():
    df = pd.read_csv('./conjugations.csv')
    verbs_list = df[['infinitive', 'infinitive_english']].drop_duplicates().values.tolist()
    verbs_list.sort()
    return verbs_list


@app.get("/get-random-verb-conjugation")
def get_random_verb_conjugation(mood: str, use_irregular: bool, use_vosotros: bool, tenses: str = Query(...)):
    all_verbs_df = pd.read_csv("./conjugations.csv")

    all_verbs_df.rename({'form_1s': 'yo', 'form_2s': 'tú', 'form_3s': 'él/ella/usted', 'form_1p': 'nosotros/as',
                         'form_2p': 'vosotros/as', 'form_3p': 'ellos/ellas/ustedes'}, axis='columns', inplace=True)

    # Drop unnecessary columns
    all_verbs_df.drop(['verb_english', 'gerund', 'gerund_english', 'pastparticiple', 'pastparticiple_english'],
                      axis='columns', inplace=True)

    # Filter the data frame for chosen mood(s)
    filtered_for_mood_df = all_verbs_df[all_verbs_df['mood_english'] == mood.capitalize()]

    # Drop mood columns after using them to filter
    filtered_for_mood_df.drop(['mood', 'mood_english'], axis='columns', inplace=True)

    # Filter the data frame for chosen tense(s)
    tenses_list = [tense.strip().capitalize() for tense in tenses.split(',')]
    filtered_for_tense_df = filtered_for_mood_df[filtered_for_mood_df['tense_english'].isin(tenses_list)]

    # Drop tense columns after using them to filter
    filtered_for_tense_df.drop(['tense', 'tense_english'], axis='columns', inplace=True)

    # Choose a verb at random from the list
    random_verb_index = random.randint(1, len(filtered_for_tense_df)) - 1
    random_verb_df = filtered_for_tense_df.iloc[[random_verb_index]]

    if use_vosotros:
        random_form_index = random.randint(1, 6) - 1
        forms = ['yo', 'tú', 'él/ella/usted', 'nosotros/as', 'vosotros/as', 'ellos/ellas/ustedes']
        filtered_for_form_df = random_verb_df[['infinitive', 'infinitive_english', forms[random_form_index]]]
    else:
        random_verb_df.drop(['vosotros/as'], axis='columns', inplace=True)
        random_form_index = random.randint(1, 5) - 1
        forms = ['yo', 'tú', 'él/ella/usted', 'nosotros/as', 'ellos/ellas/ustedes']
        filtered_for_form_df = random_verb_df[['infinitive', 'infinitive_english', forms[random_form_index]]]

    final_json = json.loads(filtered_for_form_df.to_json(orient='records'))
    return final_json


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
