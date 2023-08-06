class Customer:
    def __init__(self, username, password, ID, email, contactNumber):
        self.username = username
        self.password = password
        self.ID = ID
        self.email = email
        self.contactNumber = contactNumber
        self.accounts = []

    def deposit(self, account, amount):
        pass

    def withdrawal(self, account, amount):
        pass

    def orderCheckbook(self, account):
        pass

    def requestBankStatement(self, account, start_date, end_date):
        pass

    def updatePersonalInfo(self, **kwargs):
        pass

    def changePassword(self, old_password, new_password):
        pass


class SingleUser(Customer):
    def __init__(self, username, password, ID, email, contactNumber, fullName, gender):
        super().__init__(username, password, ID, email, contactNumber)
        self.fullName = fullName
        self.gender = gender


class BusinessUser(Customer):
    def __init__(self, username, password, ID, email, contactNumber, location, companyName):
        super().__init__(username, password, ID, email, contactNumber)
        self.location = location
        self.companyName = companyName

    def updateCompanyDetails(self, **kwargs):
        pass


class Account:
    def __init__(self, accountNumber, accountHolder, balance):
        self.accountNumber = accountNumber
        self.accountHolder = accountHolder
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        pass

    def withdrawal(self, amount):
        pass

    def getTransactionHistory(self, start_date, end_date):
        pass


class CheckingAccount(Account):
    def __init__(self, accountNumber, accountHolder, balance, monthlyFee):
        super().__init__(accountNumber, accountHolder, balance)
        self.monthlyFee = monthlyFee

    def orderCheckbook(self):
        pass


class SavingsAccount(Account):
    def __init__(self, accountNumber, accountHolder, balance, interestRate):
        super().__init__(accountNumber, accountHolder, balance)
        self.interestRate = interestRate


class Transaction:
    def __init__(self, account, type, amount, timestamp):
        self.account = account
        self.type = type
        self.amount = amount
        self.timestamp = timestamp


class BankStatement:
    def __init__(self, account, start_date, end_date, transactions):
        self.account = account
        self.start_date = start_date
        self.end_date = end_date
        self.transactions = transactions

    def generateStatement(self):
        pass


class Checkbook:
    def __init__(self, checkbookNumber, dateIssued, dateExpired, checkbookStatus, account):
        self.checkbookNumber = checkbookNumber
        self.dateIssued = dateIssued
        self.dateExpired = dateExpired
        self.checkbookStatus = checkbookStatus
        self.account = account
