#!/bin/bash

mkdir tests
for((var = 0; var < 200; var++))
do
python3 FAR_graph_maker.py
python3 data_adapter.py
mv input.xml input$var.xml
cp input$var.xml ./tests
printf "input$var.xml" > names
done

exit 0
