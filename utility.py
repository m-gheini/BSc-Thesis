def getTechnicalCoefficients(Z, X):
    return Z.div(X.iloc[0] + 0.000000001)