#!/bin/bash -eu

set -e
set -u


AUSTIN_INTERVAL=1ms
SAMPLES=50


function sample {
  n=$1
  prefix=$2

  for i in `seq 1 $n`
  do
    PYTHONPATH=. austin -i $AUSTIN_INTERVAL -o data/${prefix}_${i}.austin python -m main
  done
}


test -d data || mkdir data

sample $SAMPLES "base"

export REGRESSION=1
sample $SAMPLES "regression"

