# set the variable x, %d gets subbed for 10
x = "There are %d types of people." % 10
# set binary and do not
binary = "binary"
do_not = "don't"
# sub in the next two variables
y = "Those who know %s and those who %s." % (binary, do_not)

# print x and y
print x
print y

# now bring x and y into some new strings
print "I said: %r." % x
print "I also said '%s'." % y

# set hilarious and put a boolean into a string
hilarious = False
joke_evaluation = "Isn't that joke so funny?! %r"

# put a variable into a string after evaluation
print joke_evaluation % hilarious

# concatenate some strings 
w = "This is the left side of..."
e = "a string with a right side."

print w + e
