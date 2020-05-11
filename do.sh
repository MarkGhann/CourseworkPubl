#!/bin/bash

name=$1
number=$2
results=results$name
mkdir $results
cp tests/input$name-$number.xml .
mv input$name-$number.xml input.xml
for (( i=0; i < 100; i++ )) do
python3 mainGA.py $number
mv output.xml output$i.xml
cp output$i.xml $results
rm output$i.xml
done
rm input.xml
