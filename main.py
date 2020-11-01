import requests
import json
import pandas as pd
import time

def scrape(name):
  API_KEY = "RGAPI-1e6d8b82-5a9a-4b0b-9e5d-2545477596c3"
  head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,sl-SI;q=0.8,sl;q=0.7,hr;q=0.6",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": API_KEY
  }

  link = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(name)
  r = requests.get(link, headers=head)
  print(r.status_code)
  print(json.loads(r.text)["accountId"])

  out = []
  mid = 0
  accid = json.loads(r.text)["accountId"]
  for index_c in range(10):
    link = "https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?beginIndex={}".format(accid, index_c*250)
    r = requests.get(link, headers=head)

    # za vsak match
    for match in json.loads(r.text)["matches"]:
      
      mid += 1

      gameid = match["gameId"]
      r = requests.get("https://euw1.api.riotgames.com/lol/match/v4/matches/"+str(gameid), headers=head)
      if (r.status_code != 200):
        print("sleeping")
        time.sleep(60*2 + 15)

      
      data = json.loads(r.text)
      

      id_username = {}
      """ with open("match.json","w+") as f:
        json.dump(data, f) """
      try:
        for player in data["participantIdentities"]:
          # we find the player id
          id_username[player["participantId"]] = player["player"]["summonerName"]
      except:
        continue
       
      try:
        season = data["seasonId"]
        gm_id = data["gameId"]
        for player in data["participants"]:
          entry = {}
          entry["season"] = season
          entry["game"] = gm_id
          entry["summoner_name"] = id_username[player["participantId"]]
          print(entry["summoner_name"])
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
      except:
        pass
      print(mid)

  return out

  




if __name__ == "__main__":
  pd.DataFrame(scrape("LanLs")).to_excel("all_p.xlsx")