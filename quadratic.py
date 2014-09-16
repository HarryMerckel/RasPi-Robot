from math import sqrt

a = 1
b = 5
c = 6

try:
    squareroot = math.sqrt((b^2)-4*(a*c))
except:
    print "Fail"
    squareroot = 0
topplus = 0-b+squareroot
topminus = 0-b-squareroot
bottom = 2*a
ans1 = topplus/bottom
ans2 = topminus/bottom
print ans1
print ans2