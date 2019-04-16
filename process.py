import json, pymongo
from datetime import datetime, timedelta

try:
    data = json.load(open('mongodb_user.json'))
    mongoUser = data["userID"]
    mongoPW = data["pw"]
    mongoCluster = data['cluster']
except IOError:
    print("\nFile does not exist\n")

# pip install pymongo[srv] required to support srv: https://github.com/mongodb/mongo-python-driver/blob/master/doc/installation.rst
client = pymongo.MongoClient(f"mongodb+srv://{mongoUser}:{mongoPW}@{mongoCluster}.mongodb.net/test?retryWrites=true")

# access or crate fitbit collection, lazily created once first documents inserted
db = client.fitbit

now = datetime.now()
yest = now - timedelta(days=1)
date = yest.strftime("%Y-%m-%d")

print('\nProcessing yesterday\'s data\n')

desired = {'date': date}

with open(f'data/{date}.json') as file:
    data = json.loads(file.read())
    desired.update(
        caloriesOut=data['summary']['caloriesOut'],
        activityCalories=data['summary']['activityCalories'],
        restingHeartRate=data['summary']['restingHeartRate'],
        sedentaryMinutes=data['summary']['sedentaryMinutes'],
        steps=data['summary']['steps']
    )
with open(f'data/{date}-sleep.json') as file:
    data = json.loads(file.read())
    if data['sleep']:
        desired.update(
          duration=data['sleep'][0]['duration'],
          efficiency=data['sleep'][0]['efficiency']
        )
    if desired['duration'] > 10800000 : # > 3 H so have stage data
        desired.update(
        deep = data['summary']['stages']['deep'],
        light = data['summary']['stages']['light'],
        rem = data['summary']['stages']['rem'],
        wake = data['summary']['stages']['wake']
        )
    else:
        print('\nNo sleep data\n')
with open(f'data/{date}-weight.json') as file:
    data = json.loads(file.read())
    if data['weight']:
        desired.update(
            weight=data['weight'][0]['weight']
        )
    else:
        print('\nNo weight data\n')

print("Final data looks like:\n", desired)

existingEntry = list(db.data.find({'date':date}))
if existingEntry:
    print("\nThere is an existing entry for this date, overwrite? Y/N\n")
    input = input().upper()
    if input == "Y":
        result = db.data.find_one_and_replace({'date':date}, desired)
        if result:
            print("\nSuccessfully replaced")
    elif input == "N":
        print("\n")
    else:
        print("\nInvalid")
else:
    result = db.data.insert_one(desired)
    if result:
        print(result.inserted_id)
        print("\nSuccessfully inserted")
    else:
        print("Problem, probably")
