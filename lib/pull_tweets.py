import twitter
import yaml
import pymongo
import pandas as pd

def connect_to_mongo():
    client_aws = pymongo.MongoClient(host='52.39.42.122', port=27017)
    client_aws.database_names()
    database = client_aws.twitter
    print(database.collection_names())
    return database

def get_twitter_client():
    stream = open("credentials.yml", "r")
    docs = yaml.load_all(stream)
    creds = docs.next()
    auth = twitter.oauth.OAuth(creds['creds']['access_token'],
                               creds['creds']['access_secret'],
                               creds['creds']['consumer_token'],
                               creds['creds']['consumer_secret'])
    return twitter.Twitter(auth=auth)

def get_user_tweets(screen_name):
    
    access_key =  '823714388905336832-Vk8UvBNUR7VodGhHzdKEmK5GNs3ULxB'
    access_secret = 'XK86kGwlp4zwDzxYhYc2oHu0qJIE11uRp83Ex6TUg4JCg'
    consumer_token =  'N5dNhpdbhfLbn5Z94XyRVpr3I'
    consumer_secret = 'G8CfW44BA1mofPBh3bP0gRGp6hokuw5h3PlZCUkPRYMccyYznE'
    
    auth = OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []    
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    user=api.get_user(screen_name=screen_name)
    oldest = alltweets[-1].id - 1
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name = screen_name, count=200,max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
    return alltweets

def get_texts_and_user(user):
    tweets = get_user_tweets(user)
    return pd.concat([pd.DataFrame([[i.user.screen_name, i.text]], columns=['user','text']) for i in tweets],axis=0).reset_index(drop=True)

    
def select_all_tweets(screen_name):

    client_aws = pymongo.MongoClient(host='52.39.42.122', port=27017)
    database = client_aws.twitter
    coll = database.screen_name
    cur = coll.find()
    all = list (cur)
    all_df = pd.DataFrame(all)
    new_df = all_df[['text', 'user']]
    print new_df    

