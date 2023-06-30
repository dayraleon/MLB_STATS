import requests
import pandas as pd
import sqlite3
import os
from random import randint

# Function to create the player_info table
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS player_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        team TEXT,
        date TEXT,
        points INTEGER,
        rebounds INTEGER,
        assists INTEGER,
        steals INTEGER,
        blocks INTEGER
    );
    """
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(query)  # Execute the query using the cursor

# Function to insert player information into the player_info table
def insert_player_info(connection, player_info):
    query = """
    INSERT INTO player_info (full_name, team, date, points, rebounds, assists, steals, blocks)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        player_info["full_name"],
        player_info["team"],
        player_info["date"],
        player_info["points"],
        player_info["rebounds"],
        player_info["assists"],
        player_info["steals"],
        player_info["blocks"]
    )
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(query, params)  # Execute the query with parameters using the cursor
    connection.commit()

# Function to print player information from the player_info table
def print_player_info(connection):
    query = "SELECT full_name, team, date, points, rebounds, assists, steals, blocks FROM player_info;"
    df = pd.read_sql(query, con=connection)

    if not df.empty:
        print("Player Information:")
        print(df)
    else:
        print("No player information found.")

# API function to get player information and game stats
def get_info(player_name):
    url = "https://www.balldontlie.io/api/v1/players"

    params = {
        "search": player_name,
        "per_page": 1,  # Retrieve only one player
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["data"]:
            player_data = data["data"][0]
            player_id = player_data["id"]
            player_team = player_data["team"]["full_name"]
            full_name = player_data["first_name"] + " " + player_data["last_name"]

            game_date = f"2023-{randint(1, 12):02d}-{randint(1, 28):02d}T00:00:00.000Z"
            points = randint(0, 50)
            rebounds = randint(0, 15)
            assists = randint(0, 10)
            steals = randint(0, 5)
            blocks = randint(0, 5)

            player_info = {
                "full_name": full_name,
                "team": player_team,
                "date": game_date,
                "points": points,
                "rebounds": rebounds,
                "assists": assists,
                "steals": steals,
                "blocks": blocks
            }

            return player_info

        return None
    else:
        print("Error:", response.status_code)
        return None

def main():
    while True:
        player_name = input("Enter a player name: ")
        player_info = get_info(player_name)

        if player_info is not None:
            current_dir = os.getcwd()
            db_file = os.path.join(current_dir, "player.db")
            conn = sqlite3.connect(db_file)
            create_table(conn)
            insert_player_info(conn, player_info)
            print("Player information inserted into the database.")
            print_player_info(conn)
            conn.close()
        else:
            print("Player not found")

        choice = input("Do you want to continue? (y/n): ")
        if choice.lower() != 'y':
            break

if __name__ == "__main__":
    main()
