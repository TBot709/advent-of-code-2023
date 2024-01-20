#!/usr/bin/bash

n="$1"

if [ -z $1 ]
then 
	echo "no argument, expected day number"
	exit 1
fi

mkdir -p "day$n"
cd "day$n"
cp ../day00/day00_template.py "day${n}-1.py"
sed -i "s/puzzleNumber = \"00\"/puzzleNumber = \"${n}\"/g" "day${n}-1.py"
sed -i "s/partNumber = \"0\"/partNumber = \"1\"/g" "day${n}-1.py"
cp ../day00/day00_template.py "day${n}-2.py"
sed -i "s/puzzleNumber = \"00\"/puzzleNumber = \"${n}\"/g" "day${n}-2.py"
sed -i "s/partNumber = \"0\"/partNumber = \"2\"/g" "day${n}-2.py"
touch "day${n}_input.txt"
touch "day${n}_example-input.txt"

