import json
from pathlib import Path
from datetime import datetime
database = "expense_tracker.json"
data = {"expenses" : []}



if Path(database).exists():
    with open(database,"r") as fs:
        content = fs.read()
        if content:
            data = json.loads(content)

def save():
    with open(database,"w") as fs:
        json.dump(data,fs,indent=4)

class Expense :

    def add_expense(self):
        name = input("Enter expense name: ")
        amount = input("Enter amount: ")
        category = input("Enter category: ")
        date_time = datetime.now().date()
        date_time = str(date_time)

        def get_id ():
            return len(data["expenses"])+1
        id = get_id()
        data["expenses"].append({
                "id" : id,
                "name" : name,
                "amount" : amount,
                "category" : category,
                "datetime" : date_time
               
            })
        save()

    def update_expense (self) :
        new_id = input("Enter new id: ")
        newname = input("Enter new name: ")
        newamout = input("Enter new amount: ")
        newcat = input("Enter new category")
        newdate = datetime.now().date()
        newdate = str(newdate)
        for exp in data["expenses"] :
            if exp["id"] == new_id:
                print(f"Task found name of task: {exp["name"]} ")
                exp["name"] = newname
                exp["amount"] =  newamout
                exp["category"] = newcat
                exp["date"] = newdate
        save()

     
addExpense = Expense()
updateExpense = Expense()

user = int(input("Enter a number"))


if user == 1:
    addExpense.add_expense()
elif user == 2:
    updateExpense.update_expense()