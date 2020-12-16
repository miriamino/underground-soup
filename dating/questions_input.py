import pandas as pd
from dating.models import Question, Choice
from django.utils import timezone

df1 = pd.read_csv('dating/static/dating/data/my_questions.csv')
df2 = pd.read_csv('dating/static/dating/data/okc_questions.csv')


df2 = df2.set_index('text')

df2 = df2.stack()

df2 = df2.reset_index()

del df2['level_1']

df2.columns = ['Question', 'Choice']

frames = [df1, df2]
ds = pd.concat(frames)

que = ds['Question'].unique()

questions = []
for q in que:
    item = Question(question_text=q, pub_date=timezone.now())
    questions.append(item)

Question.objects.bulk_create(questions)

choices = []
for index, row in ds.iterrows():
    question = Question.objects.get(question_text=row['Question'])
    item = Choice(choice_text=row['Choice'], question_id=question.pk)
    choices.append(item)

Choice.objects.bulk_create(choices)
