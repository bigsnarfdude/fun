"""
Processing Transaction Records Library
"""

__author__ = 'vincent'

import re
import requests
from collections import defaultdict
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
    def cleanWords(bunch_transactions):
        cleaned_names = []
        for item in bunch_transactions:
            stripped = re.sub(r'.x+\d{4}', '', item.company)
            stripped_again = re.sub(r'CA x*\d+.\d+ USD @', "", stripped)
            item.company = stripped_again
            cleaned_names.append(item)
        return cleaned_names


    @staticmethod
    def removeDuplicates(transactions):
        seen = set()
        index = range(len(transactions))
        for i in index:
            for j in index[1:]:
                if transactions[index[i]].company == transactions[index[j]].company:
                    if transactions[index[i]].date == transactions[index[j]].date:
                        if transactions[index[i]].amount == transactions[index[j]].amount:
                            if transactions[index[i]] not in seen:
                                seen.add(transactions[index[i]])
        return seen


    @staticmethod
    def findDuplicates(transactions, seen):
        for val in transactions:
            if val in seen:
                return val.string


    @staticmethod
    def categoryTotals(transactions):
        expense_categories = defaultdict(list)
        for i in transactions:
            expense_categories[i.ledger].append(i)
        for cat, values in expense_categories.iteritems():
            print cat, PTR.totalBalance(values)


    @staticmethod
    def getTransactionPerCategory(transactions):
        expense_categories = defaultdict(list)
        for i in transactions:
            expense_categories[i.ledger].append(i)
        for cat, values in expense_categories.iteritems():
            print cat, [x.string for x in values]
