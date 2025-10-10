#!/bin/sh
# Script illustrating variable use

echo "This script was called with $# parameters"
echo "The script's name is $0"
echo "The arguments are $@"
echo "The first argument is $1"
echo "The second argument is $2"

MY_VAR='some string'
echo 'The current value of MY_VAR is:' $MY_VAR
echo
echo 'Please enter a new string:'
read MY_VAR
echo 'Now MY_VAR is:' $MY_VAR
echo

echo 'Enter two numbers separated by space(s):'
read a b
MY_SUM=$(expr $a + $b)
echo "You entered $a and $b. Their sum is: $MY_SUM"
