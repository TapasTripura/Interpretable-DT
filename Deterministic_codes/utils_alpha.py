"""
This code belongs to the paper:
-- Probabilistic machine learning based predictive and interpretable digital
    twin for dynamical systems, authored by,
    Tapas Tripura, Aarya Sheetal Desai, Sondipon Adhikari, Souvik Chakraborty
   
*** This code contains useful functions.
"""

import numpy as np
from scipy import linalg as SLA
from sklearn.metrics import mean_squared_error as MSE

from numpy import linalg as LA
from numpy.random import gamma as IG
from numpy.random import beta
from numpy.random import binomial as bern
from numpy.random import multivariate_normal as mvrv

from scipy.special import loggamma as LG



"""
The Dictionary creation part:
"""
def library(xt, uv, polyn, tensor, harmonic, exponent):
    if polyn == 0:
        polyn = 1

    # The polynomial is (x1 + x2)^p, with p is the order
    # poly order 0
    ind = 0
    n = len(xt[0])
    D = np.ones([n,1])
    
    if polyn >= 1:
        # poly order 1
        for i in range(len(xt)):
            ind = ind+1
            new = np.vstack(xt[i,:])
            D = np.append(D, new, axis=1)
     
    if polyn >= 2: 
        # ploy order 2
        for i in range(len(xt)):
            for j in  range(i,len(xt)):
                ind = ind+1
                new = np.multiply(xt[i,:], xt[j,:])
                new = np.vstack(new)
                D = np.append(D, new, axis=1) 
    
    if polyn >= 3:    
        # ploy order 3
        for i in range(len(xt)):
            for j in  range(i,len(xt)):
                for k in  range(j,len(xt)):
                    ind = ind+1
                    new = np.multiply(np.multiply(xt[i,:], xt[j,:]), xt[k,:])
                    new = np.vstack(new)
                    D = np.append(D, new, axis=1) 
    
    if polyn >= 4:
        # ploy order 4
        for i in range(len(xt)):
            for j in  range(i,len(xt)):
                for k in  range(j,len(xt)):
                    for l in range(k,len(xt)):
                        ind = ind+1
                        new = np.multiply(np.multiply(xt[i,:], xt[j,:]), xt[k,:])
                        new = np.multiply(new, xt[l,:])
                        new = np.vstack(new)
                        D = np.append(D, new, axis=1) 
    
    if polyn >= 5:
        # ploy order 5
        for i in range(len(xt)):
            for j in  range(i,len(xt)):
                for k in  range(j,len(xt)):
                    for l in  range(k,len(xt)):
                        for m in  range(l,len(xt)):
                            ind = ind+1
                            new = np.multiply(xt[i,:], xt[j,:])
                            new = np.multiply(new, xt[k,:])
                            new = np.multiply(new, xt[l,:])
                            new = np.multiply(new, xt[m,:])
                            new = np.vstack(new)
                            D = np.append(D, new, axis=1) 
    
    if polyn >= 6:
        # ploy order 6
        for i in range(len(xt)):
            for j in  range(i,len(xt)):
                for k in  range(j,len(xt)):
                    for l in  range(k,len(xt)):
                        for m in  range(l,len(xt)):
                            for n in  range(m,len(xt)):
                                ind = ind+1
                                new = np.multiply(xt[i,:], xt[j,:])
                                new = np.multiply(new, xt[k,:])
                                new = np.multiply(new, xt[l,:])
                                new = np.multiply(new, xt[m,:])
                                new = np.multiply(new, xt[n,:])
                                new = np.vstack(new)
                                D = np.append(D, new, axis=1) 
    
    # for the signum or sign operator
    for i in range(len(xt)):
        ind = ind+1
        new = np.vstack(np.sign(xt[i,:]))
        D = np.append(D, new, axis=1)
        
    ## Exponential function for degradation:
    if exponent == 1: 
        ind = ind+1
        new = np.vstack(xt[0,:]*np.exp(-xt[2,:]))
        D = np.append(D, new, axis=1)
        
        ind = ind+1
        new = np.vstack(xt[1,:]*np.exp(-xt[2,:]))
        D = np.append(D, new, axis=1)
        
        ind = ind+1
        new = np.vstack(xt[2,:]*np.exp(-xt[2,:]))
        D = np.append(D, new, axis=1)
                
        # ind = ind+1
        # new = np.vstack(xt[0,:]*np.exp(-pow(xt[2,:],2)))
        # D = np.append(D, new, axis=1)
        
        # for i in range(len(xt)):
        #     for j in range(len(xt)):
        #         ind = ind+1
        #         new = np.vstack( np.multiply(np.exp(-xt[i,:]), xt[j,:]) )
        #         D = np.append(D, new, axis=1)
    
    # for the modulus operator
    if tensor == 1:
        for i in range(len(xt)):
            ind = ind+1
            new = np.vstack(abs(xt[i,:]))
            D = np.append(D, new, axis=1)
          
        # for the tensor operator
        for i in range(len(xt)):
            for j in  range(len(xt)):
                ind = ind+1
                new = np.multiply(xt[i,:],abs(xt[j,:]))
                new = np.vstack(new)
                D = np.append(D, new, axis=1)
            
    if harmonic == 1:
        # for sin(x)
        for i in range(len(xt)):
            ind = ind+1
            new = np.vstack(np.sin(xt[i,:]))
            D = np.append(D, new, axis=1)
            #  or,
            # ind = ind+1
            # new = np.sin(xt[i,:])
            # D = np.insert(D, ind, new, axis=1)
            
        # for cos(x)
        for i in range(len(xt)):
            ind = ind+1
            new = np.vstack(np.cos(xt[i,:]))
            D = np.append(D, new, axis=1)
    
    # The force vector u
    if np.isscalar(uv):
        ind = ind + 1
        D = np.append(D, new, axis=1)
    else:
        for i in range(len(uv)):
            ind = ind+1
            new = np.vstack(uv[i,:])
            D = np.append(D, new, axis=1)
        
    ind = len(D[0])
    return D, ind



