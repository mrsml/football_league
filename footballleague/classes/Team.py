import random


class Team:
    def __init__(self, name, power):
        self.name = name
        self.power = power
        self.points = 0
        self.goal_for = 0
        self.goal_against = 0
        self.average = 0
        self.c_prob = 0
        self.total_matches = 0
        self.point_average = 0

    def playMatch(self, opposition, match_week):
        global point_weight
        if self.name != 'FREE WEEK' and opposition.name != 'FREE WEEK':
            # gol atma olasılıklarını hesaplama
            home_prob = int((self.power*100)/(self.power+opposition.power))
            away_prob = int((opposition.power*100) /
                            (self.power+opposition.power))
            home_score = 0
            away_score = 0
            # 10*10 dakika 90+10 dk gibi
            for minute in range(10):
                # 100/300 den oralama %33 ihtimalle her 10dk da bir gol olacak
                # ev sahibi takım için aralık atama
                home_range = random.randint(0, int(300-home_prob))
                # deplasman takım için aralık atama
                away_range = random.randint(0, int(300-away_prob))
                check_goal = random.randint(random.randint(0, 300), 300)
                # gol aralıkların birinde mi veya her ikisinde mi
                if check_goal > home_range and check_goal < home_range+home_prob:
                    home_score += 1
                if check_goal > away_range and check_goal < away_range+away_prob:
                    away_score += 1
            # atılan gol averaj hesaplamaları için atamalar
            self.goal_for += home_score
            self.goal_against += away_score
            opposition.goal_for += away_score
            opposition.goal_against += home_score
            result = '{} : {} - {} : {}'.format(self.name,
                                                home_score, opposition.name, away_score)
            c = self.c_prob
            o = opposition.c_prob
            self.total_matches += 1
            opposition.total_matches += 1
            # global değişkende tuttuğumuz yüzdelik değeri kazanan takıma ekleyip kaybedenden çıkarıyoruz, harika bi mantık değil ama iş görüyor
            if home_score > away_score:
                self.points += 3
            elif away_score > home_score:
                opposition.points += 3
            # beraberlik durumda bir değişiklik yok
            else:
                self.points += 1
                opposition.points += 1
            self.average += home_score-away_score
            opposition.average += away_score-home_score
            if self.points != 0:
                self.point_average = round(self.points/self.total_matches, 3)
            if opposition.points != 0:
                opposition.point_average = round(
                    opposition.points/opposition.total_matches, 3)
            self.c_prob += self.c_prob + \
                ((match_week)*self.point_average**15)
            opposition.c_prob = opposition.c_prob + \
                ((match_week)*opposition.point_average**15)
            return result
        # bay haftası kontrolü
        elif self.name == 'FREE WEEK':
            return '{} rested for the week'.format(opposition.name)
        else:
            return '{} rested for the week'.format(self.name)

    def champions_probability(self, total_power):
        prob = (self.power*100)/(total_power)
        self.c_prob = round(prob, 3)
