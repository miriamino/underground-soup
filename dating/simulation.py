from dating.models import Answer, User, Matching, Question
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
# questions = Question.objects.order_by('?')[:200]
# print([q.pk for q in questions])
choices = Question.choice_set(pk=154)
print(choices)
# answer = Answer.objects.create(
#     user=
#     question=
#     answer_self=
#     answer_other=
#     importance=
#     public_self=
#     public_other=
#     answer_date=
# )