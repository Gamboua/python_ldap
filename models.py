from os import path
from flask import Flask
from flask_mongoengine import MongoEngine
from ldap import initialize, LDAPError
from ldap.modlist import addModlist
from yaml import load
from uuid import uuid4
from hashlib import md5
from binascii import b2a_base64
from flask_login import UserMixin

import logging



app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {"db":"auth"}
db = MongoEngine(app)


class User(db.Document):
    nome = db.StringField()
    sobrenome = db.StringField()
    email = db.StringField()
    passwd = db.StringField()
    data_login = db.DateTimeField()

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @staticmethod
    def get(email):
        return User.objects(email=email)

class Ldap:

    def __init__(self):
        try:
            with open(path.dirname(path.abspath(__file__)) + 'config.yml','r') as yml:
                self.config = load(yml)['ldap']
            self.ldap = initialize("ldap://%s" % self.config['server'])
            self.ldap.bind(self.config['user'], self.config['password'])
        except IOError as e:
            logging.error(e)
        except LDAPError as e:
            logging.error(e)

    def insert(self, user):
        try:
            ldif = addModlist(self.ldifuser(user))
            cn = str("mail=" + user.email.encode('utf-8') + self.config['cn'])
            self.ldap.add_s(cn, ldif)
        except LDAPError as e:
            logging.error(e)
        except Exception as e:
            logging.error(e)

    def ldifuser(self, user):
        ldiuser = {}

        ldiuser['sn'] = user.nome.encode('utf-8')
        ldiuser['cn'] = user.nome.encode('utf-8')
        ldiuser['mail'] = user.nome.encode('utf-8')
        ldiuser['objectClass'] = ['top', 'person', 'organizationalPerson', 'inetOrgPerson', 'posixAccount']

        ldiuser['userPassword'] = user.passwd

        ldiuser['uid'] = user['email'].encode('utf-8')

        return ldiuser

    @staticmethod
    def pass_generate():
        return "{MD5}" + b2a_base64(md5(str(uuid4()).encode('utf-8')).digest())