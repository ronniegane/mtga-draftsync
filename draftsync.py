import fetch
import upload
from pick import pick

def main():
    # All-in-one: grab from 17Lands, upload without writing to disk
    expansion = (
        input("Enter MTG set, or leave blank to default to MID: ") or "MID"
    )
    # Valid formats fetched from https://www.17lands.com/data/formats
    valid_formats = ["PremierDraft", "TradDraft", "QuickDraft", "CompDraft", "Sealed", "TradSealed", "CubeDraft", "CubeSealed", "DraftChallenge", "OpenSealed_D1_Bo1", "OpenSealed_D1_Bo3", "OpenSealed_D2_Bo3"]
    pick_title = "Choose a draft type to fetch ratings for"
    format = pick(valid_formats, pick_title)[0]

    # Grab data from 17Lands
    rawRatings = fetch.fetch17LandsRatings(expansion, format)
    cardRatings = fetch.convert17LandsRatings(rawRatings)

    # Upload to MTGAHelper endpoint
    userId = input("Enter your MTGAHelper user ID (from your Profile page):")
    upload.put(userId, cardRatings)


if __name__ == "__main__":
    main()
