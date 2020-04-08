#!/bin/bash

mkdir out
./make_tests.sh
./do_GA.sh
./do_AI1.sh
./do_AI2.sh
./do_AI3.sh

exit 0
