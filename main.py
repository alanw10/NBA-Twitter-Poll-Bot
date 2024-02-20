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

def get_player_image(player_id):
    image_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to fetch image for player ID {player_id}")
        return None

# Initialize variables
selected_players = []
players_found = 0

# Loop until we find two players who average more than 15 minutes per game
while players_found < 2:
    # Choose a random active player
    random_active_player = random.choice(players.get_active_players())

    # Extract player ID and name
    player_id = random_active_player['id']
    player_name = random_active_player['full_name']

    # Fetch career stats for the player
    player_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_stats = player_stats.get_dict()

    # Check if the player has played in the 2023-24 season
    for dataset in career_stats['resultSets']:
        if dataset['name'] == 'SeasonTotalsRegularSeason':
            for row in dataset['rowSet']:
                if row[1] == '2023-24':
                    total_minutes = row[8]  # Total minutes played
                    games_played = row[6]    # Total games played
                    average_minutes_2023_24 = total_minutes / games_played
                            
                    # If the player averages more than 15 minutes, add their name to the list
                    if average_minutes_2023_24 > 15:
                        selected_players.append({'name': player_name, 'id': player_id})
                        players_found += 1
                        break
            
    # If the player doesn't average over 15 minutes, print a message and continue looping
    if average_minutes_2023_24 <= 15:
        print(f"{player_name} averages less than 15. Looping again...")

# Save the names of the selected players into variables
player1, player2 = selected_players

# Fetch images for selected players
player1_image = get_player_image(player1['id'])
player2_image = get_player_image(player2['id'])

if player1_image is not None and player2_image is not None:
    # Upload images as media
    media1 = api.simple_upload(filename=f"{player1['name']}.png", file=player1_image)
    media2 = api.simple_upload(filename=f"{player2['name']}.png", file=player2_image)

    # Create tweet with images
    text = "Who is the better player? Poll below."
    media_ids = [media1.media_id, media2.media_id]
    tweet = client.create_tweet(text=text, media_ids=media_ids)
    tweet_id = (tweet.data['id'])
    print("Initial tweet with images posted.")

    # Reply to the tweet with the poll
    poll_text = "Who's better?"
    poll_options = [player1['name'], player2['name']]
    client.create_tweet(text = "Who's better?", poll_options=poll_options, poll_duration_minutes=1440, in_reply_to_tweet_id=tweet_id)
    print("Replied to initial tweet with poll.")
else:
    print("Failed to fetch player images.")

