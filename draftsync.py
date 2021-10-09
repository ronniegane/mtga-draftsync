import fetch
import upload


def main():
    # All-in-one: grab from 17Lands, upload without writing to disk
    expansion = "MID"
    format = "PremierDraft"
    # Grab data from 17Lands
    rawRatings = fetch.fetch17LandsRatings(expansion, format)
    cardRatings = fetch.convert17LandsRatings(rawRatings)

    # Upload to MTGAHelper endpoint
    userId = input("Enter your MTGAHelper user ID (from your Profile page):")
    upload.put(userId, cardRatings)


if __name__ == "__main__":
    main()
