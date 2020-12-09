# coding=utf-8
#
# Functions needed to calculate IMA yield
# 



def getDailyInterestAccrualDetailPositions(file):
	"""
	[String] file => [Iterable] posiitons

	Read a daily interest accrual detail report, return each line as a
	position. For each position, the data format is:

	Date: String (yyyy-mm-dd)

	The below fields shoulbe of type Float:

	Textbox84, Textbox85, LotQuantity, LotSumOfChangeInAI, 
	LotSumOfBeginBalanceLocal, LotSumOfChangeAILocal, 
	LotSumOfPurSoldPaidRecLocal, LotSumOfEndAccrualBalanceLocal
	LotSumOfChangeInAIBook, LotSumOfEndBalanceBook

	All other fields should be of type String.
	"""
	# FIXME: add implementation
	return []



def getTaxlotInterestIncome( previousPeriodPositions
						   , currentPeriodPositions):
	"""
	[List] previousPeriodPositions,
	[List] currentPeriodPositions
	=> [Dictionary] ([String] tax lot id -> [Float] interest income)

	From positions from the previous period report (daily interest accrual)
	and the current period report, compute interest income for each tax lot.
	"""
	# FIXME: add implementation
	return {}