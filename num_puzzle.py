import itertools

nums = [2,3,5,9,7]

def checkAns(l):
    a,b,c,d,e = l
    return (a+b*c**2+d**3-e)==399

for p in itertools.permutations(nums):
    if checkAns(p):
        print p
