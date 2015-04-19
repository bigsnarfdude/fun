"""
Processing Transaction Records Library
"""

__author__ = 'vincent'

import requests
from TRecord import Record

class PTR:
    """
    Methods to process TRecords
    """

    @staticmethod
    def getData(url):
        """
        function will take initial url requested and
        increment requests to size of totalCount
        :param url:
        :return list of transactions:
        """
        prefix = "/".join(url.split("/")[0:-1])
        returned_transactions = []
        transaction_counter = 0

        def _inner_get(url, returned_transactions, transaction_counter):
            """
            recursive function to paginate rest
            :param url:
            :param returned_transactions:
            :param transaction_counter:
            :return _inner_get(url, returned_transactions, transaction_counter):
            """
            try:
                r = requests.get(url)
                current_page = r.json()['page']
                current_balance = r.json()['totalBalance']
                current_count = r.json()['totalCount']
                current_transactions = r.json()['transactions']
                length_current_transactions = len(current_transactions)
                if transaction_counter < int(current_count):
                    page = int(current_page) + 1
                    requested_url = prefix+"/"+str(page)+".json"
                    returned_transactions += current_transactions
                    transaction_counter += length_current_transactions
                    return _inner_get(requested_url, returned_transactions, transaction_counter)
            except:
                pass

        _inner_get(url, returned_transactions, transaction_counter)

        return returned_transactions


    @staticmethod
    def processTransactions(raw_data):
        bunch_transactions = []
        for data_dict in raw_data:
            bunch_transactions.append(Record(data_dict))
        return bunch_transactions

    @staticmethod
    def totalCount(bunch_transactions):
        return len(bunch_transactions)

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