"""
Theta: Multivariate Normal distribution
"""
def sigmu(z, D, vs, xdts):
    index = np.array(np.where(z != 0))
    index = np.reshape(index,-1) # converting to 1-D array, 
    Dr = D[:,index] 
    Aor = np.eye(len(index)) # independent prior
    # Aor = np.dot(len(Dr), LA.inv(np.matmul(Dr.T, Dr))) # g-prior
    BSIG = LA.inv(np.matmul(Dr.T,Dr) + np.dot(pow(vs,-1), LA.inv(Aor)))
    mu = np.matmul(np.matmul(BSIG,Dr.T),xdts)
    return mu, BSIG, Aor, index

"""
P(Y|zi=(0|1),z-i,vs)
"""
def pyzv(D, ztemp, vs, N, xdts, asig, bsig):
    rind = np.array(np.where(ztemp != 0))[0]
    rind = np.reshape(rind, -1) # converting to 1-D array,   
    Sz = sum(ztemp)
    Dr = D[:, rind] 
    Aor = np.eye(len(rind)) # independent prior
    # Aor = np.dot(N, LA.inv(np.matmul(Dr.T, Dr))) # g-prior
    BSIG = np.matmul(Dr.T, Dr) + np.dot(pow(vs, -1),LA.inv(Aor))
    
    (sign, logdet0) = LA.slogdet(LA.inv(Aor))
    (sign, logdet1) = LA.slogdet(LA.inv(BSIG))
    
    PZ = LG(asig + 0.5*N) -0.5*N*np.log(2*np.pi) - 0.5*Sz*np.log(vs) \
        + asig*np.log(bsig) - LG(asig) + 0.5*logdet0 + 0.5*logdet1
    denom1 = np.eye(N) - np.matmul(np.matmul(Dr, LA.inv(BSIG)), Dr.T)
    denom = (0.5*np.matmul(np.matmul(xdts.T, denom1), xdts))
    PZ = PZ - (asig+0.5*N)*(np.log(bsig + denom))
    return PZ

"""
P(Y|zi=0,z-i,vs)
"""
def pyzv0(xdts, N, asig, bsig):
    PZ0 = LG(asig + 0.5*N) - 0.5*N*np.log(2*np.pi) + asig*np.log(bsig) - LG(asig) \
        + np.log(1) - (asig+0.5*N)*np.log(bsig + 0.5*np.matmul(xdts.T, xdts))
    return PZ0



