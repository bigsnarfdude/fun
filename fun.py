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
    cleaned_names = ProcessingTR.PTR.cleanWords(bunch_transactions)
    find_unique = ProcessingTR.PTR.removeDuplicates(cleaned_names)
    find_duplicates = ProcessingTR.PTR.findDuplicates(cleaned_names, find_unique)

    print
    print "---- Rest Test API Report --------"
    print "----------------------------------"
    print "Total number of transaction to process:", transaction_count
    print "----------------------------------"
    print "Total Balance is:", transaction_balance
    print "----------------------------------"
    print "Cleaning up company names"
    print "----------------------------------"
    print "Found duplicate:", find_duplicates
    print "----------------------------------"
    print ProcessingTR.PTR.categoryTotals(find_unique)
    print "----------------------------------"
    print ProcessingTR.PTR.getTransactionPerCategory(find_unique)
    print "----------------------------------"
    print "--------- End Report -------------"
