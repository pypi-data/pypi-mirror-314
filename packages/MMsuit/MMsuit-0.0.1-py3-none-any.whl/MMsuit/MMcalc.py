#Dependencies

#Load Packages
from scipy import stats
from scipy import optimize as op
import numpy as np
import plotly.graph_objects as go

# Data Handler
def MMhandler(data):
    """
    Validates that both sets in the tuple contain only numeric values anf removes NaNs and corresponding indices from both sets adn aises a ValueError if non-numeric values are found.

    Input: Substrate Velocity data (tuple): A tuple of two numpy arrays.
     Returns: tuple: Filtered data with NaNs removed.
    """
    # Make sure the input is a tuple with two numpy arrays
    if not (isinstance(data, tuple) and len(data) == 2):
        raise ValueError("Input must be a tuple with two numpy arrays.")
    # Check if any element in both sets is non-numeric
    if not (np.issubdtype(data[0].dtype, np.number) and np.issubdtype(data[1].dtype, np.number)):
        raise ValueError("Both sets must contain only numeric values.")
    # Mask nan entries in both sets
    mask = ~np.isnan(data[0]) & ~np.isnan(data[1])
    # Filter
    filtered_data = (data[0][mask], data[1][mask])
    return filtered_data

# Define equations
def MMvelocity(S:float, Km:float, Vmax:float)-> float:
    '''
    Calculates velocity by computing michaelis Menten equation

    Inputs: Michaelis-Menten equation parameters (S, Km, Vmax).
    Output: Velocity for given S
    '''
    return Vmax*S/(Km + S)

def kcat(Vmax: float,Et: float) -> float:
    '''
    Calculates enzyme catalytic constant given maximum velocity and enzyme concentration (Et).

    Inputs: Vmax and Et {Enzyme active site concentration}.
    Output: Kcat
    '''
    return Vmax/Et

def LBfitter(eSV: tuple):
    '''
    Given substrates and velocity data, the function removes outliers by computing z-score, fits data to Lineweaver-Burk equation and optimizes fitting using sum of squares

    Inputs: eSV:(Experimental data) tuple with two arrays (substrate array, velocities array)
    :return: tuple with two arrays of fitted data (substrate array, velocities array), Km, Vmax, Vmax standard error and Vmax 95% Confidence interval
    '''
    # Handle data
    eSV = MMhandler(eSV)

    srecep = 1/(eSV[0]) # substrates
    vrecep = 1/(eSV[1]) # velocities
    #Calculate zscore to remove outliers (> 2 SD)
    z_scores = stats.zscore(vrecep)
    filtered_vrecep = vrecep[np.abs(z_scores) < 2]
    filtered_srecep = np.delete(srecep, np.where(np.abs(z_scores) > 2)) #Remove corresponding indices from substrate concentrations
    def objective(params):
        slope, intercept = params
        y_pred = slope * filtered_srecep + intercept
        return np.sum((filtered_vrecep - y_pred) ** 2)  # Minimize the residual sum of squares
    # Initial guess by linear regression of LB equation
    initial_slope, initial_intercept, *_ = stats.linregress(filtered_srecep, filtered_vrecep)
    bounds = [(-np.inf, np.inf), (0, np.inf)]      # Reject negative values for y-intercept
    # Optimization
    optimized = op.minimize(
        objective,
        x0=[initial_slope, max(0, initial_intercept),],
        bounds=bounds
    )

    # Extract optimized parameters
    slope, intercept = optimized.x

    Vmax = 1 / intercept
    Km = Vmax * slope

    # Calculate Std error (Prof Herbert Recommendation) [I had to do it manually]
    predicted = slope * srecep + intercept
    residuals = 1/vrecep - 1/predicted
    residual_variance = np.sum(residuals ** 2) / (len(srecep) - 2)
    # Standard error for slope and intercept
    x_mean = np.mean(1/srecep)
    Vmax_stderr = np.sqrt(residual_variance * (1 / len(srecep) + x_mean ** 2 / np.sum(((1/srecep) - x_mean) ** 2)))
    # Confidence Intervals for slope and intercept
    #minslope95, maxslope95 = x_mean - (slope_stderr * 1.96), x_mean + (slope_stderr * 1.96)
    minVmax95, maxVmax95 = Vmax - (Vmax_stderr * 1.96), Vmax + (Vmax_stderr * 1.96)
    ###
    fittedx = srecep
    fittedx = np.insert(fittedx, [0,0], [-1/Km,0])
    fittedy = (slope*fittedx)+intercept
    fittedLB = (fittedx, fittedy)
    return fittedLB, Km, Vmax , Vmax_stderr, [minVmax95, maxVmax95]

