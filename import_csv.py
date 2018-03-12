from models import User, Ldap
import csv


with open('users.csv', 'rb') as f:
    rows = list(csv.reader(f))

for r in rows:
    user = User()

    user.nome = r[0]
    user.sobrenome = r[1]
    user.email = r[2]
    user.passwd = Ldap.pass_generate()

    userldap = Ldap()
    userldap.insert(user)

    user.save()
