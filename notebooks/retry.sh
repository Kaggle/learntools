#!/bin/bash
with_retry() {
    count=$1                # How many times to try running the specified command.
    shift
    dur=$1                  # Initial sleep (int) duration.
    shift
    exp_backoff_factor=$1   # (int) Factor to multiply the sleep duration between attempts by.
    shift                   # Remaining "$@" specify the command to try.

    set +e
    for i in $(seq $(($count - 1))); do
        >&2 echo "-- Attempt ${i}/${count} for running: $@"
        "$@"
        status=$?
        if [[ $status == 0 ]]; then
            >&2 echo "-- Attempt ${i}/${count} succeeded."
            set -e
            return 0
        fi
        >&2 echo "-- Attempt ${i}/${count} failed with status $status, sleeping for $dur seconds before trying again..."
        sleep $dur
        dur=$(multiply $dur $exp_backoff_factor)
        dur=$(jitter 0.5 $dur)
    done
    "$@"
    status=$?
    [[ $status != 0 ]] && >&2 echo "-- Giving up after $count attempts, final status was $status."
    set -e
    return $status
}

# Returns $2 with random jitter +/- $1*$2. $1 & $2 can be decimals.
#   jitter 0.5 100 => returns values between [50, 150]
jitter() {
        jitter=$1
        dur=$2
        rand=$(random -100 100)            # random between [-100, 100]
        rand=$(multiply $rand 0.01)        # adjusted to [-1.00, 1.00]
        jitter=$(multiply $jitter $rand)
        jitter=$(multiply $jitter $dur)
        echo $(add $jitter $dur)
}

# Multiples $1 & $2 which can be decimals.
multiply() {
    echo $(awk -v A=$1 -v B=$2 'BEGIN { print (A * B)}')
}

# Adds $1 and $2 which can be decimals.
add() {
    echo $(awk -v A=$1 -v B=$2 'BEGIN { print (A + B)}')
}

# Returns a random int between $1 and $2 inclusive.
random() {
    echo $(($1 + $RANDOM % ($2-$1+1)))
}