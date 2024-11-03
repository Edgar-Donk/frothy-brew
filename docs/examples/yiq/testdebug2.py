# This script calculates the factorial of a given
# integer, which is the product of the integer and
# all positive integers below it.
number = 5
loopStop = number
multiplier = 1
while multiplier < loopStop:
    number *= multiplier
    multiplier += 1

print (number)