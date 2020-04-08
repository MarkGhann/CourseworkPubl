#!/bin/bash

names ="generate/names"
for var in $(cat $names)
do
rm input.xml
cp ../generate/tests/$var .
python3 mainAI.py 1
mv $var input.xml
cp out.xml ./out
done

names ="RealDataConstructor/names"
for var in $(cat $names)
do
rm input.xml
cp ../RealDataConstructor/tests/$var .
python3 mainAI.py 1
mv $var input.xml
cp out.xml ./out
done

exit 0
