# This script calculates the factorial of a given
#  integer, which is the product of the integer and
#  all positive integers below it.

number = 5
multiplier = 1

while multiplier < number:
    number *= multiplier
    multiplier += 1

print (number)