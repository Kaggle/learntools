def conditional_roulette_probs(history):
    # dict where keys are numbers and values are dicts
    # counts[a][b] is the number of times we've spun the number b immediately after spinning a
    counts = {}
    # Iterate over the indices of history *except* the first (index 0). (In the loop, We'll 
    # be looking at each index alongside its previous index. But there's no previous index for i=0)
    for i in range(1, len(history)):
        # The numbers for the ith spin and the spin before it
        roll, prev = history[i], history[i-1]
        # If we haven't seen prev before, we need to add it to counts. (Otherwise counts[prev] will give a KeyError)
        if prev not in counts:
            counts[prev] = {}
        # Similar to above - add key to the inner dict if not present
        if roll not in counts[prev]:
            counts[prev][roll] = 0
        counts[prev][roll] += 1

    # We have the counts, but still need to turn them into probabilities
    probs = {}
    # dict.items() gives us a dictionary's (key, value) pairs as a sequence of tuples.
    for prev, nexts in counts.items():
        # The total number of spins that landed on prev (not counting the very last spin)
        total = sum(nexts.values())
        # Take the nects dictionary and normalize it so that its values sum to 1 (and represent probabilities)
        sub_probs = {next_spin: next_count/total
                for next_spin, next_count in nexts.items()}
        probs[prev] = sub_probs
    return probs

