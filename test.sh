#!/bin/bash
set -e

IMAGE='gcr.io/kaggle-images/python:staging'
PINNED_IMAGE='gcr.io/kaggle-images/python@sha256:287c4e0e224e592dc6113940a6cf3d099b814c7bff0c1e8da57f8e6bad123ac5'
TRACK='all'
NOTEBOOK='all'

usage() {
cat <<EOF
Usage: $0 [OPTIONS]
Run automated tests.

By default, the tests are run against the staging image.

Options:
    -i, --image     IMAGE       Run tests against the specified image.
    -t, --track     TRACK       Run tests only for the specified track.
    -n, --notebook  NOTEBOOK    Run test only for notebooks mathing the specified name.
EOF
}

while :; do
    case "$1" in 
        -h|--help)
            usage
            exit
            ;;
        -i|--image)
            if [[ -z $2 ]]; then
                usage
                printf 'ERROR: No IMAGE specified after the %s flag.\n' "$1" >&2
                exit
            fi
            IMAGE=$2
            shift # skip the flag value
            ;;
        -t|--track)
            if [[ -z $2 ]]; then
                usage
                printf 'ERROR: No TRACK specified after the %s flag.\n' "$1" >&2
                exit
            fi
            TRACK="$2"
            shift # skip the flag value
            ;;
        -n|--notebook)
            if [[ -z $2 ]]; then
                usage
                printf 'ERROR: No NOTEBOOK specified after the %s flag.\n' "$1" >&2
                exit
            fi
            NOTEBOOK="$2"
            shift # skip the flag value
            ;;
        -?*)
            usage
            printf 'ERROR: Unknown option: %s\n' "$1" >&2
            exit
            ;;
        *)            
            break
    esac

    shift
done

readonly IMAGE
readonly TRACK
readonly NOTEBOOK

# set -x
if [[ -z $KAGGLE_KEY && ! ( -r "$HOME/.kaggle/kaggle.json" ) ]]; then
    printf "ERROR: Ensure your Kaggle API key is stored at ~/.kaggle/kaggle.json.\n" >&2
    printf "Visit the 'API' section of your Kaggle account page to generate this credential file.\n" >&2
    exit
fi

set -x

# Allows pinned notebooks to be tested independently. 
if [[ $TRACK  == "computer_vision" || $TRACK == "deep_learning_intro" ]]; then
    docker run --runtime runc --rm -t \
    -e KAGGLE_USERNAME -e KAGGLE_KEY \
    -v ~/.kaggle:/root/.kaggle:ro \
    -v $PWD:/input:ro \
    $PINNED_IMAGE \
    /bin/bash -c "/input/notebooks/test.sh $TRACK $NOTEBOOK"
    exit
fi


if [[ $TRACK == "all" ]]; then
    docker run --runtime runc --rm -t \
    -e KAGGLE_USERNAME -e KAGGLE_KEY \
    -v ~/.kaggle:/root/.kaggle:ro \
    -v $PWD:/input:ro \
    $PINNED_IMAGE \
    /bin/bash -c "/input/notebooks/test.sh kerasExp"
fi

docker run --runtime runc --rm -t \
    -e KAGGLE_USERNAME -e KAGGLE_KEY \
    -v ~/.kaggle:/root/.kaggle:ro \
    -v $PWD:/input:ro \
    $IMAGE \
    /bin/bash -c "/input/notebooks/test.sh $TRACK $NOTEBOOK"
