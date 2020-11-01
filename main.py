import requests
import json
import pandas as pd

def scrape(name):
  head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,sl-SI;q=0.8,sl;q=0.7,hr;q=0.6",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-1e6d8b82-5a9a-4b0b-9e5d-2545477596c3"
  }

  link = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(name)
  r = requests.get(link, headers=head)
  print(r.status_code)

  link = "https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(json.loads(r.text)["accountId"])
  r = requests.get(link, headers=head)

  out = []
  for i in json.loads(r.text)["matches"]:
    gameid = i["gameId"]

    r = requests.get("https://euw1.api.riotgames.com/lol/match/v4/matches/"+str(gameid), headers=head)
    if (r.status_code != 200):
      break
    
    data = json.loads(r.text)
    player_id = 11
    for player in data["participantIdentities"]:
      # we find the player id
      if(player["player"]["summonerName"] == name):
        player_id = player["participantId"]
    
    for player in data["participants"]:
      if player["participantId"] == player_id:
        entry = {}
        entry["kills"] = player["stats"]["kills"]
        entry["deaths"] = player["stats"]["deaths"]
        entry["assists"] = player["stats"]["assists"]
        entry["largestKillingSpree"] = player["stats"]["largestKillingSpree"]
        entry["largestMultiKill"] = player["stats"]["largestMultiKill"]
        entry["longestTimeSpentLiving"] = player["stats"]["longestTimeSpentLiving"]
        entry["totalDamageDealt"] = player["stats"]["totalDamageDealt"]
        entry["totalDamageDealtToChampions"] = player["stats"]["totalDamageDealtToChampions"]
        entry["totalHeal"] = player["stats"]["totalHeal"]
        entry["visionScore"] = player["stats"]["visionScore"]
        entry["goldEarned"] = player["stats"]["goldEarned"]
        entry["champLevel"] = player["stats"]["champLevel"]
        entry["wardsPlaced"] = player["stats"]["wardsPlaced"]
        entry["lane"] = player["timeline"]["lane"]
        try:
          entry["xpPerMinDeltas"] = player["timeline"]["xpPerMinDeltas"]["10-20"]
          entry["goldPerMinDeltas"] = player["timeline"]["goldPerMinDeltas"]["10-20"]
        except:
          pass
        out.append(entry)
        
  pd.DataFrame(out).to_excel("sawli.xlsx")


  




if __name__ == "__main__":
    scrape("LanLs")