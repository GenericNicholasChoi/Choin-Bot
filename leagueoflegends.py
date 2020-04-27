
import discord
import json
import cassiopeia as cass
from secret.py import riotapikey

cass.set_riot_api_key(riotapikey)

class Match:
    #create a match object to transfer information
    def __init__(self, region, summonername, redteam, blueteam, red_ban, blue_ban,colour):
        self.region = region
        self.summonername = summonername
        self.redteam = redteam
        self.blueteam = blueteam
        self.blue_ban = blue_ban
        self.red_ban = red_ban
        self.colour = colour

    def to_string(self):
        if(self.redteam == None):
            embed = discord.Embed(title=self.summonername + "'s Match Not Found")
        else:
            embed = discord.Embed(title=self.summonername + "'s Match", colour=self.colour)
            red = ''
            blue = ''
            r_ban = ''
            b_ban = ''
            for name in self.redteam.keys():
                red += name + ' : ' + self.redteam[name] + "\n"
            for name in self.blueteam.keys():
                blue += name + ' : ' + self.blueteam[name] + "\n"
            for i in self.red_ban:
                r_ban += i + '\n' 
            for k in self.blue_ban:
                b_ban += k + '\n' 
            embed.add_field(name="Red Team", value=red)
            embed.add_field(name='Blue Team', value=blue, inline=False)
            embed.add_field(name='Red Bans', value=r_ban)
            embed.add_field(name='Blue Bans', value=b_ban)
        return embed


def game_search(region, summonername):
    # search for the current game for the  summoner given in the given region
    summoner = cass.get_summoner(name=summonername,region=region)
    # call for current match
    try:
        colour = 0xe74c3c
        current_game = summoner.current_match
        blue_team = current_game.blue_team
        red_team = current_game.red_team
        # grab the bans from both sides
        blue_bans = []
        red_bans = []
        for i in blue_team.bans:
            if(blue_team.bans[i].id != -1):
                blue_bans.append(blue_team.bans[i].name)
        for k in red_team.bans:
            if(red_team.bans[k].id != -1):
                red_bans.append(red_team.bans[k].name)
        # gran the playing champions along with summoner names
        blue_champs = {}
        for i in blue_team.participants:
            blue_champs[i.summoner.name] = i.champion.name
            if(i.summoner.name == summonername):
                colour=0x3498db
        red_champs = {}
        for i in red_team.participants:
            red_champs[i.summoner.name] =i.champion.name
        newMatch = Match(region, summonername,red_champs,blue_champs,red_bans,blue_bans,colour)
    except:
        newMatch = Match(region, summonername,None,None,None,None, None)
    print("Match Searched")
    return newMatch

