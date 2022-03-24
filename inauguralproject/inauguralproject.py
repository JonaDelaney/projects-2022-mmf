def utility(z, eta):
    u = (z**(1+eta))/(1+eta)
    return u

def exp_utility(q, x, y, p):
    
    z1 = y-x+q-p*q
    z2 = y-p*q
    return p*utility(z1, eta) + (1-p)*utility(z2, eta)