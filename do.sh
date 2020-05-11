#!/bin/bash

name=$1
number=$2
cp tests/input$name-$number.xml .
mv input$name-$number.xml input.xml
for (( i=0; i < 100; i++ )) do
python3 mainGA.py $number
mv output.xml output$i.xml
cp output$i.xml resultsB
rm output$i.xml
done
rm input.xml
