from django.db import connection

import pandas as pd
import numpy as np

from dating.models import Answer

qu = Answer.objects.all().prefetch_related('answer_other')

data = [
    {
        'user_id': q.user_id, 
        'question': q.question_id, 
        'answer_self': q.answer_self_id,
        'answer_other': [t.id for t in q.answer_other.all()],
        'importance' : q.importance,}
    for q in qu
]

df= pd.DataFrame(
    data, 
    columns=[
        'user_id', 
        'question', 
        'importance',
        'answer_self',
        'answer_other'])

# df = answer_df.pivot(index='user_id', values=['answer_self', 'answer_other','importance'], columns='question')

df['answer_other'] = df['answer_other'].apply(np.array)
df['mandatory'] = df['importance'] == 300


def get_pair(user_id1, user_id2, data):
    data_pair = data[(data['user_id'] == user_id1) | (data['user_id'] == user_id2)]
    return data_pair


def common_answers(data):
    questions = data.groupby('question').count() == 2
    questions = questions[questions['user_id'] == True]
    questions = questions.index.values
    data = data[data['question'].isin(questions)]
    return data


def user_data(data, userid1, userid2):
    userdata = data[['user_id', 'question', 'importance', 'answer_other']][data['user_id'] == userid1]
    other = data[['question', 'answer_self']][data['user_id'] == userid2]
    merged = userdata.merge(other, on='question')
    merged['accepted_answers'] = merged['answer_other']
    merged['answer_given'] = merged['answer_self']
    del merged['answer_self']
    del merged['answer_other']
    return merged

def get_scores(data):
    data['score'] = 0
    accepted = data['accepted_answers']
    other = data['answer_given']
    data['score'] = [int(x[0] in x[1]) for x in data[['answer_given', 'accepted_answers']].values.tolist()] * data['importance']
    data['avg_score'] = data['score'].mean() / data['importance'].mean()
    return data


def matching_scores(data, user1, user2):
    def get_pair(user_id1, user_id2, data):
        data_pair = data[(data['user_id'] == user_id1) | (data['user_id'] == user_id2)]
        return data_pair


    def common_answers(data):
        questions = data.groupby('question').count() == 2
        questions = questions[questions['user_id'] == True]
        questions = questions.index.values
        data = data[data['question'].isin(questions)]
        return data


    def user_data(data, userid1, userid2):
        userdata = data[['user_id', 'question', 'importance', 'answer_other']][data['user_id'] == userid1]
        other = data[['question', 'answer_self']][data['user_id'] == userid2]
        merged = userdata.merge(other, on='question')
        merged['accepted_answers'] = merged['answer_other']
        merged['answer_given'] = merged['answer_self']
        del merged['answer_self']
        del merged['answer_other']
        return merged

    def get_scores(data):
            data['score'] = 0
            accepted = data['accepted_answers']
            other = data['answer_given']
            data['score'] = [int(x[0] in x[1]) for x in data[['answer_given', 'accepted_answers']].values.tolist()] * data['importance']
            data['avg_score'] = data['score'].mean() / data['importance'].mean()
            return data

    datapair = get_pair(user1, user2, data)
    commonanswers = common_answers(datapair)
    userdata = user_data(commonanswers, user1, user2)
    scoredata1 = get_scores(userdata)
    score1 = round(100*scoredata1['avg_score'][0])
    userdata2 = user_data(commonanswers, user2, user1)
    scoredata2 = get_scores(userdata2)
    score2 = round(100*scoredata2['avg_score'][0])
    combined = (score1 + score2)/2
    return score1, score2, combined

user1 = 1
user2 = 2
print(f'matchingscore user 2 is a {matching_scores(df, user1, user2)[0]}% match for user 1')
print(f'matchingscore user 1 is a {matching_scores(df, user1, user2)[1]}% match for user 2')
print(f'combined they have a {matching_scores(df, user1, user2)[2]}% match')

print(df)