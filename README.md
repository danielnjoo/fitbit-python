# A python library for the FitBit API

Modified version of [magnific0's](https://github.com/magnific0/FitBit.py), which was a fork of [jpattel's](https://github.com/jplattel/FitBit.py)

Was in Authentication hell for hours, @FitBit API you suck

## Idea

Get summary activity/sleep/weight data from the FitBit API, requires setting up an [application](https://dev.fitbit.com/apps), most importantly set callback URL to `https://127.0.0.1:8080/`.

At the moment, pulls data from yesterday — because sleep data isn't updated till the morning after... it's also does not detail sleep cycles unless you've slept for more than 3 hours.

This pushes data to a [MongoDB](https://cloud.mongodb.com/) cluster (which is free for 500MB), and since each entry is ~200B, that's around 2.5M days worth). Personally, was planning on then pulling from MongoDB to a spreadsheet using a [Zapier integration](https://zapier.com/apps/google-sheets/integrations/mongodb).

## Usage

Install requirements `pip install -r requirements.txt`

Update `API_keys.json` with FitBit app ID/secret, and `mongodb_user.json` with MongoDB info.

Run `get_data.py` then `process.py`
