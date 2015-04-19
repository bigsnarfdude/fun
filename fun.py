"""
Resttest API library
"""

__author__ = 'vincent'

import sys
import ProcessingTR

if __name__ == "__main__":
    for arg in sys.argv: 1

    raw_data = ProcessingTR.PTR.getData(arg)
    bunch_transactions = ProcessingTR.PTR.processTransactions(raw_data)
    transaction_count = ProcessingTR.PTR.totalCount(bunch_transactions)
    transaction_balance = ProcessingTR.PTR.totalBalance(bunch_transactions)

    print "Total number of transaction to process:", transaction_count
    print "Total Balance is:", transaction_balance
