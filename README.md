# MTGA DraftSync
_Synchronize MTG Arena draft assistants with the latest crowdsourced card ratings_

Are you tired of having your draft overlay showing you obsolete, prerelease rathings of cards that don't reflect the meta?

Tired of having to alt-tab out to 17Lands or your own spreadsheet to check every card?

Now you can update all your custom card ratings at once, from 17Lands' latest data or from any CSV file.

# Using the tool
Sign up for an MTGAHelper account and install the overlay if you haven't already.

You'll need your user ID which can be found on your profile page: https://mtgahelper.com/profile

Install Python3 and then the requirements:
`pip install -r requirements.txt`

## Upload your own CSV
DraftSync will accept any CSV as long as it has the following fields:
- **idArena** : this is the 5-digit id that MTG Arena uses for their cards
- **rating** : a 0-10 score for how good the card is
- **note** : free-text field for you to put whatever you like: personal opinions, in-colour or sideboard winrates, etc

You can have other fields in the CSV for ease of use when reading it (I usually have card name, set name, and colour), but they aren't used by the script.

Having cards from different sets in the same CSV is fine, just keep in mind that the more cards you have the longer it will take.

Call `python draftsync.py`

Enter your CSV filename

Enter your MTGAHelper user ID

wait... (currently uploads are 1-by-1 so can take some time)

Done! Start up MTGAHelper, open MTG Arena, and get drafting!

# Acknowledgements
Thanks to [this reddit thread](https://www.reddit.com/r/lrcast/comments/pr8cf9/best_way_to_take_advantage_of_17lands_data_in/) and [this .NET solution](https://github.com/LazarQt/LimitedPower.DraftHelperSync) by [LazarQt](https://github.com/LazarQt) for the inspiration.

Thanks to the guys at https://mtgarenahelper.com for making such an awesome tool! Support them on Patreon to help keep things running: https://www.patreon.com/mtgahelper
