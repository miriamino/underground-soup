from django.db import connection

import pandas as pd

from dating.models import Answer

qu = Answer.objects.all().prefetch_related('answer_other')
# qt = str(qu.query)

data = [
    {
        'id': q.pk, 
        'user_id': q.user_id, 
        'question': q.question_id, 
        'answer_self': q.answer_self_id,
        'importance' : q.importance,
        'public_self' : q.public_self,
        'public_other' : q.public_other,
        'answer_other': [t.id for t in q.answer_other.all()]}
    for q in qu
]
final_df= pd.DataFrame(
    data, 
    columns=[
        'id',
        'user_id', 
        'question', 
        'importance',
        'public_self',
        'public_other',
        'answer_self',
        'answer_other'])

print(final_df)
