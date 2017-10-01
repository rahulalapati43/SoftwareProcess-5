import math

# Outward facing method(s)
def prob(parmDictionary):
    ERROR_HEADER = "error: "
    ERROR_KEY = "gameStatus"
    RESULT_KEY = "probability"
    DEFAULT_TAILS = 1
    resultDict = {}

    # Validate input parameter values
    try:
        # Validate n
        if(not("n" in parmDictionary)):
            raise ValueError("missing n")
        n = parmDictionary["n"]
        if (not(isinstance(n, int))):
            raise ValueError("non-integer n")
        elif (n < 1):
            raise ValueError("out-of-bounds n")

        # Validate t
        if (not ("t" in parmDictionary)):
            raise ValueError("missing t")
        t = parmDictionary["t"]
        if (not (isinstance(t, float))):
            raise ValueError("non-float t")
        if (t < 0.0):
            raise ValueError("out-of-bounds t")

        # Validate tails
        if (not ("tails" in parmDictionary)):
            tails = DEFAULT_TAILS
        else:
            tails = parmDictionary["tails"]
            if (not (isinstance(tails, int))):
                raise ValueError("non-integer tails")
            if ((tails != 1) & (tails != 2)):
                raise ValueError("invalid tails")
    # Catch validation problems and return error diagnostic
    except Exception as e:
        resultDict[ERROR_KEY] = ERROR_HEADER + e.args[0]
        return resultDict

    # Calculate probability
    constant = calculateConstant(n)
    integration = integrate(t, n, f)
    if (tails == 1):
        result = constant * integration + 0.5
    else:
        result = constant * integration * 2

    resultDict[RESULT_KEY] = result
    return resultDict

#---------------------------------------------------------------------------
# Internal methods
def gamma(x):
    if (x == 1):
        return 1
    if (x == 0.5):
        return math.sqrt(math.pi)
    return (x - 1) * gamma(x - 1)

def calculateConstant(n):
    n = float(n)
    numerator = gamma((n + 1.0) / 2.0)
    denominator = gamma(n / 2.0) * math.sqrt(n * math.pi)
    result = numerator / denominator
    return result

def f(u, n):
    n = float(n)
    base = (1 + (u ** 2) / n)
    exponent = -(n + 1.0) / 2.0
    result = base ** exponent
    return result

# ----------- PLEASE COMPLETE THE FUNCTION BELOW ----------
def integrate(t, n, f):
    lowBound = 0.0
    highBound = t
    s = 4
    w = (highBound - lowBound) / float(s)

    sumEven = 0.0
    for i in range(2, ((s / 2) + 1), 2):
        sumEven = sumEven + (f((lowBound + ((i - 1) * w)), n) + f((highBound - ((i - 1) * w)), n))
    sumEven = 4 * sumEven

    sumOdd = 0.0
    for j in range(3, ((s / 2) + 2), 2):
        if (j != ((s / 2) + 1)):
            sumOdd = sumOdd + (f((lowBound + ((j - 1) * w)), n) + f((highBound - ((j - 1) * w)), n))
        elif (j == ((s / 2) + 1)):
            sumOdd = sumOdd + (f((lowBound + ((j - 1) * w)), n))
    sumOdd = 2 * sumOdd

    simpsonOld = (w / 3) * (f(lowBound, n) + sumEven + sumOdd + f(t, n))

    s = 8
    w = (highBound - lowBound) / float(s)

    sumEven = 0.0
    for i in range(2, ((s / 2) + 1), 2):
        sumEven = sumEven + (f((lowBound + ((i - 1) * w)), n) + f((highBound - ((i - 1) * w)), n))
    sumEven = 4 * sumEven

    sumOdd = 0.0
    for j in range(3, ((s / 2) + 2), 2):
        if (j != ((s / 2) + 1)):
            sumOdd = sumOdd + (f((lowBound + ((j - 1) * w)), n) + f((highBound - ((j - 1) * w)), n))
        elif (j == ((s / 2) + 1)):
            sumOdd = sumOdd + (f((lowBound + ((j - 1) * w)), n))
    sumOdd = 2 * sumOdd

    simpsonNew = (w / 3) * (f(lowBound, n) + sumEven + sumOdd + f(t, n))

    if (abs((simpsonNew - simpsonOld) / simpsonOld) <= 0.001):
        return simpsonNew



