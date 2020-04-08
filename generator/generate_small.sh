#!/bin/bash

mkdir tests
for((var = 0; var < 200; var++))
do
python3 generator.py
mv input.xml input$var.xml
cp input$var.xml ./tests
printf "input$var.xml" > names
done
exit 0
