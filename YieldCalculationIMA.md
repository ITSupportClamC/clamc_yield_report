# Yield Calculation IMA
For yield calculation IMA method.



## Interest Income of a Tax Lot
In the daily interest accrual details report, each line is a record of two types:

1. The amount of interest accrued by a tax lot on a certain day, if the column LotQuantity has a value > 0. In this case, the column LotID represents the tax lot id.

2. An event that happens on a tax lot, e.g., mature, sell or coupon payment, if the column LotQuantity has a value > 0. In this case, the column LotID represents the tax lot id.

Field Name | Meaning 
-----------|---------
Date | the date
LotID | the tax lot ID
LotQuantity | quantity of the tax lot
LotSumOfChangeInAIBook | accrued interest received by the tax lot on the day
LotSumOfEndBalanceBook | ending value of accrued interest of the tax lot on the day

To calculate interest income of a tax lot during a period:

interest income = ending value of accrued interest of the period - starting value of accrued interest of the period + coupon payment received during the period

Where,

1. Ending value of accrued interest of the period: LotSumOfEndBalanceBook of the tax lot on the last day the tax lot appears in the period when LotQuantity > 0.

2. Starting value of accrued interest of the period: it's either:

	1. LotSumOfEndBalanceBook of the tax lot on the last day of the *previous period* if the tax lot appears on that day, or
	2. (LotSumOfEndBalanceBook - LotSumOfChangeInAIBook) of the tax lot on the first day the tax lot appears in the period.

**previous period** means a period whose end date is just one day before the start date of the current period. For example, if current period is 2020-01-01 to 2020-01-31 (inclusive), then any period whose end date is 2019-12-31 is the previous period.


### Coupon Payment Received By a Tax Lot
A coupon payment event is identified by one or more lines which satisfy the following:

1. value of LotQuantity = 0 and value of LotSumOfChangeInAI > 0;
2. value of Date column and Investment column are the same.

Then the sum of values of LotSumOfChangeInAIBook of those lines is the total value of coupon payment of the event. When such event happens, there will be one or more lines showing tax lots receiving the coupon payment, where the lines will have:

1. the same value of Date column and Investment column as above;
2. value of LotQuantity > 0 and value of LotSumOfChangeInAI < 0.

Then coupon received by each tax lot is the pro-rata share of the total coupon payment according to the tax lot quantity.

Refer to "Calculate tax lot interest income from daily interest accruals.xlsx" in the reference folder for more details.

Note that there could be zero, one or more coupon payments during a period, therefore, coupon received by a tax lot is sum of coupon received by the tax lot from all coupon events during the period.
