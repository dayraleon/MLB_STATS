import requests 
import pandas as pandas

#API

def get_info(player_name):
    url = f"https://www.balldontlie.io/api/v1/players/{player_name}"
    
    data = {
        "id":237,
        "first_name":"LeBron",
         "last_name":"James",
         "position":"F",
         "height_feet": 6,
         "height_inches": 8,
         "weight_pounds": 250,
        "team":{
            "id":14,
            "abbreviation":"LAL",
            "city":"Los Angeles",
            "conference":"West",
            "division":"Pacific",
            "full_name":"Los Angeles Lakers",
            "name":"Lakers"
        }
    }

    response = requests.get(url,params=data)
    data = response.json()

    name = 'Full Name: ' + data["first_name"] + ' ' + data["last_name"]
   
    return name


def main():
    player_name = input('Enter a MLB player ID: ')
    player = get_info(player_name)

    if player is not None:
        print(player)
    else:
        print('Player not found')

if __name__ == '__main__':
    main()
