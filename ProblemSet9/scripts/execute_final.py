import SS
import numpy as np

# Set parameters
alpha = 0.3
delta = 0.1
A = 1.0
S = 10
b = 0.501
v = 1.554
l = 1.0
sigma = 1.5
beta = 0.8
chi = np.array([1 for i in range(S)])

# Make initial guesses
r_guess = 0.1
b_guesses = np.array([0.01 for i in range(S-1)])
n_guesses = np.array([1 for i in range(S)])

r_ss, success, euler_errors = SS.SS_solver(r_guess, b_guesses, n_guesses, 
                                           S, b, v, l, alpha, delta, A, sigma, beta)

print('The SS interest is ', r_ss, 'Did we find the solution? ', success)
print('The Euler errors are ', euler_errors)
