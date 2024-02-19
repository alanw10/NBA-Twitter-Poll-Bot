import random
import tweepy

from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

# Enter API tokens below
bearer_token = ''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)


    # fetch NBA players
nba_players = players.get_players()

    # filter active players
active_players = [player for player in nba_players if player['is_active']]

    # variables
selected_players = []
players_found = 0

# loop until we find two players who average more than 15 minutes per game
while players_found < 2:
    # choose a random active player
    random_active_player = random.choice(active_players)

    # extract player ID
    player_id = random_active_player['id']
    player_name = random_active_player['full_name']

    # fetch career stats for the player
    player_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_stats = player_stats.get_dict()

    # check if the player has played in the 2023-24 season
    for dataset in career_stats['resultSets']:
        if dataset['name'] == 'SeasonTotalsRegularSeason':
            for row in dataset['rowSet']:
                if row[1] == '2023-24':
                    total_minutes = row[8]  # Total minutes played
                    games_played = row[6]    # Total games played
                    average_minutes_2023_24 = total_minutes / games_played
                            
                    # If the player averages more than 15 minutes, save them to list
                    if average_minutes_2023_24 > 15:
                        selected_players.append(player_name)
                        players_found += 1
                        break
            
    # lets us know the progress
    if average_minutes_2023_24 <= 15:
        print(f"{player_name} averages less than 15. Looping again...")

# ave the names of the selected players into variables
player1, player2 = selected_players
text = "Who is the better player?"
poll_options = [player1, player2]
# send Tweet with Text and poll options
client.create_tweet(text=text, poll_options=poll_options, poll_duration_minutes=1440)
print("Tweeted!")

