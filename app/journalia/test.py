__author__ = 'rizkivmaster'


import unittest
import datetime
import random
from controllers import Record, recordAccessor

def randomId():
    return random.randint(0,10000)

class RecordAccessorTest(unittest.TestCase):
    def test_add(self):
        record = Record(date=datetime.date.today(),accountingId=str(randomId()),accountingPost='KASIR',accountingType='KREDIT',notes='Test'+str(randomId()),amount=randomId())
        recordAccessor.addRecord(record)
        result = recordAccessor.getRecordById(record.accountingId)
        assert(not result == None)
        del(result)
        result = recordAccessor.getRecordById(record.accountingId)
        result.amount = 4000
        recordAccessor.updateRecord(result)

    def test_getall(self):
        for ii in range(1,10):
            posts = ['KASIR','PENJUALAN','BELANJA']
            record = Record(date=datetime.date.today(),accountingId=str(randomId()),accountingPost=posts[ii %3],accountingType='KREDIT',notes='Test'+str(randomId()),amount=randomId())
            recordAccessor.addRecord(record)
        records = recordAccessor.getAllRecords('KASIR')
        assert(records!=None)


if __name__ == '__main__':
    unittest.main()