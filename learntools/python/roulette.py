import math
import random
import time

class RouletteException(Exception):
    pass

class TooManyRoundsException(RouletteException):
    pass

class NoSuchNumberException(RouletteException):
    pass

def report(agent, wheel_size = 11,
           num_simulations = 20000, num_spins_per_simulation = 100,
           biased_transition_prob = 0.5):
    final_balances = []
    num_bets_made = 0
    num_bets_successful = 0
    start_time = time.time()
    for i in range(num_simulations):
        game = RouletteSession(wheel_size, num_spins_per_simulation, biased_transition_prob)
        agent(game)
        final_balances.append(game.balance())
        num_bets_made += game.num_bets_made()
        num_bets_successful += game.num_bets_successful()
    time_taken = time.time() - start_time
    average_gain = sum(final_balances) / len(final_balances)
    print("Report:\nseconds taken: {:.1f}\nRan {:,} simulations with {} spins each.\nAverage gain per simulation: ${:.2f}".format(time_taken, num_simulations, num_spins_per_simulation, average_gain, ))
    print("Average # bets made: {:.1f}\nAverage # bets successful: {:.1f} ({:.1%} success rate)".format(
        num_bets_made/num_simulations, num_bets_successful/num_simulations,
        math.nan if num_bets_made == 0 else num_bets_successful/num_bets_made,
        )
    )
    #print(display_balances(final_balances)))

evaluate_roulette_strategy = report

class RouletteSession:
    def __init__(self, wheel_size, num_spins, biased_transition_prob):
        self._balance = 0
        self._wheel_size = wheel_size
        self._biased_transition_prob = biased_transition_prob
        self._num_remaining_spins = num_spins
        self._bias_pair = (random.randrange(wheel_size), random.randrange(wheel_size))
        self._last_number = 0
        self._num_bets_made = 0
        self._num_bets_successful = 0

    def balance(self):
        """How much money you have left."""
        return self._balance

    def num_remaining_spins(self):
        """How many spins are left."""
        return self._num_remaining_spins

    def spin(self, number_to_bet_on = None):
        """
        Spin the wheel!

        This method returns the number the ball landed in.

        To place a bet, pass the number you'd like to bet on with the optional
        number_to_bet_on parameter. It will cost you $1, but if you your guess
        is correct, you'll get the dollar back plus $9 more.

        To spin without placing a bet, call this with no arguments.

        Don't call this if self.num_remaining_spins() returns 0.
        """
        if self._num_remaining_spins <= 0:
            raise TooManyRoundsException()
        if number_to_bet_on is not None and number_to_bet_on not in range(self._wheel_size):
            raise NoSuchNumberException( ("{} is not a valid number to bet on. The wheel"
                " contains the numbers 0 through {} inclusive. (You can also"
                " pass number_to_bet_on=None to spin but not bet)").format(
                    number_to_bet_on, self._wheel_size-1)
                )

        # If the last number was self._bias_pair[0], we want to output
        # self._bias_pair[1] with probability self._biased_transition_prob.
        # Adding this condition is one way to do that: now the overall probability
        # of rolling self._bias_pair[1] is
        #     (biased_transition_prob * wheel_size - 1) / (wheel_size - 1)
        #     + (wheel_size - biased_transition_prob * wheel_size) / (wheel_size - 1)
        #       * (1 / wheel_size)
        #   = (biased_transition_prob * wheel_size - biased_transition_prob)
        #     / (wheel_size - 1)
        #   = biased_transition_prob
        if self._last_number == self._bias_pair[0] \
           and random.random() < \
               (self._biased_transition_prob * self._wheel_size - 1) \
               / (self._wheel_size - 1):
            next_number = self._bias_pair[1]
        else:
            next_number = random.randrange(self._wheel_size)

        if number_to_bet_on is not None:
            self._num_bets_made += 1
            if number_to_bet_on == next_number:
                self._num_bets_successful += 1
                self._balance += self._wheel_size - 2
            else:
                self._balance -= 1

        self._last_number = next_number
        self._num_remaining_spins -= 1
        return next_number

    def num_bets_made(self):
        return self._num_bets_made

    def num_bets_successful(self):
        return self._num_bets_successful

def display_balances(balances):
    histogram = {}
    for balance in balances:
        if balance == 0:
            bucket = "000"
        elif balance <= 10:
            bucket = "001..010"
        elif balance <= 100:
            bucket = "011..100"
        else:
            range_start = math.floor(balance / 100) * 100
            bucket = "{}..{}".format(range_start, range_start + 99)
        histogram.setdefault(bucket, 0)
        histogram[bucket] += 1
    lines = []
    for bucket in sorted(histogram.keys()):
        lines.append("{}: {}".format(bucket, histogram[bucket]))
    return "\n".join(lines)
