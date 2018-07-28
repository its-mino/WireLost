import math
import sympy
import sys

#A is master
#C is along X
#B is unknown

#lines
BC = 5.831

AC = 5

AB = 5.3852

#angles
A = (math.acos(((AC**2 + AB**2) - BC**2)/(2*AC*AB)))

B = (math.acos(((AB**2 + BC**2) - AC**2)/(2*AB*BC)))

C = math.radians(180)-(A+B)

print("A angle: "+str(math.degrees(A)))
print("B angle: "+str(math.degrees(B)))
print("C angle: "+str(math.degrees(C)))

#known coordinates
a_loc = (0,0)
print("A: "+str(a_loc))
c_loc = (AC,0)
print("C: "+str(c_loc))

#slopes tan(tan−1(y/x)−θ)
ac_slope = 0
print("AC Slope: "+str(ac_slope))
bc_slope = math.tan(C)
print("BC Slope: "+str(bc_slope))
ab_slope = -1 * math.tan(A)


print("AB Slope: "+str(ab_slope))

#equation for bc: y = bc_slope(x-AC)
#equation for ab: y = ab_slope(x)
 
#find B:
#	bc_slope(x-AC) = ab_slope(x) 
x = sympy.Symbol('x')
Bx = sympy.solve(bc_slope*(x-AC) - ab_slope*(x))
Bx = Bx[0]
print("Bx: "+str(Bx))

By = ab_slope * Bx

print("By: "+str(By))

# bx = (b*math.cos(A))
# print(bx)
# by = (b*math.sin(A))
# print(by)

# cx = (c*math.cos(A))
# cy = (c*math.sin(A))

# print(cy)
# print(cx)
