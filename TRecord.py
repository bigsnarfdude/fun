"""
Transaction Record Class
"""

__author__ = 'vincent'

import datetime

class Record(object):
    """
    Transaction record class pythonized values:
      * amount
      * company
      * date
      * ledger
    """

    def __init__(self, transaction_dict):
        self.string = transaction_dict
        self.amount = self._getAmount()
        self.company = self._getCompany()
        self.ledger = self._getLedger()
        self.date = self._getDate()

    def _getAmount(self):
        extracted_amount = self.string['Amount']
        converted_amount = float(extracted_amount)
        return converted_amount

    def _getDate(self):
        extract_date = self.string['Date']
        year = int(extract_date.split("-")[0])
        month = int(extract_date.split("-")[1])
        day = int(extract_date.split("-")[2])
        dt = datetime.datetime(year, month, day).date()
        return dt

    def _getCompany(self):
        return self.string['Company']

    def _getLedger(self):
        return self.string['Ledger']
