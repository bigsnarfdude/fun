"""
Resttest API library
"""

__author__ = 'vincent'

import TRecord
#import ETLData
import ProcessingTR
import sys
import json

if __name__ == "__main__":
    for arg in sys.argv: 1
    raw_data = ProcessingTR.PTR.getData(arg)
    parsed_json = json.loads(raw_data)
    bunch_transactions = []
    for item in parsed_json['transactions']:
        a = TRecord.Record(item)
        bunch_transactions.append(a)
    print "Total Balance for API request is:", ProcessingTR.PTR.totalBalance(bunch_transactions)

'''
combined_df = TransactionProcessing.getData()
transactions = TransactionProcessing.processTransactions(combined_df)
print "Total number of transaction to process: ", TransactionProcessing.totalCount(transactions)
print "Total Balance is: ", TransactionProcessing.totalBalance(transactions)
print "List of Vendors: "
for vendor in TransactionProcessing.cleanNames(transactions):
    print vendor
print "Duplicate transaction found: ", TransactionProcessing.findDuplicates(transactions)
print TransactionProcessing.categoryTotals(transactions)
print TransactionProcessing.getTransactionPerCategory(transactions)
'''
