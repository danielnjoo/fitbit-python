# A python library for the FitBit API

Modified version of [magnific0's](https://github.com/magnific0/FitBit.py), which was a fork of [jpattel's](https://github.com/jplattel/FitBit.py)

Was in Authentication hell for hours, @FitBit API you suck

## Idea

Get summary activity/sleep/weight data from the FitBit API, requires setting up an [application](https://dev.fitbit.com/apps), most importantly set callback URL to `https://127.0.0.1:8080/`.

At the moment, pulls data from yesterday — because sleep data isn't updated till the morning after; note sleep cycles aren't given unless you've slept for more than 3 hours.

Previous [commit](https://github.com/danielnjoo/fitbit-python/commit/161a0d5f819ffa118b041f57722a86284f3829f9) pushed data to a [MongoDB](https://cloud.mongodb.com/) cluster (which is free for 500MB), and since each entry is ~200B, that's around 2.5M days worth). Personally, was planning on then pulling from MongoDB to a spreadsheet using a [Zapier integration](https://zapier.com/apps/google-sheets/integrations/mongodb). But connecting to MongoDB through Zapier was a pain, so currently uses [gspread](https://github.com/burnash/gspread/) to push to a Google Sheet.

## Usage

Install requirements `pip install -r requirements.txt`

- update `API_keys.json` with FitBit app ID/secret
- create Google Sheet and make sure edit access is given to anyone with link [explanation](https://stackoverflow.com/questions/38949318/google-sheets-api-returns-the-caller-does-not-have-permission-when-using-serve)
- update `get_data_and_push_to_GSheets.py` with your sheet's key
- enable Google Drive API and download credentials, [walkthru](https://gspread.readthedocs.io/en/latest/oauth2.html)
- run `get_data_and_push_to_GSheets.py`, first time requires FitBit authorization flow
