import fitbit, json, datetime

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

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

summaryData = z.ApiCall(token, f'/1/user/-/activities/date/{date}.json')
json.dump(summaryData, open(f'{date}.json','w'), indent=4)
weightData = z.ApiCall(token, f'/1/user/-/body/log/weight/date/{date}.json')
json.dump(weightData, open(f'{date}-weight.json','w'), indent=4)
sleepData = z.ApiCall(token, f'/1/user/-/sleep/date/{date}.json')
json.dump(sleepData, open(f'{date}-sleep.json','w'), indent=4)
