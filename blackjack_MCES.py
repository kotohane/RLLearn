import numpy as np
import random


class blackjackGame:
    cards = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10])  # 0 stands for A

    show = 0

    banker_point = 0
    point = 0

    ba = 0
    a = 0

    # bust flag
    bust = 0
    banker_bust = 0

    def __init__(self, holda, showed, point):
        self.a = holda
        self.show = showed
        self.point = point
        hide = self.cards[random.randint(0, self.cards.size - 1)]
        self.banker_point = self.show + hide
        if self.show == 1 or hide == 1:
            self.ba = 1

    def banker_init(self):
        self.show = self.cards[random.randint(1, self.cards.size - 1)]
        hide = self.cards[random.randint(1, self.cards.size - 1)]
        self.banker_point = self.show + hide

    def draw_card(self):
        newcard = self.cards[random.randint(0, self.cards.size - 1)]
        if newcard == 1:
            self.point += 1
            self.a = 1
        else:
            self.point += newcard

    def banker_draw_card(self):
        newcard = self.cards[random.randint(0, self.cards.size - 1)]
        if newcard == 1:
            self.banker_point += 1
            self.ba = 1
        else:
            self.banker_point += newcard

    def is_terminal(self):
        if self.point > 21:
            self.bust = 1
            return 1
        return 0

    def get_max_score(self, pt, pa):
        if pa == 1 and pt <= 11:
            return pt + 10
        return pt

    def end_game(self):
        self.is_terminal()
        if self.bust == 1:
            return -1
        elif self.get_max_score(self.banker_point, self.ba) > self.get_max_score(self.point, self.a):
            return -1
        elif self.get_max_score(self.banker_point, self.ba) == self.get_max_score(self.point, self.a):
            return 0
        else:
            while self.get_max_score(self.banker_point, self.ba) < self.get_max_score(self.point, self.a):
                self.banker_draw_card()
            if self.banker_point + self.ba > 10:
                return 1
            elif self.get_max_score(self.banker_point, self.ba) > self.get_max_score(self.point, self.a):
                return -1
            else:
                return 0


# cards = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10])  # 0 stands for A

state = np.zeros(3)  # if has A; showed A~10; player total 12~21
policy = np.zeros((2, 10, 10))
q = np.zeros((2, 10, 10, 2))  # Q(s,a), A: 0~end, 1~draw
returns = np.zeros((2, 10, 10, 2), dtype=float)
returns_weight = np.zeros((2, 10, 10, 2))

gamma = 0.8


def generate_episode(holda, showed, point, action):
    episode = []
    game = blackjackGame(holda=holda, showed=showed, point=point)
    fa = game.a
    fpoint = game.point
    if action == 1:
        game.draw_card()
    r1 = game.end_game()
    episode.append([fa, game.show - 1, fpoint - 12, action, r1])

    while (game.point < 21):
        act = policy[game.a, game.show - 1, game.point - 12]
        nfa = game.a
        nfpoint = game.point
        if (act == 1):
            game.draw_card()
        else:
            break
        rew = game.end_game()
        episode.append([nfa, game.show - 1, nfpoint - 12, act, rew])
    episode = np.array(episode)
    episode.astype(int)
    return episode


for epic in range(0, 100000):
    # choose state and action
    state_holda = random.randint(0, 1)
    state_showed = random.randint(0, 9)  # 1 stands for A
    state_point = random.randint(0, 9)
    action = random.randint(0, 1)

    G = 0

    episode = generate_episode(state_holda, state_showed + 1, state_point + 12, action)
    for i in range(len(episode) - 1, -1, -1):
        G = gamma * G + float(episode[i][4])
        ea = int(episode[i][0])
        es = int(episode[i][1])
        ep = int(episode[i][2])
        eact = int(episode[i][3])
        G_weight = returns_weight[ea, es, ep, eact]
        G_ori = returns[ea, es, ep, eact]
        returns[ea, es, ep, eact] = float(G_ori * G_weight + G) / (G_weight + 1)
        q[ea, es, ep, eact] = returns[ea, es, ep, eact]
        if q[ea, es, ep, 0] > q[ea, es, ep, 1]:
            policy[ea, es, ep] = 0
        else:
            policy[ea, es, ep] = 1

print(q)
print(policy)
