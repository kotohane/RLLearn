import numpy as np
import random

# init Q at random
q = np.zeros((6, 6))
q = np.matrix(q)

# get Rewards by the environment
r = np.array([[-1, -1, -1, -1,  0,  -1],
              [-1, -1, -1,  0, -1, 100],
              [-1, -1, -1,  0, -1,  -1],
              [-1,  0,  0, -1,  0,  -1],
              [0,  -1, -1,  0, -1, 100],
              [-1,  0, -1, -1,  0, 100]])

gamma = 0.8

# train process

for i in range(1000):
    # randomly select training state
    state = random.randint(0, 5)
    while state != 5:
        r_pos_action = []
        for action in range(6):
            if r[state, action] >= 0:  # select only legal action
                r_pos_action.append(action)
        next_state = r_pos_action[random.randint(0, len(r_pos_action) - 1)]
        q[state, next_state] = r[state, next_state] + gamma * q[next_state].max()
        state = next_state

print("Q-table")
print(q)  # Q-table
print()

for i in range(10):
    state = random.randint(0, 5)
    print("exp {exp}, start at state {state}".format(exp=i+1, state=state))
    count = 0
    if state == 5:
        print("end\n")
        continue
    while state != 5:
        if count > 20:
            print('fail')
            break

        q_max = q[state].max()  # q_* <- max_a(q(s))

        # generate policy table pi(s), one state for multiply actions which are all optimistic
        q_opt_action = []
        for action in range(6):
            if q[state, action] == q_max:
                q_opt_action.append(action)

        next_state = q_opt_action[random.randint(0, len(q_opt_action) - 1)]
        print("Move: " + str(next_state) + ' <-- ' + str(state))
        state = next_state
        count += 1
        if state == 5:
            print("end\n")
