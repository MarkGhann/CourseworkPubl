#!/bin/bash

cd WCRT
cd IMASimulator
cmake CMakeLists.txt
make
cd ..
cd ..
python3 main.py

exit 0
