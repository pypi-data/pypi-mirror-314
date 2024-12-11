import numpy as np

def AdjustedRV(X1, X2, version='Maye', center=True):
    # Helper function to calculate the trace of a matrix
    def trace(mat):
        return np.trace(mat)
    
    # Helper function to standardize the columns of a matrix
    def standardize(mat):
        return (mat - np.mean(mat, axis=0)) / np.std(mat, axis=0, ddof=1)
    
    # Center the matrices by subtracting the mean of each column, if specified
    if center:
        X1 -= np.mean(X1, axis=0)
        X2 -= np.mean(X2, axis=0)
    
    # Get the number of rows and columns in X1 and the number of columns in X2
    n, p = X1.shape
    q = X2.shape[1]
    
    # Compute the cross-product matrices for X1 and X2
    AA = X1 @ X1.T
    BB = X2 @ X2.T
    
    if version == 'Maye':
        # Calculate the products of the number of columns
        pq = p * q
        pp = p * p
        qq = q * q
        
        # Standardize X1 and X2 if needed
        X1s = standardize(X1)
        X2s = standardize(X2)
        AAs = X1s @ X1s.T
        BBs = X2s @ X2s.T
        
        # Calculate intermediate values for RV adjustment
        xy = trace(AAs @ BBs) / (pq - (n-1) / (n-2) * (pq - trace(AAs @ BBs) / (n-1)**2))
        xx = trace(AAs @ AAs) / (pp - (n-1) / (n-2) * (pp - trace(AAs @ AAs) / (n-1)**2))
        yy = trace(BBs @ BBs) / (qq - (n-1) / (n-2) * (qq - trace(BBs @ BBs) / (n-1)**2))
        
        # Calculate the adjusted RV value
        RVadj_value = (trace(AA @ BB) / xy) / (np.sqrt(trace(AA @ AA) / xx * trace(BB @ BB) / yy))
        return RVadj_value
    
    elif version == 'Ghaziri':
        # Calculate the RV coefficient
        rv = trace(AA @ BB) / np.sqrt(trace(AA @ AA) * trace(BB @ BB))
        # Calculate the mean RV under the null hypothesis
        mrvB = np.sqrt(trace(AA)**2 / trace(AA @ AA)) * np.sqrt(trace(BB)**2 / trace(BB @ BB)) / (n - 1)
        # Adjusted RV coefficient
        aRV = (rv - mrvB) / (1 - mrvB)
        return aRV
    
    else:
        raise ValueError("Unsupported or misspelled version of RV adjusted. Use 'Maye' or 'Ghaziri'.")
