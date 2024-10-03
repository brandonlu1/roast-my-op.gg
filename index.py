import os
import asyncio
import aiohttp
import requests
from dotenv import load_dotenv
from Summoner import Summoner, Champion
import json
load_dotenv()
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

async def getMatches(puuid, count):
    async with aiohttp.ClientSession() as session:
        norms_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=400&type=normal&start=0&count={count}&api_key={RIOT_API_KEY}"
        ranked_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count={count}&api_key={RIOT_API_KEY}"
        flex_url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=440&type=ranked&start=0&count={count}&api_key={RIOT_API_KEY}"

        norms_response = await session.get(norms_url)
        ranked_response = await session.get(ranked_url)
        flex_response = await session.get(flex_url)

        norms = await norms_response.json()
        ranked = await ranked_response.json()
        flex = await flex_response.json()

        return norms + ranked + flex

async def getPUUID(username):
    username = username.split("#")
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username[0]}/{username[-1]}?api_key={RIOT_API_KEY}"
    
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        if response.status != 200:
            print("ERROR: ", response.status)
            return None
        return (await response.json())["puuid"]

def getMatchDetails(match_id, puuid):
        response = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}")
        if response.status_code == 200:
            match = response.json()
            participants = match["info"]["participants"]
            for player in participants:
                if player["puuid"] == puuid:
                    return player["championName"], player["kills"], player["deaths"], player["assists"], player["win"]
        return 

async def getSummonerInfo(who):
    puuid = await getPUUID(who)
    if puuid is None:
        return
    
    match_ids = await getMatches(puuid, 10)
    summoner = Summoner(who)

    performances = [getMatchDetails(match_id, puuid) for match_id in match_ids]
    for performance in performances:
        if performance:
            champion_name, kills, deaths, assists, win = performance
            summoner.addGame(champion_name, kills, deaths, assists, win)
    return summoner

async def updateDB(who):
    summoner = await getSummonerInfo(who)
    if not summoner:
        print("unable to find ", who)
        return
    with open('data.json', 'r') as file:
        db = json.load(file)
    db[who] = summoner.toJSON()
    with open('data.json', 'w') as file:
        json.dump(db, file, indent=4)
    return db[who]

async def getDB(who):
    with open('data.json', 'r') as file:
        db = json.load(file)
    if who not in db:
        res = await updateDB(who)
        return json.dumps(res)
    return json.dumps(db[who])


if __name__ == "__main__":
    # asyncio.run(getSummonerInfo("grippykitten69#UWU"))
    res = asyncio.run(getDB("Waviz#NA1"))
    print(res)