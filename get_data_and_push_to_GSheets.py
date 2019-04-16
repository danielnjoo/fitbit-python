import fitbit, json, gspread
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

tokenfile = "user_settings.txt"
z = fitbit.Fitbit();

# Try to read existing token pair
try:
    token = json.load(open(tokenfile))
except IOError:
    # If not generate a new file
    # Get the authorization URL for user to complete in browser.
    auth_url = z.GetAuthorizationUri()
    print ("Please visit the link below and approve the app:\n %s" % auth_url) ## CHANGES MADE HERE
    # Set the access code that is part of the arguments of the callback URL FitBit redirects to.
    access_code = input("Please enter code (from the URL you were redirected to): ")
    # Use the temporary access code to obtain a more permanent pair of tokens
    token = z.GetAccessToken(access_code)
    # Save the token to a file
    json.dump(token, open(tokenfile,'w'))

# Sample API call
response = z.ApiCall(token, '/1/user/-/profile.json')

# Token is part of the response. Note that the token pair can change when a refresh is necessary.
# So we replace the current token with the response one and save it.
token = response['token']
json.dump(token, open(tokenfile,'w'))

# Do something with the response
print ("\nWelcome %s!\n" % response['user']['displayName'])

now = datetime.now()
yest = now - timedelta(days=1)
date = yest.strftime("%Y-%m-%d")

print('\nDownloading yesterday\'s data\n')

# empty dict to deal with missing data later
desired = {
    'date': date,
    'caloriesOut': None,
    'activityCalories': None,
    'restingHeartRate': None,
    'sedentaryMinutes': None,
    'steps': None,
    'duration': None,
    'efficiency': None,
    'weight': None,
    'deep': None,
    'light': None,
    'rem': None,
    'wake': None
}

data = z.ApiCall(token, f'/1/user/-/activities/date/{date}.json')
desired.update(
    caloriesOut=data['summary']['caloriesOut'],
    activityCalories=data['summary']['activityCalories'],
    restingHeartRate=data['summary']['restingHeartRate'],
    sedentaryMinutes=data['summary']['sedentaryMinutes'],
    steps=data['summary']['steps']
)

data = z.ApiCall(token, f'/1/user/-/body/log/weight/date/{date}.json')
if data['weight']:
    desired.update(
        weight=data['weight'][0]['weight']
    )
else:
    print('\nNo weight data\n')

data = z.ApiCall(token, f'/1/user/-/sleep/date/{date}.json')
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


print("\nData looks like this\n",desired,"\n")

scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_key('___gsheetURL___')
worksheet = sh.get_worksheet(0)

worksheet.insert_row(list(desired.values()),index=2)
