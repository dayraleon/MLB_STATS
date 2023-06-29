import requests

def get_info(player_name):
    url = f"https://www.balldontlie.io/api/v1/players"

    params = {
        "search": player_name
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data["data"]:
            player_data = data["data"][0]
            full_name = player_data["first_name"] + " " + player_data["last_name"]

            player_info = {
                "Full Name": full_name,
                "Team": player_data["team"]["full_name"]
            }

            return player_info
        else:
            return None
    else:
        print("Error:", response.status_code)
        return None


def main():
    player_name = input("Enter a player name: ")
    player_info = get_info(player_name)

    if player_info is not None:
        print("Player Information:")
        for key, value in player_info.items():
            print(f"{key}: {value}")
    else:
        print("Player not found")


if __name__ == "__main__":
    main()
