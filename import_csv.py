from models import Users
import csv


with open('users.csv', 'rb') as f:
    rows = list(csv.reader(f))

for r in rows:
    user = Users()

    user.name = r[0]
    user.sobrenome = r[1]
    user.email = r[2]
    user.save()
