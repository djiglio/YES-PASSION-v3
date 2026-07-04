import json
import math
import random

with open('data/seasons/season_25.json', 'r', encoding='utf-8') as f:
    seasonData = json.load(f)

teams = []
for t in seasonData['teams']:
    teams.append({
        'id': t['id'],
        'name': t['name'],
        'isUser': False,
        'fullRoster': t['players'],
        'squad': []
    })

AVAILABLE_FORMATIONS = [
    [ ['POR'], ['DC', 'DC', 'DC'], ['CDC'], ['ES', 'CC', 'CC', 'ED'], ['ATT', 'ATT'] ],
    [ ['POR'], ['TS', 'DC', 'DC', 'TD'], ['ES', 'CC', 'CC', 'ED'], ['ATT', 'ATT'] ],
    [ ['POR'], ['TS', 'DC', 'DC', 'TD'], ['CDC', 'CDC'], ['COC', 'AT', 'COC'], ['ATT'] ],
    [ ['POR'], ['TS', 'DC', 'DC', 'DC', 'TD'], ['ES', 'CC', 'CC', 'ED'], ['ATT'] ]
]

def generateCPUSquad(teamPlayers):
    if not teamPlayers: return []
    chosen = random.choice(AVAILABLE_FORMATIONS)
    formations = [role for row in chosen for role in row]
    squad = []
    availablePlayers = list(teamPlayers)
    for role in formations:
        bestIdx = -1
        bestOvr = -1
        for i, p in enumerate(availablePlayers):
            r = p.get('Ruolo', '')
            ovr = p.get('Overall', 50)
            if role in r and ovr > bestOvr:
                bestOvr = ovr
                bestIdx = i
        if bestIdx == -1:
            bestOvr = -1
            for i, p in enumerate(availablePlayers):
                ovr = p.get('Overall', 50)
                if ovr > bestOvr:
                    bestOvr = ovr
                    bestIdx = i
        if bestIdx != -1:
            squad.append(availablePlayers[bestIdx])
            availablePlayers.pop(bestIdx)
    return squad

def calculateTeamPowers(squad):
    attSum = 0; attCount = 0
    midSum = 0; midCount = 0
    defSum = 0; defCount = 0
    gkSum = 0; gkCount = 0
    for player in squad:
        role = player.get('Ruolo', '')
        ovr = player.get('Overall', 50)
        if 'POR' in role: gkSum+=ovr; gkCount+=1
        elif any(r in role for r in ['DC', 'TS', 'TD', 'ASA', 'ADA']): defSum+=ovr; defCount+=1
        elif any(r in role for r in ['CDC', 'CC', 'COC', 'ES', 'ED']): midSum+=ovr; midCount+=1
        else: attSum+=ovr; attCount+=1
    
    def calcPower(s, c):
        if c == 0: return 0
        return s / c # Use strict average!
    return {
        'att': calcPower(attSum, attCount),
        'mid': calcPower(midSum, midCount),
        'def': calcPower(defSum, defCount),
        'gk': calcPower(gkSum, gkCount)
    }

def getPoissonRandom(lmbda):
    L = math.exp(-lmbda)
    k = 0
    p = 1
    while True:
        k += 1
        p *= random.random()
        if p <= L:
            break
    return k - 1

def simulateMatch(homeTeam, awayTeam, BASE, EXP_STRONG, EXP_WEAK):
    # regenerate squad every time to randomize formation
    homeTeam['squad'] = generateCPUSquad(homeTeam['fullRoster'])
    awayTeam['squad'] = generateCPUSquad(awayTeam['fullRoster'])
    
    homePowers = calculateTeamPowers(homeTeam['squad'])
    awayPowers = calculateTeamPowers(awayTeam['squad'])
    
    homeAdvantage = 1.05
    homeMidControl = homePowers['mid'] * homeAdvantage
    awayMidControl = awayPowers['mid']
    
    homeAttackPower = (homePowers['att'] * 0.7 + homeMidControl * 0.3) * homeAdvantage
    awayDefensePower = (awayPowers['def'] * 0.7 + awayPowers['gk'] * 0.15 + awayMidControl * 0.15)
    
    awayAttackPower = (awayPowers['att'] * 0.7 + awayMidControl * 0.3)
    homeDefensePower = (homePowers['def'] * 0.7 + homePowers['gk'] * 0.15 + homeMidControl * 0.15) * homeAdvantage
    
    def calc_goals(att, df):
        if df == 0: df = 1
        ratio = att / df
        if ratio >= 1:
            expectedGoals = BASE * math.pow(ratio, EXP_STRONG)
        else:
            expectedGoals = BASE * math.pow(ratio, EXP_WEAK)
        
        luckFactor = (random.random() * 0.4) - 0.2
        expectedGoals += luckFactor
        if expectedGoals < 0.1: expectedGoals = 0.1
        return getPoissonRandom(expectedGoals)

    homeGoals = calc_goals(homeAttackPower, awayDefensePower)
    awayGoals = calc_goals(awayAttackPower, homeDefensePower)
    
    return homeGoals + awayGoals

def test_params(BASE, EXP_STRONG, EXP_WEAK):
    total_seasons = 30
    total_goals_all = 0
    for s in range(total_seasons):
        totalGoals = 0
        for i in range(len(teams)):
            for j in range(len(teams)):
                if i == j: continue
                totalGoals += simulateMatch(teams[i], teams[j], BASE, EXP_STRONG, EXP_WEAK)
        total_goals_all += totalGoals
    return total_goals_all / total_seasons

print("Testing strict average + old params 1.65, 1.8, 2.2: ", test_params(1.65, 1.8, 2.2))
print("Testing strict average + BASE 1.35, EXP 2.5, 3.0: ", test_params(1.35, 2.5, 3.0))
print("Testing strict average + BASE 1.45, EXP 2.8, 3.2: ", test_params(1.45, 2.8, 3.2))
print("Testing strict average + BASE 1.50, EXP 3.0, 3.5: ", test_params(1.50, 3.0, 3.5))
print("Testing strict average + BASE 1.40, EXP 4.0, 4.0: ", test_params(1.40, 4.0, 4.0))
