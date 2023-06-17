#!/bin/bash

workdir=$(pwd)

echo "Enter repositories list file:"
read repofile

echo "Enter output file:"
read outputFile

echo "Search for (1: Sign in Solidity files ~ 2: SignTypedData, eth_sign and personal_sign in TS and JS files):"
read regNum

if [ $regNum -eq 1 ]
then
   stringToSearch="sign"
   stringToSearch2="ecrecover"
   fileRegex1="*.sol"
   fileRegex2="*.sol"
else
   stringToSearch="signTypedData"
   stringToSearch2="eth_sign"
   stringToSearch3="personal_sign"
   fileRegex1="*.js"
   fileRegex2="*.ts"
fi

echo ""

echo "Results of searching for $stringToSearch, $stringToSearch2 and $stringToSearch3" > $outputFile

while read repolink
do
   repo=$(echo $repolink | cut -d '/' -f 4-5)
   
   echo "=======================================" 
   echo "Searching in $repo..."
   
   echo "======================================= $repo =======================================" >> $outputFile
   
   gh repo clone "$repo" tmp -- -q
   cd tmp
   
   git grep -I -n -i -o "$stringToSearch" -- "$fileRegex1" "$fileRegex2" >> "../$outputFile"
   echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" >> "../$outputFile"
   git grep -I -n -i -o "$stringToSearch2" -- "$fileRegex1" "$fileRegex2" >> "../$outputFile"
   if [ $regNum -eq 1 ]
   then
      echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" >> "../$outputFile"
      git grep -I -n -i -o "$stringToSearch3" -- "$fileRegex1" "$fileRegex2" >> "../$outputFile"
   fi
   
   cd $workdir
   rm -rf tmp
   
done < $repofile



