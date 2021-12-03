# Import packages
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
from scipy import interpolate
from scipy import integrate
from scipy import interpolate
from scipy import optimize
import functions

# to print plots inline
%matplotlib inline


#Set grids
size_grid = 200
x_grid = np.linspace(0, 2000, size_grid)
y_grid = np.linspace(0, 2000, size_grid)
V = np.zeros(size_grid)

#Set parameters
VFtol = 1e-8
dist = 7.0
VFmaxiter = 3000
D = np.random.normal(1000, 100, VFmaxiter)
Vmat = np.zeros((size_grid, size_grid))
Vstore = np.zeros((size_grid, VFmaxiter))
VFiter = 1
b = 10
h = 5
beta = 0.97
c = 10

V_func = interpolate.interp1d(x_grid, V, kind = 'cubic', fill_value = 'extrapolate')
opty = np.empty_like(V)


while dist > VFtol and VFiter < VFmaxiter:
    for x in x_grid:
        for y in y_grid:
            Vprime = np.trapz(V_func(y-D), D)  ##something is wrong here
            Vmat[x, y] = TC(c, y, x, h, b, D) + beta * Vprime
            opty[y] = minimize_scalar(Vmat)
            
    Vstore[:, VFiter] = V.reshape(size_grid, )
    TV = Vmat.min(1)
    PF = np.argmin(Vmat, axis = 1)
    V_func_new = interpolate.interp1d(x_grid, TV, kind = "cubic", fill_value = 'extrapolate')
    dist = (np.absolute(V_func_new(x_grid) - V_func(x_grid))).max()
    V = TV
    VFiter += 1

VF = V

if VFiter < VFmaxiter:
    print('Value function converged after this many iterations:', VFiter)
else:
    print('Value function did not converge')


#value function vs. state variable
plt.figure()
plt.scatter(x_grid[1:], VF[1:])
plt.xlabel('Initial inventory Level')
plt.ylabel('Value Function')
plt.title('Value Function - order up to inventory policy')
plt.show()


#policy function vs. state variable
plt.figure()
fig, ax = plt.subplots()
ax.plot(x_grid[3:], opty[3:], label='Order up to')
# Now add the legend with some customizations.
legend = ax.legend(loc='upper left', shadow=False)
# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Initial Inventory Level')
plt.ylabel('Optimal Order up to point')
plt.title('Policy Function, order up to')
plt.show()

