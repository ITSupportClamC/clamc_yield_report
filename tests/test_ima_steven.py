# coding=utf-8
# 

import unittest2
from clamc_yield_report.ima import getCurrentDirectory \
								, getDailyInterestAccrualDetailPositions \
								, getTaxlotInterestIncome
from os.path import join



class TestImaSteven(unittest2.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestImaSteven, self).__init__(*args, **kwargs)



	def testReadDailyInterestAccrualDetailTxtReport(self):
		inputFile = join(getCurrentDirectory(), 'samples', 'daily interest 2020-01.txt')
		positions = list(getDailyInterestAccrualDetailPositions(inputFile))
		self.assertEqual(19641, len(positions))
		self.verifyDailyTaxlotAccrualDetailPosition(positions[2])



	def testGetTaxlotInterestIncome(self):
		d = getTaxlotInterestIncome(
				list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2019-12.txt')
					))

			  , list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-01.txt')
					))
			)

		self.assertEqual(True, all(d[key] >=0 for key in d))

		# Total interest income in 2020 Jan
		self.assertAlmostEqual(790093159.63, sum(d[key] for key in d), 2)



	def testGetTaxlotInterestIncome2(self):
		d = getTaxlotInterestIncome(
				list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-01.txt')
					))

			  , list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-02.txt')
					))
			)

		# going to cross check per position, whether
		# investment level interest income == sum of tax lot level interest income
		# FIXME: to be implemented



	def verifyDailyTaxlotAccrualDetailPosition(self, position):
		self.assertEqual('Portfolio (  )', position['PortfolioInfo'])
		self.assertEqual( 'DE000LB1P2W1 HTM (LBBW 5 02/28/33 EMTN)'
						, position['Investment'])
		self.assertEqual('2020-01-02', position['Date'])
		self.assertEqual(185000000, position['Textbox84'])
		self.assertEqual('1028327', position['LotID'])
		self.assertEqual(37000000, position['LotQuantity'])
		self.assertEqual(5003864.58, position['LotSumOfEndBalanceBook'])
		self.assertEqual(5138.89, position['LotSumOfChangeAILocal'])
		self.assertEqual(637222.22, position['LotSumOfBeginBalanceLocal'])