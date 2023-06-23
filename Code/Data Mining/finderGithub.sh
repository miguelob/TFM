#!/bin/bash

############################################################
# Help                                                     #
############################################################

Help() {
  # Display Help
  echo "Search for a string inside every git repositories from list."
  echo
  echo "Syntax: finderGithub [-h|o] repoFile"
  echo "options:"
  echo "h     Print this Help."
  echo "o     Output file."
}

############################################################
# Process the input options.                               #
############################################################

while getopts "h:o:" option; do
  case $option in
  h) # display Help
    Help
    exit
    ;;
  o) # output file
    outputFile=$OPTARG
    ;;
  \?) # Invalid option
    echo "Error: Invalid option"
    exit
    ;;
  esac
done

shift "$((OPTIND - 1))"

if [ -z "$1" ]; then
  echo 'Missing query argument' >&2
  Help
  exit 1
fi

if [ -z "$outputFile" ]; then
  echo 'Missing -o option' >&2
  Help
  exit 1
fi

############################################################
# Main program                                             #
############################################################

workdir=$(pwd)

echo "Search for:"
echo "    1: Sign and ecrecover in Solidity files"
echo "    2: SignTypedData, eth_sign and personal_sign in TS and JS files"
read -r regNum

if [ "$regNum" -eq 1 ]; then
  stringToSearch="sign"
  stringToSearch2="ecrecover"
  fileRegex1="*.sol"
  fileRegex2="*.sol"
  echo "Results for $stringToSearch and $stringToSearch2" >"$outputFile"
else
  stringToSearch="signTypedData"
  stringToSearch2="eth_sign"
  stringToSearch3="personal_sign"
  fileRegex1="*.js"
  fileRegex2="*.ts"
  echo "Results for $stringToSearch, $stringToSearch2 and $stringToSearch3" >"$outputFile"
fi

echo ""

while read -r repolink; do
  repoTemp=$(echo "$repolink" | cut -d '/' -f 4-5)
  # shellcheck disable=SC2086
  repo=$(echo $repoTemp | cut -d '.' -f 1)

  echo "======================================="
  echo "Searching in $repo"

  echo "======================================= $repo =======================================" >>"$outputFile"

  git clone -q "https://github.com/$repo" "$workdir/tmpGitRepo"
  cd "$workdir/tmpGitRepo" || continue
  {
    git grep -I -n -i -o "$stringToSearch" -- "$fileRegex1" "$fileRegex2"
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    git grep -I -n -i -o "$stringToSearch2" -- "$fileRegex1" "$fileRegex2"
  } >>"../$outputFile"

  if [ "$regNum" -eq 1 ]; then
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" >>"../$outputFile"
    git grep -I -n -i -o "$stringToSearch3" -- "$fileRegex1" "$fileRegex2" >>"../$outputFile"
  fi

  cd "$workdir" || exit 1
  rm -rf "$workdir/tmpGitRepo"

done <"$1"
