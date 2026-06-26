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
                "amount" : f"${amount}",
                "category" : category,
                "datetime" : date_time,
                "date" : "No Update"
            })
        save()

    def update_expense (self) :
        new_id = int(input("Enter new id: "))
        newname = input("Enter new name: ")
        newamout = input("Enter new amount: ")
        newcat = input("Enter new category")
        newdate = datetime.now().date()
        newdate = str(newdate)
        for exp in data["expenses"] :
            if exp["id"] == new_id :
                exp["name"] = newname
                exp["amount"] =  f"${newamout}"
                exp["category"] = newcat
                exp["updatedate"] = newdate
                print(f"Task found name of task: {exp["name"]} and updated ")
                save()

    def delete_expense (self) :
        id = int(input("Enter expense id: "))
        for i in data["expenses"] :
            if i["id"] == id:
                print(f"Expense found: {i["name"]}")
                data["expenses"].remove(i)
                save()
    
    def view_expense (self) :
        print("ID | Name | Amount | Category | Creation Date | Updation Date ")
        for i in data["expenses"] :
            print(f"{i["id"]} | {i["name"]} | {i["amount"]} | {i["category"]} | {i["datetime"]} | {i["date"]}")

    def summery_expense (self) :
        for i in data["expenses"] :
            print(f"{i["id"]} : id, name of exp {i["name"]}, with price of {i["amount"]} in cat {i["category"]}")

addExpense = Expense()
updateExpense = Expense()
deleteExpense = Expense()
viewExpense = Expense()
summeryExpense = Expense()

user = int(input("Enter a number"))


if user == 1:
    addExpense.add_expense()
elif user == 2:
    updateExpense.update_expense()
elif user == 3:
    deleteExpense.delete_expense()
elif user == 4:
    viewExpense.view_expense()
elif user == 5:
    summeryExpense.summery_expense()