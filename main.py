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
    verbs_list = df[['infinitive_spanish', 'infinitive_english']].drop_duplicates().values.tolist()
    verbs_list.sort()
    return verbs_list


@app.get("/get-random-verb-conjugation")
def get_random_verb_conjugation(mood: str, use_irregular: bool, use_vosotros: bool, tenses: str = Query(...)):
    all_verbs_df = pd.read_csv("./conjugations.csv")

    # # Drop unnecessary columns
    # all_verbs_df.drop([
    #     'gerund_spanish',
    #     'gerund_english',
    #     'past_participle_spanish',
    #     'past_participle_english'
    # ], axis='columns', inplace=True)

    # Filter the data frame for the chosen mood(s)
    all_verbs_df = all_verbs_df[all_verbs_df['mood_english'] == mood]

    # Filter the data frame for chosen tense(s)
    tenses_list = [tense.strip() for tense in tenses.split(',')]
    all_verbs_df = all_verbs_df[all_verbs_df['tense_english'].isin(tenses_list)]

    # Choose a verb at random from the list
    random_verb_index = random.randint(1, len(all_verbs_df)) - 1
    all_verbs_df = all_verbs_df.iloc[[random_verb_index]]

    if use_vosotros:
        random_form = random.choice(['form_1ps', 'form_2ps', 'form_3ps', 'form_1pp', 'form_2pp', 'form_3pp'])
        all_verbs_df = all_verbs_df[[
            'infinitive_spanish',
            'infinitive_english',
            'mood_spanish',
            'mood_english',
            'tense_english',
            'tense_spanish',
            random_form + '_spanish',
            random_form + '_english']]
        all_verbs_df = all_verbs_df.rename(
            columns={random_form + '_spanish': 'form_spanish', random_form + '_english': 'form_english'}
        )
    else:
        random_form = random.choice(['form_1ps', 'form_2ps', 'form_3ps', 'form_1pp', 'form_3pp'])
        all_verbs_df = all_verbs_df[[
            'infinitive_spanish',
            'infinitive_english',
            'mood_spanish',
            'mood_english',
            'tense_english',
            'tense_spanish',
            random_form + '_spanish',
            random_form + '_english']]
        all_verbs_df = all_verbs_df.rename(
            columns={random_form + '_spanish': 'form_spanish', random_form + '_english': 'form_english'}
        )

    final_json = json.loads(all_verbs_df.to_json(orient='records'))
    return final_json


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
