def outlier(n):
    import numpy as np
    data = n
    
    q1= np.percentile(data,25)
    q2= np.percentile(data,50)
    q3= np.percentile(data,75)
    
    iqr = q3 - q1
    
    ub = q3 + 1.5 * iqr
    lb = q1 - 1.5 * iqr
    

    
	
    return (f'lower bound = {lb},upper bound = {ub}')

def value(n):
    import numpy as np
    data = n
    
    q1= np.percentile(data,25)
    q3= np.percentile(data,75)
    
    iqr = q3 - q1
    
    ub = q3 + 1.5 * iqr
    lb = q1 - 1.5 * iqr
	
    return list(data[np.where((data<lb) | (data>ub))[0]])

def index(n):
    import numpy as np
    data = n
    
    q1= np.percentile(data,25)
    q3= np.percentile(data,75)
    
    iqr = q3 - q1
    
    ub = q3 + 1.5 * iqr
    lb = q1 - 1.5 * iqr
	
    return list(np.where((data<lb) | (data>ub))[0])
