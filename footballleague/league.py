import random
from fastapi import FastAPI
from random import shuffle
from collections import deque
from functions import create_fixture, response_generator
from classes.Team import Team


app = FastAPI()


@app.post("/fixture/{number_of_teams}")
async def create_league(number_of_teams: int):
    team_names = ['Galatasaray', 'Besiktas', 'Fenerbahce', 'Trabzonspor', 'Malatyaspor', 'Duzcespor', 'Genclerbirligi',
                  'Yalovaspor', 'Giresunspor', 'Manisaspor', 'Kocaelispor', 'Sakaryaspor', 'Ankaragucu', 'Umraniyespor',
                  'Alanyaspor', 'Hatayspor', 'Kasimpasa', 'Istanbulspor', 'Sivasspor', 'Bandirmaspor', 'Konyaspor']
    response = {'createdTeams': [], 'fixture_plan': {}}
    response2 = {'play': {}}
    teams = []
    LOWER_RANDOM_RANGE = 1
    UPPER_RANDOM_RANGE = 100
    total_power = 0
    for team_number in range(number_of_teams):  # Create teams
        team_name = random.choice(team_names)
        teams.append(Team(team_name, round((random.randint(LOWER_RANDOM_RANGE, UPPER_RANDOM_RANGE) +
                     random.randint(LOWER_RANDOM_RANGE, UPPER_RANDOM_RANGE))/2, 2)))
        team_names.remove(team_name)
        total_power += teams[team_number].power

    championship_prob = deque()
    for team in teams:  # Assign championship probabilities to each team
        team.champions_probability(total_power)
        response['createdTeams'].append(
            {"{}  --->  strenght: {}".format(team.name, team.power)})
        championship_prob.append(
            {"{}  --->  %{}".format(team.name, round(team.c_prob, 2))})
    response2['play']['Initial championship probabilities'] = list(
        championship_prob)

    global point_weight
    number_of_legs = 2
    winning_points = 3
    point_weight = round(
        100/((number_of_teams-1)*number_of_legs*winning_points), 2)
    winning_probabilites = deque()
    fixture, winning_probabilites = create_fixture(teams)
    # response generator
    message = response_generator(
        fixture, response, response2, teams, winning_probabilites)
    return message
