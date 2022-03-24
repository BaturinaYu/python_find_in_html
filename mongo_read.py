from pymongo import MongoClient
from pprint import pprint as pp

client = MongoClient('localhost', 27017)
db = client.vacancies2103
vacancy_coll = db.hhru
#vacancy_coll.delete_many({})
col = 0
for i in vacancy_coll.find({}):
    col += 1
    pp(i)

print(col)
