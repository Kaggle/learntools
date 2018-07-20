import random

"""
Example display:
    Player is dealt K and 3 (total = 13)
    Dealer is dealt 8
    Player hits and receives 5. (total = 18)
    Player stays.
    Dealer hits and receives 4 (total = 12)
    Dealer hits and receives Q (total = 22)
    Dealer busts! Player wins!
"""

class BlackJack:

    def __init__(self, player_agent, verbose=False, legacy=False):
        self.phit = player_agent
        # Backwards compatibility with old call signature of should_hit
        self.legacy = legacy
        self.verbose = verbose
        self.player_cards = []
        self.dealer_cards = []

    @staticmethod
    def deal():
        return random.choice(list(range(2, 11)) + ['A', 'J', 'Q', 'K'])

    def log(self, msg):
        if self.verbose:
            print(msg)

    @property
    def player_total(self):
        return self.card_total(self.player_cards)
    @property
    def dealer_total(self):
        return self.card_total(self.dealer_cards)

    @staticmethod
    def card_total(cards, ace_counts=False):
        tot = 0
        aces = 0
        for c in cards:
            if c == 'A':
                aces += 1
            elif c in list('JQK'):
                tot += 10
            else:
                tot += c
        # tot is now the total of non-ace cards
        tot = tot + aces
        # tot is now the smallest possible total
        # Looping here isn't strictly necessary because we'll never count more 
        # than one ace as high. But hey, we're future-proofed in case we ever
        # want to implement 31.
        high_aces = 0
        for _ in range(aces):
            if (tot + 10) <= 21:
                tot += 10
                high_aces += 1
        if ace_counts:
            return tot, (aces-high_aces), high_aces
        return tot

    def player_hits(self):
        if self.legacy:
            args = [self.player_total, self.dealer_total, self.player_cards.count('A')]
        else:
            player_total, low_aces, high_aces = self.card_total(self.player_cards, ace_counts=1)
            args = [self.dealer_total, player_total, low_aces, high_aces]
        return self.phit(*args)

    def play(self):
        p1, p2 = self.deal(), self.deal()
        self.player_cards = [p1, p2]
        self.log('Player starts with {} and {} (total = {})'.format(
            p1, p2, self.player_total,
            ))
        d1 = self.deal()
        self.log('Dealer starts with {}'.format(d1))
        self.dealer_cards = [d1]

        self.log('\n__Player\'s turn__')
        while self.player_hits():
            c = self.deal()
            self.player_cards.append(c)
            self.log('Player hits and receives {}. (total = {})'.format(
                c, self.player_total))
            if self.player_total > 21:
                self.log('Player busts! Dealer wins.')
                return -1
        self.log('Player stays')

        self.log('\n__Dealer\'s turn__')
        while True:
            c = self.deal()
            self.dealer_cards.append(c)
            self.log('Dealer hits and receives {}. (total = {})'.format(
                c, self.dealer_total))
            if self.dealer_total > 21:
                self.log('Dealer busts! Player wins.')
                return 1
            # Stand on 17
            elif self.dealer_total >= 17:
                self.log('Dealer stands.')
                if self.dealer_total >= self.player_total:
                    self.log('Dealer wins. {} >= {}'.format(
                        self.dealer_total, self.player_total,
                        ))
                    return -1
                else:
                    self.log('Player wins. {} > {}'.format(
                        self.player_total, self.dealer_total,
                        ))
                    return 1

