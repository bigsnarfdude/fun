"""
Processing Transaction Records Library
"""

__author__ = 'vincent'

import urllib2

class PTR:
    """
    Methods to process TRecords
    """

    @staticmethod
    def getData(url):
        #url_1 = 'http://resttest.bench.co/transactions/1.json'
        #url_2 = 'http://resttest.bench.co/transactions/2.json'
        #url_3 = 'http://resttest.bench.co/transactions/3.json'
        #url_4 = 'http://resttest.bench.co/transactions/4.json'
        #data_pages = [url]
        #data_strings = defaultdict()
        #for page in data_pages:
        data_strings = urllib2.urlopen(url).read()
        #data_frames = defaultdict()
        #for k,v in data_strings.iteritems():
        #    data_frames[k] = pd.io.json.read_json(v)
        #combined_df = pd.concat(data_frames)
        return data_strings

    @staticmethod
    def processTransactions(combined_df):
        bunch_transactions = []
        for item in combined_df['transactions']:
            bunch_transactions.append(TRecord(item))
        return bunch_transactions

    @staticmethod
    def totalCount(bunch_transactions):
        return len(bunch_transactions)

    @staticmethod
    def getObjects(combined_df):
        bunch_transactions = []
        for item in combined_df['transactions']:
            bunch_transactions.append(TRecord(item))
        return bunch_transactions

    @staticmethod
    def totalBalance(bunch_transactions):
        balance = 0.0
        for item in bunch_transactions:
            balance += item.amount
        return balance

    @staticmethod
    def cleanNames(bunch_transactions):
        temp = Set()
        for item in bunch_transactions:
            temp.add(" ".join(item.company().split()[0:2]))
        return temp

    @staticmethod
    def findDuplicates(transactions):
        try:
            for i in range(len(transactions)):
                a = transactions[i]
                b = transactions[i+1]
                if a.company() == b.company():
                    if a.date() == b.date():
                        if a.amount() == b.amount():
                            return transactions[i].s
        except:
            pass

    @staticmethod
    def categoryTotals(transactions):
        expense_categories = defaultdict(list)
        for i in transactions:
            expense_categories[i.ledger()].append(i)
        for cat, values in expense_categories.iteritems():
            print cat, TransactionProcessing.totalBalance(values)

    @staticmethod
    def getTransactionPerCategory(transactions):
        expense_categories = defaultdict(list)
        for i in transactions:
            expense_categories[i.ledger()].append(i)
        for cat, values in expense_categories.iteritems():
            print cat, [x.s for x in values]
