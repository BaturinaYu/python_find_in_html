# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies2103

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            salary = item['salary']
        else:
            salary = self.salary_sjru(item['salary'])

        item['min'], item['max'], item['cur'], item['comment'] = self.process_salary(salary)
        #del item['salary']

        collection = self.mongobase[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        new_sal = []
        key = ''
        comment = None
        for el in salary:
            if el == ' ':
                continue
            el = el.replace('\u202f', '')
            el = el.replace('\xa0', '')
            if el.isdigit():
                key += '1'
            else:
                key += '0'
            new_sal.append(el)

        if key.find('1') != key.rfind('1'):
            min_ = new_sal[key.find('1')]
            max_ = new_sal[key.rfind('1')]
        else:
            if (key.find('1') == 0) or (new_sal[0].find('до') != -1):
                min_ = None
                max_ = new_sal[key.find('1')]
            else:
                min_ = new_sal[key.find('1')]
                max_ = None
        v_ind = key.rfind('1') + 1
        val = new_sal[v_ind]
        if v_ind != len(new_sal) - 1:
            comment = new_sal[-1]

        return min_, max_, val, comment

    def salary_sjru(self, salary):
        comment = salary[-1]
        str_sal = ' '.join(salary[:-1])
        str_sal = str_sal.replace('\xa0', '')

        fl = str_sal[0].isdigit()
        dgs = []
        s = ''
        for i in str_sal:
            if not i.isdigit():
                if fl:
                    dgs.append(s)
                    fl = False
                    s = ''
                else:
                    continue
            else:
                fl = True
                s += i
        salary = list(str_sal.rpartition(dgs[-1])) + [comment]

        return salary