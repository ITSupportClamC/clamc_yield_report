# Yield Calculation IMA
For yield calculation IMA method.



## Interest Income of a Tax Lot
In the daily interest accrual detail report, each line is a record of some kind of event. The event types that interest us include:

Event | Condition
------|----------
Interest Accrual to Tax Lot | LotQuantity > 0, LotSumOfChangeInAIBook > 0
Coupon Payment | Textbox84 > 0, LotQuantity = 0, LotSumOfChangeInAIBook > 0
Coupon Received by Tax Lot | Textbox84 > 0, LotQuantity > 0, LotSumOfChangeInAIBook < 0
Sale or Maturity | Textbox84 = 0, LotQuantity = 0, LotSumOfChangeInAIBook > 0
Cash Flow to Tax Lot Due to Sale or Maturity | Textbox84 = 0, LotQuantity = 0, LotSumOfChangeInAIBook < 0

Where,

Column Name | Meaning 
------------|---------
Investment | identity of an investment (typically a bond)
Date | date of an event
LotID | tax lot ID or event ID
Textbox84 | quantity of a position that includes one or more tax lots
LotQuantity | quantity of a tax lot
LotSumOfChangeInAIBook | accrued interest received on the day
LotSumOfEndBalanceBook | ending value of accrued interest on the day

A tax lot is uniquely identified by its tax lot id in an interest accrual event. There could be one or more interest accrual events for a tax lot during a period.

To calculate interest income of a tax lot during a period:

interest income = ending value of accrued interest of the period - starting value of accrued interest of the period + coupon received during the period

Where,

1. Ending value of accrued interest of the period: LotSumOfEndBalanceBook of the tax lot on the last day the tax lot appears in the period when LotQuantity > 0.

2. Starting value of accrued interest of the period: (LotSumOfEndBalanceBook - LotSumOfChangeInAIBook) of a tax lot on the first day the tax lot appears in the period.


### Coupon Received By a Tax Lot
When a bond receives coupon on a day, there will be one or more coupon payment events and one or more coupon received by tax lot events for the bond on that day.

To calculate coupon received by a tax when a bond receives coupon payment, we need to calcualte total amount of coupon received by the bond on that day,

total amount of coupon received = sum of LotSumOfChangeInAIBook of coupon payment events

Where all such coupon payment events should have their Date column the same value and Investment columns the same value.

Then coupon received by each tax lot is the pro-rata share of the total coupon payment according to the tax lot quantity.

Refer to "Calculate tax lot interest income from daily interest accruals.xlsx" in the reference folder for more details.

Note that a bond can receive coupon payments multiple times during a period, so does a tax lot. Therefore, 

coupon received by a tax lot = sum of coupon received by the tax lot from all coupon events during the period.
