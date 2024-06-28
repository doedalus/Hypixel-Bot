import requests
from mojang import API
import config

api_key = config.api_key

def get_info(name):
    mojang_api = API()
    uuid = mojang_api.get_uuid(name)
    url = f'https://api.hypixel.net/skyblock/profiles?key={config.api_key}&uuid={uuid}'

    def getinfo(url):
        r = requests.get(url)
        return r.json()

    result = getinfo(url)

    def selected_profile(result):
        for i in range(len(result)):
            if result['profiles'][i]['selected'] == True:
                return i

    def max_catacombs(selected):
        catalist = selected['members'][uuid]['leveling']['completed_tasks']
        maxcat = 0
        for i in range(len(catalist)):
            if 'COMPLETE_CATACOMBS' in catalist[i]:
                maxcat = max(maxcat,int(catalist[i][-1]))
        return f'Progress in the catacombs: {maxcat} floor'

    def lvl(selected):
        exp = selected['members'][uuid]['leveling']['experience']
        return f'Player level : {exp//100}'

    def new_lvl(selected):
        exp = selected['members'][uuid]['leveling']['experience']
        return f' To a new level : {100 - exp%100} exp'

    def total_catacombs(selected):
        cata = selected['members'][uuid]["dungeons"]["dungeon_types"]['catacombs']['tier_completions']
        res = ''
        total = ''
        for k in cata:
            if k!='total':
                res = res + f'* Floor {k}: {int(cata[k])}\n'
            if k == 'total':
                total = str(int(cata[k]))
        return res + f'* Total number of floors completed: {total}'

    selected = (result['profiles'][selected_profile(result)])

    def accessory_bag(selected):
        highest_magical_power = selected['members'][uuid]["accessory_bag_storage"]["highest_magical_power"]
        try:
            selected_power = selected['members'][uuid]["accessory_bag_storage"]["selected_power"]
        except KeyError:
            selected_power = 0
        try:
            unlocked_powers = selected['members'][uuid]["accessory_bag_storage"]["unlocked_powers"]
        except KeyError:
            unlocked_powers = 0
        qres = ''
        try:
            for i in unlocked_powers:
                qres = qres + f'{i}, '
            qres = qres[:-2]
        except TypeError:
            qres = 0
        return f'''* Highest magical power: {highest_magical_power}
* Selected power: {selected_power}
* Unlocked powers: {qres}'''

    def records(selected):
        try:
            highest_damage = int(selected['members'][uuid]['stats']["highest_damage"])
        except KeyError:
            highest_damage = 0
        try:
            highest_critical_damage = int(selected['members'][uuid]['stats']["highest_critical_damage"])
        except KeyError:
            highest_critical_damage = 0
        try:
            dragon_most_damage = int(selected['members'][uuid]['stats']["dragon_most_damage"])
        except KeyError:
            dragon_most_damage = 0
        try:
            ender_crystals_destroyed = int(selected['members'][uuid]['stats']["ender_crystals_destroyed"])
        except KeyError:
            ender_crystals_destroyed = 0
        try:
            special_zealot_loot_collected = int(selected['members'][uuid]['stats']['special_zealot_loot_collected'])
        except KeyError:
            special_zealot_loot_collected = 0
        return f'''* Highest damage: {highest_damage}
* Highest critical damage: {str(highest_critical_damage).zfill(1)}
* Dragon most damage: {str(dragon_most_damage).zfill(1)}
* Ender crystals destroyed: {str(ender_crystals_destroyed).zfill(1)}
* Special zealot loot collected: {str(special_zealot_loot_collected).zfill(1)}'''

    def cda(selected):
        try:
            deaths = int(selected['members'][uuid]['stats']['deaths'])
        except KeyError:
            deaths = 0
        try:
            kills = int(selected['members'][uuid]['stats']['kills'])
        except KeyError:
            kills = 0
        return f'''* Deaths: {deaths}
* Kills: {kills}'''

    result = getinfo(url)
    res = (f'''Player statistics {name} on profile {result['profiles'][selected_profile(result)]['cute_name']} :
--------------------------------
* {lvl(selected)}
* {new_lvl(selected)}
{cda(selected)}
* {max_catacombs(selected)}
-- Statistics in the catacombs --
{total_catacombs(selected)}
-- Accessory bag --
{accessory_bag(selected)}
-- Records --
{records(selected)}
--------------------------------''')
    return res
