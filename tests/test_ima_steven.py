# coding=utf-8
# 

import unittest2
from clamc_yield_report.ima import getCurrentDirectory \
								, getDailyInterestAccrualDetailPositions \
								, getTaxlotInterestIncome \
								, getTaxlotInterestDetail
from os.path import join



def getCNEnergyTaxlots():
	#1010330 apeears on for 2020-02
	#'1005226', '1008069', '1005786', '1008093' apeears on 2020-04
	return set(('1010330', '1005226', '1008069', '1005786', '1008093'))



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
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-01.txt')
					))
			)

		# CNOOC 7.5 07/30/39
		self.assertAlmostEqual(239735.21, d['1104216'], 2)
		self.assertAlmostEqual(239735.21, d['1104217'], 2)
		self.assertAlmostEqual(239735.21, d['1104496'], 2)
		self.assertAlmostEqual( 47947.05, d['1104497'], 2)
		self.assertAlmostEqual(144793.52, d['1109831'], 2)
		self.assertAlmostEqual(240634.82, d['1110346'], 2)

		# GBHK 2.93 01/13/20
		self.assertAlmostEqual( 47104.76, d['1108340'], 2)

		self.assertEqual(
			True
		  , all(key in getCNEnergyTaxlots() or d[key] >=0 for key in d)
		)

		"""
		Total interest income of bonds in 2020 Jan
		Total interest income from the profit loss report is
		811,203,318.61, a difference of 0.0141%. This is due to
		inaccurate ending AI of some positions (52 out of 125)
		in the daily interest accrual detail report. The ending AI
		from the tax lot appraisal report is accurate.
		"""
		self.assertAlmostEqual(811088743.30, sum(d[key] for key in d), 2)



	def testGetTaxlotInterestIncome2(self):
		d = getTaxlotInterestIncome(
				list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-02.txt')
					))
			)

		# RPCUH 6 08/31/36 REGS
		self.assertAlmostEqual( 11530.44, d['1006824'], 2)
		self.assertAlmostEqual( 19217.39, d['1006825'], 2)
		self.assertAlmostEqual( 19217.39, d['1006826'], 2)
		self.assertAlmostEqual(172956.53, d['1008174'], 2)
		self.assertAlmostEqual( 65339.13, d['1008175'], 2)
		self.assertAlmostEqual( 38434.78, d['1008176'], 2)
		self.assertAlmostEqual(172956.53, d['1008177'], 2)
		self.assertAlmostEqual(3651304.52, d['1021956'], 2)

		# Total interest income of bonds in 2020 Feb
		# Matches exactly with the total interest income from
		# profit loss report.
		self.assertEqual(
			True
		  , all(key in getCNEnergyTaxlots() or d[key] >=0 for key in d)
		)
		self.assertAlmostEqual(755655112.07, sum(d[key] for key in d), 2)



	def testGetTaxlotInterestIncome3(self):
		d = getTaxlotInterestIncome(
				list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-03.txt')
					))
			)

		# BCHINA V3.6 PERP
		self.assertAlmostEqual( 349872.08, d['1115230'], 2)
		self.assertAlmostEqual(  42323.24, d['1115231'], 2)
		self.assertAlmostEqual(1269697.06, d['1115402'], 2)
		self.assertAlmostEqual( 781119.09, d['1115403'], 2)
		self.assertAlmostEqual(  87468.02, d['1115431'], 2)
		self.assertAlmostEqual(7025.19, d['1118798'], 2)
		self.assertAlmostEqual(7025.19, d['1118799'], 2)
		self.assertAlmostEqual(7025.19, d['1118800'], 2)
		self.assertAlmostEqual(7025.19, d['1118801'], 2)
		self.assertAlmostEqual(7025.19, d['1118802'], 2)
		self.assertAlmostEqual(35125.95, d['1118803'], 2)

		# Total interest income of bonds in 2020 Mar
		# It's 808,319,689.00 from profit loss report, here is a
		# difference arround 0.0042%.
		self.assertEqual(
			True
		  , all(key in getCNEnergyTaxlots() or d[key] >=0 for key in d)
		)
		self.assertAlmostEqual(808353818.31, sum(d[key] for key in d), 2)



	def testGetTaxlotInterestIncome4(self):
		d = getTaxlotInterestIncome(
				list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-04.txt')
					))
			)

		# CHIOLI 5.5 11/10/20
		self.assertAlmostEqual( 7141.98, d['1005742'], 2)
		self.assertAlmostEqual(17696.16, d['1005791'], 2)
		self.assertAlmostEqual(88480.79, d['1005793'], 2)

		# Total interest income of bonds in 2020 Apr is 706,267,464.75 
		# from profit loss report. The relative difference should be 
		# less than 0.02%
		self.assertEqual(
			True
		  , all(key in getCNEnergyTaxlots() or d[key] >=0 for key in d)
		)
		self.assertTrue((1 - abs(sum(d[key] for key in d)/706267464.75)) < 0.0002)



	def testGetTaxlotInterestDetail(self):
		d = getTaxlotInterestDetail(
				list(getDailyInterestAccrualDetailPositions(
						join(getCurrentDirectory(), 'samples', 'daily interest 2020-05.txt')
					))
			)

		# US56501RAK23 (MFCCN 2.484 05/19/27)
		self.assertEqual(0, d['1123235'][0])
		self.assertAlmostEqual(5347.57, d['1123235'][1], 2)
		self.assertAlmostEqual(5350.74, d['1123235'][2], 2)



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