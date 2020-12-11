# Yield Calculation IMA
For yield calculation IMA method.



## Interest Income of a Tax Lot
In the daily interest accrual detail report, each line is a record of two kinds,

Record Type | Condition | Meaning
------------|-----------|--------
Tax Lot Interest Accrual Status | LotSumOfPurSoldPaidRecLocal = 0 | status of interest accrued to a tax lot on a day
Interest Payment Event | LotSumOfPurSoldPaidRecLocal > 0 | interest payment due to bond maturity or sale of tax lot(s)

Where,

Column Name | Meaning 
------------|---------
Investment | identity of an investment to which a tax lot belongs or an interest payment event applies
Date | date of a record
LotID | tax lot ID or event ID
Textbox84 | quantity of a position that includes one or more tax lots on a day
LotQuantity | quantity of a tax lot, if the record is an interest payment event, LotQuantity is always 0
LotSumOfChangeInAIBook | accrued interest received on the day
LotSumOfEndBalanceBook | ending value of accrued interest on the day

A tax lot is uniquely identified by its tax lot id. There could be one or more interest accrual events for a tax lot during a period.

Interest income of a tax lot during a period is calculated as:

interest income = ending value of accrued interest of the period - starting value of accrued interest of the period + interest received during the period

Where,

1. Ending value of accrued interest of the period: LotSumOfEndBalanceBook of the tax lot on the last day the tax lot appears in the period when LotQuantity > 0.

2. Starting value of accrued interest of the period: (LotSumOfEndBalanceBook - LotSumOfChangeInAIBook) of a tax lot interest accrual status record on the day the tax lot appears the first time in the period.


### Interest Received By a Tax Lot
When an interest payment event occurs, one or more tax lots could receive interest. This is usually due to: 

1. A bond matures or is called;
2. A bond pays coupon;
3. A bond position (the whole or a part of) is sold.

When the above happens, say it's on day D0 and for bond BB, there will be one or more interest payment events which satisfy:

1. Date = D0;
2. Investment = BB.

then we have:

total amount of interest received = sum of LotSumOfChangeInAIBook of such interest payment events

Then coupon received by a tax lot of bond BB on day D0 is the pro-rata share of the total amount of interest received based on its tax lot quantity.

Refer to "Calculate tax lot interest income from daily interest accruals.xlsx" in the reference folder for more details.

Note that a bond can have interest payment events on multiple days during a period, so does a tax lot. Therefore, 

interest received by a tax lot = sum of interest received by the tax lot from all such events during the period.
