import pandas as pd
import numpy as np

from dating.models import Answer, User, Matching
def update_matches(user_id, answer, user, matching, pd, np):
    def get_data(answer, pd, np):
        qu = answer.objects.all().prefetch_related('answer_other')

        data = [
            {
                'user_id': q.user_id,
                'question': q.question_id,
                'answer_self': q.answer_self_id,
                'answer_other': [t.id for t in q.answer_other.all()],
                'importance': q.importance, }
            for q in qu
        ]

        df = pd.DataFrame(
            data,
            columns=[
                'user_id',
                'question',
                'importance',
                'answer_self',
                'answer_other'])

        df['answer_other'] = df['answer_other'].apply(np.array)
        df['mandatory'] = df['importance'] == 300
        return df

    def matching_scores(user1, user2, data):

        def get_pair(user_id1, user_id2, data):
            data_pair = data[(data['user_id'] == user_id1) |
                            (data['user_id'] == user_id2)]
            return data_pair

        def common_answers(data):
            questions = data.groupby('question').count() == 2
            questions = questions[questions['user_id'] == True]
            questions = questions.index.values
            data = data[data['question'].isin(questions)]
            return data

        def user_data(data, userid1, userid2):
            userdata = data[['user_id', 'question', 'importance',
                'answer_other', 'mandatory']][data['user_id'] == userid1]
            other = data[['question', 'answer_self']][data['user_id'] == userid2]
            merged = userdata.merge(other, on='question')
            merged['accepted_answers'] = merged['answer_other']
            merged['answer_given'] = merged['answer_self']
            del merged['answer_self']
            del merged['answer_other']
            return merged

        def get_scores(data):

            accepted = data['accepted_answers']
            other = data['answer_given']
            data['score'] = [int(x[0] in x[1]) for x in data[[
                                'answer_given', 'accepted_answers']].values.tolist()] * data['importance']
            data['avg_score'] = data['score'].mean() / data['importance'].mean()
            filter_mandatory = data[(data['mandatory'] == True)
                                    & (data['score'] == 0)]
            if filter_mandatory.shape[0] == 1:
                data['avg_score'] = -1
            return data

        datapair = get_pair(user1, user2, data)
        if len(datapair.index) < 2:
            return None
        commonanswers = common_answers(datapair)
        if len(commonanswers.index) < 2:
            return None
        userdata1 = user_data(commonanswers, user1, user2)
        if len(userdata1.index) < 2:
            return None
        scoredata1 = get_scores(userdata1)
        score1 = round(100*scoredata1['avg_score'][0])
        userdata2 = user_data(commonanswers, user2, user1)
        if len(userdata2.index) < 2:
            return None
        scoredata2 = get_scores(userdata2)
        score2 = round(100*scoredata2['avg_score'][0])
        combined = (score1 + score2)/2
        return score1, score2, combined

    data =  get_data(answer, pd, np)
# todo only calculate each pair once

    for i in user.objects.all():
        if i != user_id:
            scores = matching_scores(user_id, i.pk, data)
            if scores != None:
                matching.objects.update_or_create(
                    user=user.objects.get(pk=user_id),
                    other_user=user.objects.get(pk=i.pk),
                    forward_score=scores[0],
                    backward_score=scores[1],
                    combined_score=scores[2],
                )
                matching.objects.update_or_create(
                    user=user.objects.get(pk=i.pk),
                    other_user=user.objects.get(pk=user_id),
                    forward_score=scores[1],
                    backward_score=scores[0],
                    combined_score=scores[2],
                )

# update_matches(239, Answer, User, Matching, pd, np)
# user = User.objects.get(username='boredPonie1-sim')
# print(user.pk)
