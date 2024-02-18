import random, tweepy, time, schedule
from nba_api.stats.static import players

# Enter API tokens below
bearer_token = '' # not needed for this
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

#tweeting part
def tweet():
    # gets the players names from the nba_api
    nba_players = players.get_players()


    active_players = [player for player in nba_players if player['is_active']]


    random_active_player = random.choice(active_players)
    random_active_player2 = random.choice(active_players)

    player1 = random_active_player['full_name']
    player2 = random_active_player2['full_name']
    # Text to be Tweeted
    text = "Who is the better player?"
    poll_options = [player1,player2]
    # Send Tweet with Text and poll options
    client.create_tweet(text=text,poll_options = poll_options,poll_duration_minutes=1440) 
    print("Tweeted!")
    
schedule.every().hour.do(tweet)# tweets every hour
while True:
    schedule.run_pending()
    time.sleep(1)
