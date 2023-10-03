import requests
import pandas as pd
import sqlite3
import os

DB_FILE = "player.db"

# Function to create the player_info table
def create_table(connection):
  query = """
    CREATE TABLE IF NOT EXISTS player_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        team TEXT,
        season INTEGER,
        steals INTEGER,
        blocks INTEGER,
        rebounds INTEGER,
        points INTEGER
    );
    """
    connection.execute(query)


# Function to insert player information into the player_info table
def insert_player_info(connection, player_info):
    query = """
    INSERT INTO player_info(full_name, team, season, steals, blocks, rebounds, points)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    values = (
        player_info["Full Name"],
        player_info["Team"],
        player_info["Season Year"],
        player_info["Steals"],
        player_info["Blocks"],
        player_info["Rebounds"],
        player_info["Points"]
    )
    connection.execute(query, values)

# Function to print player information from the player_info table
def print_player_info(connection):
    query = "SELECT full_name, team, steals, blocks, rebounds, points, season FROM player_info"
    df = pd.read_sql(query, con=connection)

    if not df.empty:
        print("Player Information:")
        print(df)
    else:
        print("No player information found.")

def get_info(player_name, season):
    players_url = f"https://www.balldontlie.io/api/v1/players"
    response = requests.get(players_url, params={"search": player_name})
    data = response.json()

    if len(data["data"]) == 0:
        return None

    player_data = data["data"][0]
    full_name = player_data["first_name"] + " " + player_data["last_name"]
    team = player_data["team"]["full_name"]
    player_id = player_data["id"]

    stats_url = f"https://www.balldontlie.io/api/v1/season_averages"
    stats_response = requests.get(stats_url, params={"player_ids[]": player_id, "season": season})
    stats_data = stats_response.json()

    if len(stats_data["data"]) == 0:
        return None

    player_stats = stats_data["data"][0]

    stats = {
        "Full Name": full_name,
        "Team": team,
        "Steals": player_stats.get("stl", 0),
        "Blocks": player_stats.get("blk", 0),
        "Rebounds": player_stats.get("reb", 0),
        "Points": player_stats.get("pts", 0),
        "Season Year": season
    }

    return stats


def main():
    # Create the database file if it doesn't exist
    if not os.path.exists(DB_FILE):
        open(DB_FILE, "w").close()

    try:
        conn = sqlite3.connect(DB_FILE)
        create_table(conn)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return

    while True:
        player_name = input('Enter a player name (or "quit" to exit): ')
        if player_name.lower() == "quit":
            break

        season = input("Enter the season year: ")
        if season.lower() == "quit":
            break

        player_stats = get_info(player_name, season)

        if player_stats is not None:
            try:
                insert_player_info(conn, player_stats)
                print("Player information inserted into the database.")
                print_player_info(conn)
            except sqlite3.Error as e:
                print(f"Error inserting player information: {e}")
        else:
            print('Player not found')

    conn.close()

if __name__ == '__main__':
    main()
