from django.http import HttpResponse
from django.shortcuts import render

def getLocs():
	return [(0,0), (3,5), (2,2), (4,2)]

def findGreatestX(locs):
	target = None
	g = 0
	for i, tup in enumerate(locs):
		if tup[0] > g:
			g = tup[0]
			target = i
	return target

def findGreatestY(locs):
	target = None
	l = 0
	for i, tup in enumerate(locs):
		if tup[1] > l:
			l = tup[1]
			target = i
	return target

def mapLocs(locs):
	greatest_x = findGreatestX(locs)
	greatest_y = findGreatestY(locs)

	x_max = locs[greatest_x][0]
	y_max = locs[greatest_y][1]

	for i, tup in enumerate(locs):
		x_ratio = locs[i][0]/x_max
		print(i,x_ratio)
		y_ratio = locs[i][1]/y_max
		locs[i] = (i, (780*x_ratio, 630*y_ratio))
	

	return locs

def index(request):
	locs = getLocs()
	locs = mapLocs(locs)

	context = {'locs': locs}
	return render(request, 'mapping/index.html', context)

locs = getLocs()
locs = mapLocs(locs)