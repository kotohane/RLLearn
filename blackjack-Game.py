import numpy as np
import random

cards = np.array([0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10])  # 0 stands for A

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


def banker_init():
    global show, banker_point, banker_cards
    show = cards[random.randint(1, cards.size - 1)]
    hide = cards[random.randint(1, cards.size - 1)]
    banker_cards.append(str(show))
    banker_cards.append(str(hide))
    banker_point = show + hide


def draw_card():
    global a, drawed_cards, point
    newcard = cards[random.randint(0, cards.size - 1)]
    if newcard == 0:
        print("Draw A")
        drawed_cards.append("A")
        a += 1
    else:
        print("Draw {}".format(newcard))
        drawed_cards.append(str(newcard))
        point += newcard


def banker_draw_card():
    global banker_point, ba
    newcard = cards[random.randint(1, cards.size - 1)]
    if newcard == 0:
        print("Banker draw A")
        banker_cards.append("A")
        ba += 1
    else:
        print("Banker draw {}".format(newcard))
        banker_cards.append(str(newcard))
        banker_point += newcard


def is_terminal():
    global bust
    if point + a > 21:
        bust = 1
        return 1
    return 0


def get_max_score(pt, pa):
    score = pt
    res = pa
    while res >= 1:
        if pt + res + 10 <= 21:
            res -= 1
            score += 11
        else:
            res -= 1
            score += 1
    return score


# Game Start

banker_init()
draw_card()
draw_card()

while 1:
    if show == 0:
        print("Banker's showed card: A")
    else:
        print("Banker's showed card: {}".format(show))
    print("My cards: {}\n".format(drawed_cards))

    choose = input("Draw: 1, End: 0\n")
    if choose == '1':
        draw_card()
        result = is_terminal()
        if result == 1:
            break
    else:
        break

print("\n\nEnd:\n")
print("Banker's Cards:{}".format(banker_cards))
print("My cards: {}\n".format(drawed_cards))

if bust == 1:
    print("Bust! Lose\n")
elif get_max_score(banker_point, ba) > get_max_score(point, a):
    print("Lose #\n")
elif get_max_score(banker_point, ba) == get_max_score(point, a):
    print("Push.\n")
else:
    print("Banker's Turn\n")
    while get_max_score(banker_point, ba) < get_max_score(point, a):
        banker_draw_card()
    print("Banker's Cards:{card} point:{point}".format(card=banker_cards, point=get_max_score(banker_point, ba)))
    print("My cards: {card} point:{point}\n".format(card=drawed_cards, point=get_max_score(point, a)))
    if banker_point + ba > 21:
        print("Banker Bust! Win!")
    elif get_max_score(banker_point, ba) > get_max_score(point, a):
        print("Lose")
    else:
        print("Push")

