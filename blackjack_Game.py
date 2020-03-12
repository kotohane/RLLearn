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

    drawed_cards = []
    banker_cards = []

    def banker_init(self):
        self.show = self.cards[random.randint(0, self.cards.size - 1)]
        hide = self.cards[random.randint(0, self.cards.size - 1)]
        if self.show == 1:
            self.banker_cards.append("A")
        else:
            self.banker_cards.append(str(self.show))
        if hide == 1:
            self.banker_cards.append("A")
        else:
            self.banker_cards.append(str(hide))
        self.banker_point = self.show + hide
        if self.show == 1 or hide == 1:
            self.ba = 1

    def draw_card(self):
        newcard = self.cards[random.randint(0, self.cards.size - 1)]
        if newcard == 1:
            print("Draw A")
            self.drawed_cards.append("A")
            self.point += 1
            self.a = 1
        else:
            print("Draw {}".format(newcard))
            self.drawed_cards.append(str(newcard))
            self.point += newcard

    def banker_draw_card(self):
        newcard = self.cards[random.randint(0, self.cards.size - 1)]
        if newcard == 1:
            print("Banker draw A")
            self.banker_cards.append("A")
            self.banker_point += 1
            self.ba = 1
        else:
            print("Banker draw {}".format(newcard))
            self.banker_cards.append(str(newcard))
            self.banker_point += newcard

    def is_terminal(self):
        if self.point + self.a > 21:
            self.bust = 1
            return 1
        return 0

    def get_max_score(self, pt, pa):
        if pa == 1 and pt <= 11:
            return pt + 10
        return pt

    def end_game(self):
        if self.bust == 1:
            print("Bust! Lose\n")
            return -1
        elif self.get_max_score(self.banker_point, self.ba) > self.get_max_score(self.point, self.a):
            print("Lose #\n")
            return -1
        elif self.get_max_score(self.banker_point, self.ba) == self.get_max_score(self.point, self.a):
            print("Push.\n")
            return 0
        else:
            print("Banker's Turn\n")
            while self.get_max_score(self.banker_point, self.ba) < self.get_max_score(self.point, self.a):
                self.banker_draw_card()
            print(
                "Banker's Cards:{card} point:{point}".format(card=self.banker_cards,
                                                             point=self.get_max_score(self.banker_point, self.ba)))
            print("My cards: {card} point:{point}\n".format(card=self.drawed_cards,
                                                            point=self.get_max_score(self.point, self.a)))
            if self.banker_point + self.ba > 21:
                print("Banker Bust! Win!")
                return 1
            elif self.get_max_score(self.banker_point, self.ba) > self.get_max_score(self.point, self.a):
                print("Lose")
                return -1
            else:
                print("Push")
                return 0


# Game Start

bg = blackjackGame()

bg.banker_init()
bg.draw_card()
bg.draw_card()

while 1:
    if bg.show == 1:
        print("Banker's showed card: A")
    else:
        print("Banker's showed card: {}".format(bg.show))
    print("My cards: {}\n".format(bg.drawed_cards))

    choose = input("Draw: 1, End: 0\n")
    if choose == '1':
        bg.draw_card()
        result = bg.is_terminal()
        if result == 1:
            break
    else:
        break

print("\n\nEnd:")
print("Banker's Cards:{}".format(bg.banker_cards))
print("My cards: {}\n".format(bg.drawed_cards))

bg.end_game()