"""
Sparse regression with Normal Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
def sparse(xdts, ydata, uv, polyorder, tensor, harmonic, exponent, MCMC, burn_in):
    # Library creation:
    D, nl = library(ydata, uv, polyorder, tensor, harmonic, exponent)

    # Adding % of the std. of acceleration as noise:
    xdts = xdts + 0.02*np.random.normal(0, np.std(xdts), len(xdts))

    # Residual variance:
    err_var = res_var(D, xdts)

    """
    # Gibbs sampling:
    """
    # Hyper-parameters
    ap, bp = 0.1, 1 # for beta prior for p0
    av, bv = 0.5, 0.5 # inverge gamma for vs
    asig, bsig = 1e-4, 1e-4 # invese gamma for sig^2

    # Parameter Initialisation:
    p0 = np.zeros(MCMC)
    vs = np.zeros(MCMC)
    sig = np.zeros(MCMC)
    p0[0] = 0.1
    vs[0] = 10
    sig[0] = err_var

    N = len(xdts)

    # Initial latent vector
    zval = np.zeros(nl)
    zint  = latent(nl, D, xdts)
    zstore = np.transpose(np.vstack([zint]))
    zval = zint

    zval0 = zval
    vs0 = vs[0]
    mu, BSIG, Aor, index = sigmu(zval0, D, vs0, xdts)
    Sz = sum(zval)

    # Sample theta from Normal distribution
    thetar = mvrv(mu, np.dot(sig[0], BSIG))
    thetat = np.zeros(nl)
    thetat[index] = thetar
    theta = np.vstack(thetat)

    for i in range(1, MCMC): 
        if i % 50 == 0:
            print('MCMC: ', i)
        # sample z from the Bernoulli distribution:
        zr = np.zeros(nl) # instantaneous latent vector (z_i):
        zr = zval
        for j in range(nl):
            ztemp0 = zr
            ztemp0[j] = 0
            if np.mean(ztemp0) == 0:
                PZ0 = pyzv0(xdts, N, asig, bsig)
            else:
                vst0 = vs[i-1]
                PZ0 = pyzv(D, ztemp0, vst0, N, xdts, asig, bsig)
            
            ztemp1 = zr
            ztemp1[j] = 1      
            vst1 = vs[i-1]
            PZ1 = pyzv(D, ztemp1, vst1, N, xdts, asig, bsig)
            
            zeta = PZ0 - PZ1  
            zeta = p0[i-1]/( p0[i-1] + np.exp(zeta)*(1-p0[i-1]))
            zr[j] = bern(1, p = zeta, size = None)
        
        zval = zr
        zstore = np.append(zstore, np.vstack(zval), axis = 1)
        
        # sample sig^2 from inverse Gamma:
        asiggamma = asig+0.5*N
        temp = np.matmul(np.matmul(mu.T, LA.inv(BSIG)), mu)
        bsiggamma = bsig+0.5*(np.dot(xdts.T, xdts) - temp)
        sig[i] = 1/IG(asiggamma, 1/bsiggamma) # inverse gamma RVs
        
        # sample vs from inverse Gamma:
        avvs = av+0.5*Sz
        bvvs = bv+(np.matmul(np.matmul(thetar.T, LA.inv(Aor)), thetar))/(2*sig[i])
        vs[i] = 1/IG(avvs, 1/bvvs) # inverse gamma RVs
        
        # sample p0 from Beta distribution:
        app0 = ap+Sz
        bpp0 = bp+nl-Sz # Here, P=nl (no. of functions in library)
        p0[i] = beta(app0, bpp0)
        # or, np.random.beta()
        
        # Sample theta from Normal distribution:
        vstheta = vs[i]
        mu, BSIG, Aor, index = sigmu(zval, D, vstheta, xdts)
        Sz = sum(zval)
        thetar = mvrv(mu, np.dot(sig[i], BSIG))
        thetat = np.zeros(nl)
        thetat[index] = thetar
        theta = np.append(theta, np.vstack(thetat), axis = 1)

    # Marginal posterior inclusion probabilities (PIP):
    zstore = zstore[:, burn_in:] # discard the first burn_in samples
    Zmean = np.mean(zstore, axis=1)

    # Post processing:
    theta = theta[:, burn_in:] # discard the first burn_in samples
    mut = np.mean(theta, axis=1)
    sigt = np.cov(theta, bias = False)
    
    return zstore, Zmean, theta, mut, sigt



"""
# Bayesian Interference:
"""
def BayInt(D, xdt):
    # for the dictionary:
    muD = np.mean(D,0)
    sdvD1 = np.std(D,0)
    sdvD = np.diag(sdvD1)
    Ds = np.dot((D - np.ones([len(D),1])*muD), SLA.inv(sdvD))
    
    # for the observed data:
    muxdt = np.mean(xdt)
    xdts = np.vstack(xdt) - np.ones([len(D),1])*muxdt
    xdts = np.reshape(xdts, -1)
    
    return Ds, xdts, sdvD



"""
# Residual variance:
"""
def res_var(D, xdts):
    theta1 = np.dot(SLA.pinv(D), xdts)
    error = xdts - np.matmul(D, theta1)
    err_var = np.var(error)
    
    return err_var



"""
# Initial latent vector finder:
"""
def latent(nl, D, xdts):
    # Forward finder:
    zint = np.zeros(nl)
    theta = np.matmul(SLA.pinv(D), xdts)
    index = np.array(np.where(zint != 0))[0]
    index = np.reshape(index,-1) # converting to 1-D array,
    Dr = D[:, index]
    thetar = theta[index]
    err = MSE(xdts, np.dot(Dr, thetar))
    for i in range(0, nl):
        index = i
        Dr = D[:, index]
        thetar = theta[index]
        err = np.append(err, MSE(xdts, np.dot(Dr, thetar)) )
        if err[i+1] <= err[i]:
            zint[index] = 1
        else:
            zint[index] = 0
    
    # Backward finder:
    index = np.array(np.where(zint != 0))
    index = np.reshape(index,-1) # converting to 1-D array,
    Dr = D[:, index]
    thetar = theta[index]
    err = MSE(xdts, np.dot(Dr, thetar))
    ind = 0
    for i in range(nl-1, -1, -1):
        index = ind
        Dr = D[:, index]
        thetar = theta[index]
        err = np.append(err, MSE(xdts, np.dot(Dr, thetar)) )
        if err[ind+1] <= err[ind]:
            zint[index] = 1
        else:
            zint[index] = 0
        ind = ind + 1
    
    # for the states
    zint[[0, 1]] = [1, 1]
    return zint
