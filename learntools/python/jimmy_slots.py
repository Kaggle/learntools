import random
from matplotlib import pyplot as plt
from learntools.python.ex5 import play_slot_machine

seed = 50
random.seed(seed)
balances = []
balance = 200
n = 10**3  // 2
for _ in range(n):
    if balance < 1:
        break
    balance = balance - 1 + play_slot_machine()
    balances.append(balance)

del seed, balance
    
def get_graph():
    """TODO (Jimmy): write documentation.
    """
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.plot(
        range(n), 
        balances,
        ',-',
    )
    return ax
