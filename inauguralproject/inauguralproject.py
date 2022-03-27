def utility(z, theta):
    """ Calculates utility of the agent.
    
    Args: 
    
        z
        theta (int): model parameter
        
    Returns: 
        
        (float): Utility of agent.
    
    """
    
    u = (z**(1+theta))/(1+theta)
    return u

def exp_utility(q, x, y, p):
    """Calculates expected utility of an insured agent.
    
    Args: 
        
        q (int): coverage amount
        x (float): monetary loss
        y (int): assets hold by agent
        p (float): probability of a loss incurring
        
    Returns: 
        
        (float): Expected utility of an insured agent """
    
    V = p*utility(y-x+(1-p)*q, theta) + (1-p)*utility(y-p*q, theta)
    return V

def q_optimize(x, y, p):
    """ Calculates the agents optimal insurance coverage q*
    
    x (float): monetary loss
        y (int): assets hold by agent
        p (float): probability of a loss incurring
        
    Returns: 
        
        (float): Optimal insurance coverage """
    
    obj = lambda q: -exp_utility(q, x, y, p)
    res = optimize.minimize_scalar(obj, bounds=(0, 1), method='bounded')
    return res.x

def V_pi(pi, q, x, y, p):
    """ Calculates expected utility of an insured agent.
    Args: 
        
        pi (float): insurance premium
        q (int): coverage amount
        x (float): monetary loss
        y (int): assets hold by agent
        p (float): probability of a loss incurring
        
    Returns: 
        
        (float): Expected utility of an insured agent """
    
    return p*utility(y-x+q-pi, theta) + (1-p)*utility(y-pi, theta)

def optimal_pi(q, x, y, p, V0):
    """ Calculates the value of the insurance premium which will make the agent indifferent.
    
    Args: 
        
        q (int): coverage amount
        x (float): monetary loss
        y (int): assets hold by agent
        p (float): probability of a loss incurring
        V0 (float): utility of agent without an insurance
        
    Returns: 
        
        (float): Value of the insurance premium which will make the agent indifferent """
    
    
    # objective function
    def obj(pi):
   
    
    
        return V_pi(pi, q, x, y, p) - V0
    # optimize
    res = optimize.root(obj, 0.1)
    return res.x

def g(x, y, gamma, pi):
    """ Calculates the altered value of the agent
    
    Args:
        
        pi (float): insurance premium
    
    Returns: 
        (float): value of agent """
    
    return utility(y-(1-gamma)*x-pi, theta)

def monte_carlo(y, p, gamma, pi, N):
    """ Calculates mean value of agent by Monte Carlo integration using N number of draws.
    
    Args: 
        y (int): assets hold by agent
        p (float): probability of a loss incurring
        gamma (float): [0,1] determines fraction of x that equals coverage amount
        pi: insurance premium
        N: number of draws
    
    Returns: 
        (float): value of agent"""
    
    np.random.seed(123)
    # Draws of X
    xlist = np.random.beta(alpha, beta, N)
    return np.mean(g(xlist, y, gamma, pi))

def optimal_pi2(y, p, gamma, pi, N, V0):
    """ Calculates the value of the insurance premium which will make the agent indifferent in a Monte Carlo simulation

    Args: 
        y (int): assets hold by agent
        p (float): probability of a loss incurring
        gamma (float): [0,1] determines fraction of x that equals coverage amount
        pi: insurance premium
        N: number of draws
        V0 (float): utility of agent without an insurance
    
    Returns: 
        (float): value of agent"""
    
    def obj(pi): 
        return monte_carlo(y, p, gamma, pi, N) - V0
    # Optimize
    res = optimize.root(obj, 0.1, method="broyden1")
    return res.x