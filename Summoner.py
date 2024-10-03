class Summoner:
    def __init__(self, username):
        self.username = username
        self.champions = {} #take ID and add a name to it
        self.mostKills = 0
        self.mostDeaths = 0
        self.totalGames = 0
    
    def __str__(self) -> str:
        summary = f"Summoner: {self.username}\n"
        summary += f"Total Games: {self.totalGames}\n"
        summary += f"Most Kills in a Game: {self.mostKills}\n"
        summary += f"Most Deaths in a Game: {self.mostDeaths}\n"
        summary += f"Champion Pool: {', '.join(self.champions.keys()) if self.champions else 'None'}\n"
        summary += "Champion Stats:\n"
        sorted_champions = sorted(self.champions.values(), key=lambda champion: champion.gamesPlayed, reverse=True)

        for champion in sorted_champions[:10]:
            summary += f" - {champion}\n"
        return summary
    
    def addGame(self, name, kills, deaths, assists, win):
        self.mostKills = max(self.mostKills, kills)
        self.mostDeaths = max(self.mostDeaths, deaths)
        self.totalGames += 1
        if name not in self.champions:
            self.champions[name] = Champion(name)
        self.champions[name].addStats(kills, deaths, assists, win)

    def getMostPlayedChampions(self, count):
        res = []
        for k, v in self.champions.items():
            res.append([])

    def getChampionPool(self):
        return self.champions.keys()
    
    def toJSON(self):
        sorted_champions = sorted(self.champions.values(), key=lambda champion: champion.gamesPlayed, reverse=True)

        return {
            "name": self.username, 
            "mostDeaths": self.mostDeaths, 
            "mostKills": self.mostKills, 
            "champions": [champ.toJSON() for champ in sorted_champions[:4]]
            }

class Champion:
    def __init__(self, name):
        self.name = name
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.gamesPlayed = 0
        self.wins = 0
    
    def addStats(self, kills, deaths, assists, win):
        self.kills += kills
        self.deaths += deaths
        self.assists += assists
        self.gamesPlayed += 1

        if win:
            self.wins += 1
        
    def getName(self):
        return self.name

    def getKDA(self):
        return (self.kills + self.assists) / self.deaths if self.deaths > 0 else 1

    def getWinrate(self):
        return self.wins / self.gamesPlayed if self.gamesPlayed > 0 else 1
    
    def __str__(self) -> str:
        kda = self.getKDA()
        winrate = self.getWinrate() * 100
        return (f"{self.name}: "
                f"{self.gamesPlayed} games played, "
                f"{self.kills/self.gamesPlayed:.2f}/{self.deaths/self.gamesPlayed:.2f}/{self.assists/self.gamesPlayed:.2f}, "
                f"KDA: {kda:.2f}, Win Rate: {winrate:.2f}%")

    def toJSON(self):
        kda = self.getKDA()
        winrate = self.getWinrate() * 100
        return {
            "name":self.name,
            "games": self.gamesPlayed,
            "deaths": self.deaths,
            "kda": kda,
            "wr": winrate
            }