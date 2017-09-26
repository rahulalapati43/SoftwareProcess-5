from unittest import TestCase
import math
from TDD.prob import prob
from TDD.prob import gamma
from TDD.prob import calculateConstant
from TDD.prob import f
from TDD.prob import integrate


class ProbTest(TestCase):
    def setUp(self):
        self.nominalN = 4
        self.nominalT = 1.4398
        self.nominalTails = 1
        self.inputDictionary = {}
        self.errorKey = "gameStatus"
        self.errorValue = "error:"
        self.solutionKey = "probability"

    def tearDown(self):
        self.inputDictionary = {}

    def setT(self, t):
        self.inputDictionary["t"] = t

    def setN(self, n):
        self.inputDictionary["n"] = n

    def setTails(self, tails):
        self.inputDictionary["tails"] = tails


    # 100 prob
    #    Desired level of confidence:    boundary value analysis
    #    Input-output Analysis
    #        inputs:        n -> integer, .GE.3, mandatory, unvalidated
    #                       t ->    float > 0.0, mandatory, unvalidated
    #                       tails -> integer, 1 or 2, optional, defaults to 1
    #        outputs:    float .GT. 0 .LE. 1.0
    #    Happy path analysis:
    #       n:       nominal value    n=6
    #                low bound        n=3
    #        t:      nominal value    t=1.4398
    #                low bound        t>0.0
    #        tails:  value 1          tails = 1
    #                value 2          tails = 2
    #                missing tails
    #        output:
    #                The output is an interaction of t x tails x n:
    #                    nominal t, 1 tail
    #                    nominal t, 2 tails
    #                    low n, low t, 1 tail
    #                    low n, low t, 2 tails
    #                    high n, low t, 1 tail
    #                    high n, low t, 2 tails
    #                    low n, high t, 1 tail
    #                    low n, high t, 2 tails
    #                    high n, high t, 1 tail
    #                    high n, high t, 2 tails
    #                    nominal t, default tails
    #    Sad path analysis:
    #        n:      missing n
    #                out-of-bound n   n<3
    #                non-integer n    n = 2.5
    #        t:      missing t
    #                out-of-bounds n  t<0.0
    #                non-numeric t    t="abc"
    #        tails:  invalid tails    tails = 3
    #
    # Happy path
    def test100_010ShouldCalculateNominalCase1Tail(self):
        self.setT(1.8946)
        self.setN(7)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.950, 3)


    def test100_020ShouldCalculateNominalCase2Tail(self):
        self.setT(1.8946)
        self.setN(7)
        self.setTails(2)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.900, 3)

    def test100_030ShouldCalculateLowNLowT1TailEdgeCase(self):
        self.setT(0.2767)
        self.setN(3)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.600, 3)

    def test100_040ShouldCalculateLowNLowT2TailEdgeCase(self):
        self.setT(0.2767)
        self.setN(3)
        self.setTails(2)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.200, 3)

    def test100_050ShouldCalculateHighNLowT1TailEdgeCase(self):
        self.setT(0.2567)
        self.setN(20)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.600, 3)

    def test100_060ShouldCalculateHighNLowT2TailEdgeCase(self):
        self.setT(0.2567)
        self.setN(20)
        self.setTails(2)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.200, 3)

    def test100_070ShouldCalculateLowNHighT1EdgeCase(self):
        self.setT(5.8409)
        self.setN(3)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.995, 3)

    def test100_080ShouldCalculateLowNHighT2EdgeCase(self):
        self.setT(5.8409)
        self.setN(3)
        self.setTails(2)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.990, 3)

    def test100_090ShouldCalculateHighHighT1TailEdgeCase(self):
        self.setT(2.8453)
        self.setN(20)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.995, 3)

    def test100_100ShouldCalculateHighHighT2TailEdgeCase(self):
        self.setT(2.8453)
        self.setN(20)
        self.setTails(2)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.990, 3)

    def test100_110ShouldCalculateWithDefaultTails(self):
        self.setT(1.8946)
        self.setN(7)
        resultDictionary = prob(self.inputDictionary)
        self.assertAlmostEqual(resultDictionary[self.solutionKey], 0.950, 3)

    # Sad path
    def test100_910ShouldRaiseExceptionOnMissingT(self):
        self.setN(self.nominalN)
        self.setTails(self.nominalTails)
        resultDictionary = prob(self.inputDictionary)
        self.assertIn(self.errorKey, resultDictionary)
        self.assertIn(self.errorValue, resultDictionary[self.errorKey])

    def test100_920ShouldRaiseExceptionOnOutOfBoundsT(self):
        self.setT(-1.0)
        self.setN(self.nominalN)
        self.setTails(self.nominalTails)
        resultDictionary = prob(self.inputDictionary)
        self.assertIn(self.errorKey, resultDictionary)
        self.assertIn(self.errorValue, resultDictionary[self.errorKey])

    def test100_930ShouldRaiseExceptionOnNonNumericT(self):
        self.setT("abc")
        self.setN(self.nominalN)
        self.setTails(self.nominalTails)
        resultDictionary = prob(self.inputDictionary)
        self.assertIn(self.errorKey, resultDictionary)
        self.assertIn(self.errorValue, resultDictionary[self.errorKey])

    def test100_940ShouldRaiseExceptionOnInvalidTails(self):
        self.setTails(0)
        self.setT(self.nominalT)
        self.setN(self.nominalN)
        resultDictionary = prob(self.inputDictionary)
        self.assertIn(self.errorKey, resultDictionary)
        self.assertIn(self.errorValue, resultDictionary[self.errorKey])

    def test100_950ShouldRaiseExceptionOnMissingN(self):
        self.setT(self.nominalT)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertIn(self.errorKey, resultDictionary)
        self.assertIn(self.errorValue, resultDictionary[self.errorKey])

    def test100_960ShouldRaiseExceptionOnOutOfBoundN(self):
        self.setN(0)
        self.setT(self.nominalT)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertIn(self.errorKey, resultDictionary)
        self.assertIn(self.errorValue, resultDictionary[self.errorKey])

    def test100_970ShouldRaiseExceptionOnNonIntegerN(self):
        self.setN(2.5)
        self.setT(self.nominalT)
        self.setTails(1)
        resultDictionary = prob(self.inputDictionary)
        self.assertIn(self.errorKey, resultDictionary)
        self.assertIn(self.errorValue, resultDictionary[self.errorKey])

    #
    # --------------------------------------------------------------------
    # Architecture:
    #    p -> calculateConstant
    #    p -> integrate
    #    calculateConstant -> gamma
    #    integrate -> f
    #
    # ---- Unit tests
    #
    # 200 gamma
    #     Analysis
    #        inputs:
    #            x ->  n umeric (either integer or integer/2, mandatory validated
    #     Happy path:
    #            x:    termination condition    x=1
    #                  termination condition    x=1/2
    #                  nominal value            x=5
    #                  nominal value            x=5/2
    #     Sad path:
    #            none ... x is pre-validated
    #

    def test200_010_ShouldReturnUpperTerminationCondition(self):
        self.assertEquals(gamma(1), 1.0)

    def test200_020_ShouldReturnLowerTerminationCondition(self):
        self.assertAlmostEquals(gamma(1.0 / 2.0), math.sqrt(math.pi), 3)

    def test200_030_ShouldWorkOnIntegralX(self):
        self.assertEquals(gamma(5), 24)

    def test200_030_ShouldWorkOnHalfX(self):
        self.assertAlmostEquals(gamma(5.0 / 2.0), 1.329, 3)

    # 300 calculateConstant
    # Analysis
    #     inputs
    #        n -> numeric  mandatory validated
    #    outputs
    #        float .GE. 0
    #
    #     Happy path
    #        n:    nominal case     n=5
    #     Sad path
    #        none ... will prevalidate

    def test300_010_ShouldCalculateLHP(self):
        self.assertAlmostEquals(calculateConstant(5), 0.37960669, 4)

    # 400 f
    # Analysis
    #    inputs
    #        n -> numeric mandatory validated
    #        u -> float mandatory validated
    #    outputs
    #        float .GE. 0
    # Happy path
    #    nominal case:  f(1) -> 0.5787
    # Sad path
    #            none ... x is pre-validated

    def test400_010_ShouldCalculateFStarterCase(self):
        self.assertAlmostEquals(f(0, 5), 1, 4)

    def test400_020_ShouldCalculateF(self):
        self.assertAlmostEquals(f(1, 5), 0.578703704)


    # 500 integrate
    # Analysis
    #    inputs
    #        t -> numeric mandatory validated
    #        f -> function mandatory validated
    #        n -> integer mandatory validated
    #    outputs
    #        float .GE. 0
    # Happy path
    #
    # Sad path
    #            none ... all inputs are pre-validated


