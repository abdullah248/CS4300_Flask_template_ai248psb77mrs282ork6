import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

# Followed tutorial from
# https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'Ki0UkdeDOeLU1fc4HCcFdyn7o'
        consumer_secret = 'N0cSZ0vVCh2SNKndHBaWRys1sfMGD1Ti17dqIoq2kt3kCyqB1T'
        access_token = '1120165913855131648-j4ZcZBI9AJ4AATMqWmuiVHOGiAKcqx'
        access_token_secret = 'dj705NHkHNmnTzQhNZxsqi73EWawVMzNVG70s86TbhCtm'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        #return analysis.sentiment.polarity
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count, tweet_mode = 'extended' )
            # print(fetched_tweets)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.full_text
                # print(tweet.full_text)
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def runTwitterAnalysis(nameOfCandidate):
    api = TwitterClient()
    tweets = api.get_tweets(query = nameOfCandidate, count = 200)

    if not tweets:
        return 0, 0, 0

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    neutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']



    percentPos = 100*len(ptweets)/len(tweets)
    percentNeg = 100*len(ntweets)/len(tweets)
    percentNeu = 100*len(neutweets)/len(tweets)

    if percentPos >= percentNeg and percentPos >= percentNeu:
        twee = ptweets[0]['text']

    elif percentNeu >= percentNeg and percentNeu >= percentPos:
        twee = ntweets[0]['text']

    elif percentNeg >= percentPos and percentNeg >= percentNeu:
        twee = neutweets[0]['text']
    # percentNet = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)

    return round(percentPos,2), round(percentNeg,2), round(percentNeu,2), twee

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = 'Larry Hogan', count = 200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

#if __name__ == "__main__":
    # calling main function
#    main()
