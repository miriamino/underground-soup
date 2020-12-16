from django.db import connection

import pandas as pd 
from .models import Answer


query = str(Answer.objects.all().query)
df = pandas.read_sql_query(query, connection)
print(df.head())
