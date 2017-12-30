import time
import sys

matrix = [['*', '8', '-', '1'],
		  ['4', '*', '11','*'],
		  ['+', '4', '-','18'],
		  ['22','-', '9', '*'],]

begin = (0,3)

def up(z):
	x,y=z
	y-=1
	return (x,y)
def down(z):
	x,y=z
	y+=1
	return (x,y)
def left(z):
	x,y=z
	x-=1
	return (x,y)
def right(z):
	x,y=z
	x+=1
	return (x,y)

def options(z):
	x,y=z
	r = [up,down,left,right]
	if z == (0,2):
		r.remove(down)
	if z == (1,3):
		r.remove(left)
	if x==0:
		r.remove(left)
	if y==0:
		r.remove(up)
	if x==3:
		r.remove(right)
	if y==3:
		r.remove(down)
	return r

def traverse(sq,cur_val,max_depth,depth=0):
	#time.sleep(0.001)
	op = options(sq)
	x,y = sq
	expr = cur_val+[matrix[y][x]]
	#print "at,",sq,expr
	if sq==(3,0):
		try:
			z = evalx(expr)
			if z==30:
				print "FOUND at,",sq,expr
				sys.exit(0)
			else:
				return False
		except SyntaxError:
			return False
	if depth==max_depth:
		return False
	for p in op:
		new_sq = p(sq)
		traverse(new_sq,expr,max_depth,depth+1)
	return False

def evalx(expr):
	cur_val = eval(expr[0])
	for i in range(len(expr)/2):
		cur_val = eval(str(cur_val)+expr[i*2+1]+expr[i*2+2])
	return cur_val

if __name__ == '__main__':
	i = 1
	while i<=25:
		print i,traverse(begin,[],i)
		i += 1
