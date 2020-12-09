# Yield Calculation IMA
For yield calculation IMA method.



## Interest Income of a Tax Lot
To calculate interest income per tax lot, we need two inputs:

1. daily interest accrual details report during a period (*current period report*);

2. daily interest accrual details report with a period end date just one day before the start date of the current period report (*previous period report*).

interest income of a tax lot = accrued interest at current period report - accrued interest at previous period report + coupon payment at current period report


### Accrued Interest
Accrued interest is shown in the LotSumOfEndBalanceBook column of a daily interest accrual details report. The accrued interest of a tax lot during a period is the accrued interest of the tax lot on the last day the tax lot appears during that period.

For example, a tax lot appears like this in the report

Day | LotSumOfEndBalanceBook
----|-----------------------
d1 | v1
d2 | v2
...
d_N | v_N
... does not appear any more in the remaining days ... |

Then accrued interest of the tax lot is v_N.

If the tax lot does not appear in a report during a period, then accued interest is 0 for that period.


### Coupon Payment
Coupon payment of a tax lot during a period = sum of coupon received by the tax lot during the period

A bond can receive zero or more coupon payments during a period, similar for a tax lot. When a coupon payment happens, there will be one or more lines with column LotQuantity = 0 in the daily interest accrual details report, with LotSumOfChangeInAIBook column as the book amount of the coupon payment.

Refer to Calculate tax lot interest income from daily interest accruals.xlsx for more details.
