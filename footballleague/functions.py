from collections import deque


def normalize_championship_probability(teams):
    total_prob = 0
    for team in teams:
        total_prob += team.c_prob
    for team in teams:
        team.c_prob = round((team.c_prob/total_prob)*100, 2)
    return teams


def is_odd(value):
    if value % 2 == 0:
        return False
    else:
        return True


def create_fixture(teams: list):
    fixture = deque()
    number_of_teams = len(teams)
    number_of_legs = 2
    if is_odd(number_of_teams):                  # tek sayıda takım varsa bay haftası ekleniyor
        teams.append(Team('FREE WEEK', 0))
    # maç sayısı = (takım sayısı - 1)*2 (ev-deplasman)
    match_week = 0
    normalized_probabilties = {}
    for leg in range((number_of_teams-1)*number_of_legs):
        normalized = []
        fix = deque()  # haftalık maçları, skorları, şampiyonluk oranı değişimlerini tutacağız
        for match_number in range(int(number_of_teams/2)):
            # haftalık maç sayısı takım sayısı / 2
            t1 = teams[match_number]
            t2 = teams[(number_of_teams)-(match_number+1)]
            # deplasman değişimi/ 4 takım->6 maç / 0,1,2 ev 3,4,5 deplasman
            if leg < (int(number_of_teams-1)):
                fix.append('{} - {}'.format(t1.name, t2.name))
                fix.append(t1.playMatch(t2, match_week))
            else:
                fix.append('{} - {}'.format(t2.name, t1.name))
                fix.append(t2.playMatch(t1, match_week))
        match_week += 1
        normalize_championship_probability(teams)
        for team in teams:
            normalized.append("{} ---> %{}".format(team.name, team.c_prob))
        normalized_probabilties['Week {}'.format(match_week)] = normalized
        fixture.append(fix)
        # (n-1)'nci takımı 2. sıraya taşıyoruz // https://en.wikipedia.org/wiki/Round-robin_tournament
        move = teams[number_of_teams-1]
        teams.remove(move)
        teams.insert(1, move)
    return fixture, normalized_probabilties


def response_generator(fixture, response, response_part2, teams, winning_probabilities):
    fixture_lenght = len(fixture)
    for week in range(fixture_lenght):
        fixture_plan, played_matches, matches_probabilities = deque(), deque(), deque()
        value = 0
        while value < int(len(fixture[week])):
            fixture_plan.append(fixture[week][value])
            value += 1
            played_matches.append(fixture[week][value])
            value += 1
        response['fixture_plan']['week {}'.format(
            week+1)] = list(fixture_plan)
        response_part2['play']['week {}'.format(
            week+1)] = list(played_matches)
        if week < fixture_lenght-1:
            response_part2['play']['Championship chances before week {}'.format(
                week+2)] = winning_probabilities['Week {}'.format(week+1)]

    return response, response_part2
