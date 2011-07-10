#!/usr/bin/env python

import unittest

from tests.test_index import TestIndex
from tests.test_host import TestHost

testCases = [TestIndex, TestHost]

if __name__ == '__main__':
    suites = [ unittest.TestLoader().loadTestsFromTestCase(testCase) for testCase in testCases]
    for suite in suites:
        unittest.TextTestRunner(verbosity=2).run(suite)