def MMfitter(eSV: tuple):
    '''
    Fits velocity and substrate data to Michaelis Menten equation and optimizes fitting using sum of squares
    N.B. the function uses LBfitter to compute an initial guess for Michaelis Menten parameters
    Inputs:
    eSV: (Experimental data) tuple with two arrays (substrate array, velocities array)
    :return: tuple with two arrays of fitted data (substrate array, velocities array), optimized parameters, covariance of optimized parameters,
    results.success {boolean for the occurance of minimization}, SSR: Minimized sum of squared residuals
    '''
    # Handle data
    eSV = MMhandler(eSV)
    def residual_sum_of_squares(params):
        Vmax, Km = params
        predicted = MMvelocity(eSV[0], Vmax, Km)
        residuals = eSV[1] - predicted
        return np.sum(residuals ** 2)  # Sum of squared residuals

    # Initial guess for Vmax and Km using LBfitter
    LBfunc = LBfitter(eSV)
    initial_guess = [LBfunc[2], LBfunc[1]]

    # Minimize the RSS
    result = op.minimize(residual_sum_of_squares, initial_guess, bounds=[(0, None), (0, None)])
    popt = result.x  # Optimized parameters

    # Covariance estimation from curve_fit for comparison
    popt_curvefit, pcov_curvefit = op.curve_fit(MMvelocity, eSV[0], eSV[1])

    # Fitted substrate and velocities using minimized parameters
    fittedSV = (eSV[0], MMvelocity(eSV[0], *popt))
    SSR = result.fun # The minimized sum of squared residuals

    return fittedSV, popt, pcov_curvefit, result.success, SSR

#Plotting functions
def MMplot(expSV):
    '''
    A function for interactive plotting of Michaelis Menten equation after fitting using MMfitter.

    Inputs: expSV: (Experimental data) tuple with two arrays (substrate array, velocities array)
    returns: Michaelis-Menten plot with experimental and fitted data.
    '''
    # Handle data
    expSV = MMhandler(expSV)

    figMM = go.Figure()
    figMM.add_trace(go.Scatter(x=expSV[0], y=expSV[1], mode='markers', name='Experimental'))  # Experimental as scatter
    fitted = MMfitter(expSV)
    figMM.add_trace(go.Line(x=fitted[0][0], y=fitted[0][1], mode='lines', name='Fitted'))  # Fitted as line
    figMM.update_layout(title='Michaelis-Menten Plot', xaxis_title='Substrate concentration', yaxis_title='Velocity')
    #figMM.show()
    return figMM

def MMsimulator(Km:float,Vmax:float):
    '''
    A function that uses MM velocity to simulate Michaelis-Menten graph for given Km and Vmax

    Inputs: Km, Vmax
    :return: simulated Michaelis-Menten plot
    '''
    xsimulate = np.linspace(Km*(0.1),Km*10,100)
    ysimulate = MMvelocity(xsimulate,Km,Vmax)
    LBx = 1/xsimulate
    LBy = 1/ysimulate
    simulatedMM = go.Figure()
    simulatedMM.add_trace(go.Scatter(x=xsimulate, y=ysimulate, mode='lines', name='Simulated'))
    simulatedMM.update_layout(title='Michaelis-Menten Plot', xaxis_title='Substrate concentration', yaxis_title='Velocity')

    simulatedLB = go.Figure()
    simulatedLB.add_trace(go.Scatter(x=LBx, y=LBy, mode='lines', name='Simulated'))
    simulatedLB.update_layout(title='Lineweaver-Burk Plot', xaxis_title='1/Substrate concentration',
                              yaxis_title='1/Velocity')
    #figsimulate.show()
    return simulatedMM, simulatedLB

def LBplot(expSV:tuple):
    '''
    A function for interactive plotting of Lineweaver-Burk plot equation after fitting using LBfitter.

    Inputs: expSV: (Experimental data) tuple with two arrays (substrate array, velocities array)
    returns: Lineweaver-Burk plot with experimental and fitted data.
    '''
    # Handle data
    expSV = MMhandler(expSV)\

    srecep = 1 / (expSV[0]) # substrats
    vrecep = 1 / (expSV[1]) # velocities
    figLB = go.Figure()
    figLB.add_trace(go.Scatter(x=srecep, y=vrecep, mode='markers', name='Experimental'))  # Experimental as scatter
    LBfitted = LBfitter(expSV)
    figLB.add_trace(go.Line(x= LBfitted[0][0], y=LBfitted[0][1], mode='lines', name='Fitted'))  # Fitted as line
    figLB.update_layout(title='Lineweaver-Burk Plot', xaxis_title='1/Substrate', yaxis_title='1/Velocity')
    #figLB.show()
    return figLB

