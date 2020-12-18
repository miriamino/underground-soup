import random
from dating.models import Answer, User, Matching, Question, Choice
from django.contrib.auth.models import User
from faker import Faker
from random_username.generate import generate_username
fake = Faker()

# for i in range(200):
#     name = f'{generate_username()[0]}-sim'
#     email = fake.ascii_email()
#     password = generate_username()
#     print(name)
#     user = User.objects.create_user(name, email, email)

# users = User.objects.all().filter(username__iendswith='-sim')
# print([u.pk for u in users])
# questions = Question.objects.all().order_by('-pub_date')[:5]
# print([q.pk for q in questions])
# q = Question.objects.get(pk=1556)
# choices = q.choice_set.all()
# choice_set = [c.pk for c in choices]
# answer_self = random.choice(choice_set)
# answer_other = random.sample(choice_set, random.randint(1, len(choice_set)))
# importance_set = [0,1,50,250, 300]
# importance = random.choice(importance_set)
# public_other = random.choices([0,1], [0.2, 0.8])
# public_self = random.choices([0,1], [0.2, 0.8])


# for u in users:
#     for q in questions:
#         que = Question.objects.get(pk=q.pk)
#         choices = q.choice_set.all()
#         choice_set = [c.pk for c in choices]
#         importance_set = [0,1,50,250, 300]
#         answer = Answer.objects.create(
#             user=u,
#             question=que,
#             answer_self=Choice.objects.get(pk=random.choice(choice_set)),

#             importance=random.choice(importance_set),
#             public_self=random.choices([False,True], [0.2, 0.8])[0],
#             public_other=random.choices([False,True], [0.2, 0.8])[0],
#         )
#         ao=random.sample(choice_set, random.randint(1, len(choice_set)))
#         for c in ao:
#             answer.answer_other.add(q.choice_set.get(pk=c))