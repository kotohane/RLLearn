import torch
import numpy as np


BANDIT_NUM = 50
STD_DIFF = 5
eps = 0.1
RANGE_NUM = 3000

np.random.seed(1)
bandit = np.random.normal(100, 10, BANDIT_NUM)

q = np.zeros(BANDIT_NUM)
qnum = np.zeros(BANDIT_NUM)

maxindex = 1
maxvalue = 0

reward = 0
answer = 0.0

poi = np.random.uniform(0, 1, RANGE_NUM)
rdch = np.random.randint(0,BANDIT_NUM, RANGE_NUM)
scar = np.random.normal(0, STD_DIFF, RANGE_NUM)

for step in range(0, RANGE_NUM):
    if (poi[step] < eps or step == 0):
        # choose a new one
        rd = rdch[step]
        answer = bandit[rd] + scar[step]
        q[rd] = ( q[rd] * qnum[rd] + answer)/(qnum[rd] + 1)
        qnum[rd] += 1
        if(qnum[rd] > maxvalue):
            maxvalue = qnum[rd]
            maxindex = rd
        reward += answer
        print("#{step} choose {index}, reward {reward}\n".format(step = step, index = rd, reward = answer))
    else:
        answer = bandit[maxindex] + scar[step]
        q[maxindex] = (q[maxindex] * qnum[maxindex] + answer) / (qnum[maxindex] + 1)
        qnum[maxindex] += 1
        maxvalue = qnum[maxindex]
        reward += answer
        print("#{step} choose {index}, reward {reward}\n".format(step = step, index= maxindex, reward = answer))

print("\n\nTotal reward:{rewards}\n\n".format(rewards = reward))

for _ in range(0,BANDIT_NUM):
    print("bandit {index} ex {exp}".format(index = _, exp = q[_]))

