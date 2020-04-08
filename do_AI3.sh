#!/bin/bash

names ="generate/names"
for var in $(cat $names)
do
rm input.xml
cp ../generate/tests/$var .
mv $var input.xml
python3 mainAI.py 3
cp out.xml ./out
done

names ="RealDataConstructor/names"
for var in $(cat $names)
do
rm input.xml
cp ../RealDataConstructor/tests/$var .
mv $var input.xml
python3 mainAI.py 3
cp out.xml ./out
done

exit 0
