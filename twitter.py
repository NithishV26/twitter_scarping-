
#importing necessary libraries
import snscrape.modules.twitter as sntwitter
import pymongo
import streamlit as st
import json
import csv
from datetime import datetime, timedelta

#connect to the mongodb
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["twitter_scraping_db"]

#function to scrape the twitter data
def twitter_scraping(hashtag, start_date, end_date):
    data = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(hashtag).get_items()):
        if i<1000:
            break
        data.append({ 'Date':tweet.date,
                      'Id':tweet.id,
                      'URL':tweet.url,
                      'Content':tweet.rawContent,
                      'UserName':tweet.user.username,
                      'ReplyCount':tweet.replyCount,
                      'ReTweet':tweet.retweetCount,
                      'Language':tweet.lang,
                      'Source':tweet.source,
                      'LikeCount':tweet.likeCount
                   })
    print(data)    
    db.twitterdata.insert_many(data)
    st.success("Twitter Data Scraped Successfully")

#creating GUI using streamlit
st.title("Twitter Scraping")

#getting hashtag to scrape
hashtag = st.text_input("Enter the Hash tag")

#getting the date range
start_date = st.date_input("Enter the Start Date")
end_date = st.date_input("Enter the End Date")

#scrape data button
if st.button("Scrape Data"):
    twitter_scraping(hashtag, start_date, end_date)

#display the data
tweets_data = db.twitterdata.find()
st.write(tweets_data)

#download data
if st.button("Download Data"):
    with open("tweets_data.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["date", "id", "url", "tweet_content", "user", "reply_count", "retweet_count", "language", "source", "like_count"])
        for tweet in tweets_data:
            csv_writer.writerow([tweet["date"], tweet["id"], tweet["url"], tweet["tweet_content"], tweet["user"], tweet["reply_count"], tweet["retweet_count"], tweet["language"], tweet["source"], tweet["like_count"]])
    with open("tweets_data.json", "w") as json_file:
        json.dump(tweets_data, json_file)
    st.success("Data Downloaded Successfully")