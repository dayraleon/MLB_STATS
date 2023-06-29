import requests 
import pandas as pandas

#API

def get_info(playerID):
    url = "https://mlb-data.p.rapidapi.com/json/named.player_teams.bam"
    
    data = {
        "player_id":"'493316'",
        "season":"'2014'"
    }

    headers = {
	    "X-RapidAPI-Key": "90b564737fmsh9e5b3ab74e323adp1d1f7fjsn55583b924947",
	    "X-RapidAPI-Host": "mlb-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=data)
    data = response.json()
   
    return data


def main():
    playerID = input('Enter a MLB player ID: ')
    player = get_info(playerID)

    if player is not None:
        print('The stats and games for {playerID} are {player}')
    else:
        print('Player not found')

if __name__ == '__main__':
    main()