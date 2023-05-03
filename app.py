import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import datetime as dt

app = Flask(__name__)

# Replace this with your MongoDB Atlas connection string


class BudgetTracker:
    def __init__(self):
        mongodb_connection_string = "mongodb+srv://fthenosyd:ksz7WfkeoRy6XLHu@budgetcluster.9oayoit.mongodb.net/test"
        self.client = MongoClient(mongodb_connection_string)
        self.db  = self.client["BudgetCluster"]
        self.income = 1300
        self.rent = 340
        self.bills = 60
        self.gas = 100
        self.supermarket = 150
        self.entertainment = 150
        self.efood = 40
        self.others = 100
        self.car_installement = 180
        self.savings = 180
        
    def insert_expense(self, expense):
        self.db.daily_expenses.insert_one(expense)
    

    def initialize_budget(self):
        now = dt.datetime.now()
        month = now.month
        year = now.year
        budget_entry = {
            "month": month,
            "year": year,
            "income": self.income,
            "rent": self.rent,
            "bills": self.bills,
            "car_installement": self.car_installement,
            "gasoline": self.gas,
            "supermarket": self.supermarket,
            "efood": self.efood,
            "entertainment": self.entertainment,
            "other": self.others,
            "saving": self.savings,
        }
        self.db.budget.insert_one(budget_entry)
    
    def initialize_balance(self):
        now = dt.datetime.now()
        month = now.month
        year = now.year
        balance_entry = {
            "month": month,
            "year": year,
            "income": self.income,
            "rent": 0,
            "bills": 0,
            "car_installement": 0,
            "gasoline": 0,
            "supermarket": 0,
            "efood": 0,
            "entertainment": 0,
            "other": 0,
            "saving": 1300,
        }
        self.db.balance.insert_one(balance_entry)
    
    def budget_exists(self):
        now = dt.datetime.now()
        month = now.month
        year = now.year
        budget = self.db.budget.find_one({"month": month, "year": year})
        if budget is None:
            return False
        else:
            return True
    
    def balance_exists(self):
        now = dt.datetime.now()
        month = now.month
        year = now.year
        balance = self.db.balance.find_one({"month": month, "year": year})
        if balance is None:
            return False
        else:
            return True
    
    def update_balance(self, expenses):
        now = dt.datetime.now()
        month = now.month
        year = now.year

        month_balance = self.db.balance.find_one({"month": month, "year": year})
        
        if month_balance is None:
            month_balance = {
                "month": month,
                "year": year,
                "income": 1300,
                "rent": 0,
                "bills": 0,
                "car_installement": 0,
                "gasoline": 0,
                "supermarket": 0,
                "efood": 0,
                "entertainment": 0,
                "other": 0,
                "saving": 1300,
            }
            self.balance.insert_one(month_balance)
            month_balance = self.db.balance.find_one({"month": month, "year": year})

        total_expenses = 0
        for category in expenses:
            if category in month_balance:
                try: 
                    month_balance[category] += expenses[category]
                    total_expenses += expenses[category]
                except TypeError: # in case the category is ObjectID
                    continue
        month_balance["saving"] = month_balance["income"] - total_expenses
        self.db.balance.update_one({"month": month, "year": year}, {"$set": month_balance})
    
    def show_budget(self):
        now = dt.datetime.now()
        month = now.month
        year = now.year
        budget = self.db.budget.find_one({"month": month, "year": year})
        if budget is None:
            return "Error: Budget not initialized for this month."
        else:
            return budget
    
    def show_balance(self):
        now = dt.datetime.now()
        month = now.month
        year = now.year
        balance = self.db.balance.find_one({"month": month, "year": year})
        if balance is None:
            return "You have't registered any expenses yet."
        else:
            return balance
        
        
Tracker = BudgetTracker()


@app.route('/')
def index():
    if dt.datetime.now().day == 1:
        Tracker.initialize_budget()
        Tracker.initialize_balance()
    # Check if budget and balance exists (
    # maybe the first day of the month has passed and the budget has not been initialized yet)
    if not Tracker.budget_exists():
        Tracker.initialize_budget()
    if not Tracker.balance_exists():
        Tracker.initialize_balance()
    # Find the budget for the current month
    budget = Tracker.show_budget()
    balance = Tracker.show_balance()

    return render_template('index.html', date=dt.datetime.now(), budget=budget, balance=balance)


@app.route('/form', methods=['GET'])
def daily_expenses():
    return render_template('form.html', date=dt.datetime.now())

@app.route('/submit', methods=['POST'])
def submit():
    daily_expenses = {
        "date": dt.datetime.now(),
        "rent": float(request.form['rent']),
        "bills": float(request.form['bills']),
        "car_installements": float(request.form['car_installements']),
        "gasoline": float(request.form['gasoline']),
        "supermarket": float(request.form['supermarket']),
        "efood": float(request.form['efood']),
        "entertainment": float(request.form['entertainment']),
        "other": float(request.form['other']),
    }
    Tracker.insert_expense(daily_expenses)
    Tracker.update_balance(daily_expenses)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))