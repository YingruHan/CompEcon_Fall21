import numpy as np
#Transition equation: not needed - replace x(t+1) with y-D


# Total cost for period t
def TC(c, y, x, h, b, D):
    TC = c * (y - x) + np.trapz(np.where(y > D, h*(y-D), b*(y-D)), D)
    return TC
