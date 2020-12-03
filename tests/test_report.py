# coding=utf-8
# 
# Production data test comes here
import unittest2
import os
from report import Report

class TestReport(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestReport, self).__init__(*args, **kwargs)
    
    def setUp(self):
        self.report = Report()

    def test_getpositions_1linedata(self):
        #-- the path is relative to the report.py
        meta_data, positions = self.report.getPositions("tests/testdata/investment positions_1linedata.txt")
        #-- check the first line value
        row_count=0
        for pos in positions:
            row_count+=1
            if row_count == 1:
                self.assertEqual(pos['ReportMode'], 'Investments', 'line 1 ReportMode wrong. Value received:' + pos['ReportMode'])
                self.assertEqual(pos['MarketValueBook'], 3749.25, 'line 1 MarketValueBook wrong. Value received:' + str(pos['MarketValueBook']))
                self.assertAlmostEqual(pos['Invest'], 0, 7, 'line 1 Invest wrong: ' + str(pos['Invest']))

        #-- assert meta_data
        self.assertEqual(meta_data['AccountingCalendar'], '12229_AccountingCalendar', 'AccountingCalendar wrong! ' + meta_data['AccountingCalendar'])
        self.assertEqual(meta_data['WithholdPurchasedSoldAI'], '0', 'WithholdPurchasedSoldAI wrong! ' + meta_data['WithholdPurchasedSoldAI'])
        self.assertEqual(meta_data['PeriodEndDate'], '2020-01-31', 'PeriodEndDate wrong! ' + meta_data['PeriodEndDate'])
        self.assertEqual(meta_data['PeriodStartDate'], '2020-01-01', 'PeriodStartDate wrong! ' + meta_data['PeriodEndDate'])

    def test_getpositions_2linedata(self):
        #-- the path is relative to the report.py
        meta_data, positions = self.report.getPositions("tests/testdata/investment positions_2linedata.txt")
        # testcase of the unit test
        row_count=0
        for pos in positions:
            row_count+=1
            if row_count == 1:
                self.assertEqual(pos['ReportMode'], 'Investments', 'line 1 ReportMode wrong. Value received:' + pos['ReportMode'])
                self.assertEqual(pos['MarketValueBook'], 3749.25, 'line 1 MarketValueBook wrong. Value received:' + str(pos['MarketValueBook']))
                self.assertAlmostEqual(pos['Invest'], 0, 7, 'line 1 Invest wrong: ' + str(pos['Invest']))
            if row_count == 2:
                self.assertEqual(pos['ReportMode'], 'Receivable Investments', 'Last line ReportMode wrong ' + pos['ReportMode'])
                self.assertEqual(pos['MarketValueBook'], -37418217.94, 'Last line MarketValueBook wrong. Value received:' + str(pos['MarketValueBook']))
                self.assertAlmostEqual(pos['Invest'], 0.5277, 7, 'Last line Invest wrong ' + str(pos['Invest']))
        #-- assert meta_data
        self.assertEqual(meta_data['AccountingCalendar'], '12229_AccountingCalendar', 'AccountingCalendar wrong! ' + meta_data['AccountingCalendar'])
        self.assertEqual(meta_data['WithholdPurchasedSoldAI'], '0', 'WithholdPurchasedSoldAI wrong! ' + meta_data['WithholdPurchasedSoldAI'])
        self.assertEqual(meta_data['PeriodEndDate'], '2020-01-31', 'PeriodEndDate wrong! ' + meta_data['PeriodEndDate'])
        self.assertEqual(meta_data['PeriodStartDate'], '2020-01-01', 'PeriodStartDate wrong! ' + meta_data['PeriodEndDate'])

    def test_getpositions_emptypos(self):
        #-- the path is relative to the report.py
        meta_data, positions = self.report.getPositions("tests/testdata/investment positions_emptypos.txt")
        try:
            next(positions)
        except StopIteration:
            pass  # This is what should happen
        else:
            self.fail("Expected positions to be empty")

        self.assertEqual(meta_data['AccountingCalendar'], '12229_AccountingCalendar', 'AccountingCalendar wrong! ' + meta_data['AccountingCalendar'])
        self.assertEqual(meta_data['WithholdPurchasedSoldAI'], '0', 'WithholdPurchasedSoldAI wrong! ' + meta_data['WithholdPurchasedSoldAI'])
        self.assertEqual(meta_data['PeriodEndDate'], '2020-01-31', 'PeriodEndDate wrong! ' + meta_data['PeriodEndDate'])
        self.assertEqual(meta_data['PeriodStartDate'], '2020-01-01', 'PeriodStartDate wrong! ' + meta_data['PeriodEndDate'])

    def test_getpositions_missingcol(self):
        #-- the path is relative to the report.py
        try:
            self.report.getPositions("tests/testdata/investment positions_missingcol.txt")
        except KeyError:
            pass  # This is what should happen
        else:
            self.fail("Expected missing MarketValueBook column")

    def test_getpositions_normal(self):
        #-- the path is relative to the report.py
        meta_data, positions = self.report.getPositions("tests/testdata/investment positions_normal.txt")
        # testcase of the unit test
        row_count=0
        for pos in positions:
            row_count+=1
            if row_count == 1:
                self.assertEqual(pos['ReportMode'], 'Investments', 'line 1 ReportMode wrong. Value received:' + pos['ReportMode'])
                self.assertEqual(pos['MarketValueBook'], 11255.49, 'line 1 MarketValueBook wrong. Value received:' + str(pos['MarketValueBook']))
                self.assertAlmostEqual(pos['Invest'], 0, 7, 'line 1 Invest wrong: ' + str(pos['Invest']))
            if row_count == 2:
                self.assertEqual(pos['ReportMode'], 'Investments', 'Last line ReportMode wrong ' + pos['ReportMode'])
                self.assertEqual(pos['MarketValueBook'], 202562599.37, 'Last line MarketValueBook wrong. Value received:' + str(pos['MarketValueBook']))
                self.assertAlmostEqual(pos['Invest'], 0.001, 7, 'Last line Invest wrong ' + str(pos['Invest']))
        #test the last row
        self.assertEqual(pos['ReportMode'], 'Investments', 'Last line ReportMode wrong ' + pos['ReportMode'])
        self.assertEqual(pos['MarketValueBook'], 17861291.29, 'Last line MarketValueBook wrong. Value received:' + str(pos['MarketValueBook']))
        self.assertAlmostEqual(pos['Invest'], 0.0001, 7, 'Last line Invest wrong ' + str(pos['Invest']))

        self.assertEqual(meta_data['AccountingCalendar'], '12229_AccountingCalendar', 'AccountingCalendar wrong! ' + meta_data['AccountingCalendar'])
        self.assertEqual(meta_data['WithholdPurchasedSoldAI'], '0', 'WithholdPurchasedSoldAI wrong! ' + meta_data['WithholdPurchasedSoldAI'])
        self.assertEqual(meta_data['PeriodEndDate'], '2020-10-31', 'PeriodEndDate wrong! ' + meta_data['PeriodEndDate'])
        self.assertEqual(meta_data['PeriodStartDate'], '2020-10-01', 'PeriodStartDate wrong! ' + meta_data['PeriodEndDate'])

    def test_getReturnFromPositions_normal(self):
        #-- test withcash 8 months data
        mon_realized_return_withcash_expects = [
            794354025.64,
            743848071.6,
            790720702.3,
            1069928303,
            820873440.3,
            825677290,
            910273720.8,
            834768238.2
        ]

        month_count = 0
        for mon_realized_return_withcash_expect in mon_realized_return_withcash_expects:
            month_count += 1
            meta_data, positions = self.report.getPositions("tests/testdata/profit loss 2020-0" + str(month_count) +".txt")
            monthly_realized_return, monthly_total_return = self.report.getReturnFromPositions(True, positions)
            self.assertAlmostEqual(monthly_realized_return, 
                                    mon_realized_return_withcash_expect, 
                                    0, 
                                    "with cash 2020-0" + str(month_count) +" monthly_realized_return wrong. Value received:" + str(monthly_realized_return))

        mon_total_return_withcash_expects = [
            467300058.6,
            1305367116,
            -292801202.4,
            1289771356,
            645117919.5,
            808487471,
            975551797.1,
            893933279.8
        ]

        month_count = 0
        for mon_total_return_withcash_expect in mon_total_return_withcash_expects:
            month_count += 1
            meta_data, positions = self.report.getPositions("tests/testdata/profit loss 2020-0" + str(month_count) +".txt")
            monthly_realized_return, monthly_total_return = self.report.getReturnFromPositions(True, positions)
            self.assertAlmostEqual(monthly_total_return, 
                                    mon_total_return_withcash_expect, 
                                    0, 
                                    "with cash 2020-0" + str(month_count) +" monthly_total_return wrong. Value received:" + str(monthly_total_return))

       #-- test without cash 8 months data
        mon_realized_return_withoutcash_expects = [
            795081909.54,
            743454341.2,
            786564833.1,
            1071090784,
            819777517.3,
            825577306.3,
            910888436.8,
            835110810.4,
        ]

        month_count = 0
        for mon_realized_return_withoutcash_expect in mon_realized_return_withoutcash_expects:
            month_count += 1
            meta_data, positions = self.report.getPositions("tests/testdata/profit loss 2020-0" + str(month_count) +".txt")
            monthly_realized_return, monthly_total_return = self.report.getReturnFromPositions(False, positions)
            self.assertAlmostEqual(monthly_realized_return, 
                                    mon_realized_return_withoutcash_expect, 
                                    0, 
                                    "2020-0" + str(month_count) +" without cash monthly_realized_return wrong. Value received:" + str(monthly_realized_return))

        mon_total_return_withoutcash_expects = [
            468008054.9,
            1305050625,
            -296805557.3,
            1289488201,
            645290337.3,
            808359754.1,
            976508916.4,
            893939456
        ]

        month_count = 0
        for mon_total_return_withoutcash_expect in mon_total_return_withoutcash_expects:
            month_count += 1
            meta_data, positions = self.report.getPositions("tests/testdata/profit loss 2020-0" + str(month_count) +".txt")
            monthly_realized_return, monthly_total_return = self.report.getReturnFromPositions(False, positions)
            self.assertAlmostEqual(monthly_total_return, 
                                    mon_total_return_withoutcash_expect, 
                                    0, 
                                    "2020-0" + str(month_count) +" without cash monthly_total_return wrong. Value received:" + str(monthly_total_return))

    def test_getNavFromPositions_normal(self):
        
         #-- verify avg nav with cash
        last_year_end_nav = 177801674041.66
        acc_navs = [last_year_end_nav]
        impairment = 3212689500
        cutoff_month = 7

        #-- test 8 months data
        acc_nav_withcash_expects = [
            178862489321.83,
            179654509989.67,
            181706314938.85,
            183256791748.77,
            184887150491.03,
            186512145974.12,
            187949907557.90,
            189426010312.31
        ]

        #-- verify  2020-01 avg nav with cash
        month_count = 0
        for acc_nav_expect in acc_nav_withcash_expects:
            month_count += 1
            meta_data, positions = self.report.getPositions("tests/testdata/investment positions 2020-0" + str(month_count) +".txt")
            nav = self.report.getNavFromPositions(True, cutoff_month, impairment, meta_data, positions)
            acc_navs.append(nav)
            avg_nav = sum(acc_navs) / len(acc_navs)
            self.assertAlmostEqual(avg_nav, acc_nav_expect, 0, "2020-0" + str(month_count) +" with cash avg nav wrong. Value received:" + str(avg_nav))

        #-- verify avg nav without cash
        last_year_end_nav = 177800934590.20
        acc_navs = [last_year_end_nav]
        impairment = 3212689500
        cutoff_month = 7

        acc_nav_withoutcash_expects = [
            178202412228.44,
            179053923336.87,
            180651954607.04,
            182129154073.73,
            183498189848.02,
            185009441602.27,
            186264602699.66,
            187879692204.51
        ]

        month_count = 0
        for acc_nav_expect in acc_nav_withoutcash_expects:
            month_count += 1
            meta_data, positions = self.report.getPositions("tests/testdata/investment positions 2020-0" + str(month_count) +".txt")
            nav = self.report.getNavFromPositions(False, cutoff_month, impairment, meta_data, positions)
            acc_navs.append(nav)
            avg_nav = sum(acc_navs) / len(acc_navs)
            self.assertAlmostEqual(avg_nav, acc_nav_expect, 0, "2020-0" + str(month_count) +" without cash avg nav wrong. Value received:" + str(avg_nav))


    def test_getAccumulateReturnFromFiles_normal(self):
        # filepaths = os.listdir("tests/testdata")
        filepaths = [
            'tests/testdata/profit loss 2020-01.txt',
            'tests/testdata/profit loss 2020-02.txt',
            'tests/testdata/profit loss 2020-03.txt',
            'tests/testdata/profit loss 2020-04.txt',
            'tests/testdata/profit loss 2020-05.txt',
            'tests/testdata/profit loss 2020-06.txt',
            'tests/testdata/profit loss 2020-07.txt',
            'tests/testdata/profit loss 2020-08.txt'
        ]
        input_files = self._get_file_iterator(filepaths)

        #-- test withcash 8 months data
        accumulate_realized_returns, accumulate_total_returns = self.report.getAccumulateReturnFromFiles(True, input_files)
        accumulate_realized_return_withcash_expects = [
            794354025.64,
            1538202097.25,
            2328922799.56,
            3398851102.73,
            4219724543.05,
            5045401833.09,
            5955675553.84,
            6790443792.02
        ]
    
        accumulate_total_return_withcash_expects = [
            467300058.6,
            1772667174,
            1479865972,
            2769637328,
            3414755247,
            4223242718,
            5198794515,
            6092727795
        ]

        month_count = 0
        for accumulate_realized_return in accumulate_realized_returns:
            month_count += 1
            self.assertAlmostEqual(accumulate_realized_return, 
                                    accumulate_realized_return_withcash_expects[month_count-1], 
                                    0, 
                                    '2020-0' + str(month_count) + ' with cash accumulate_realized_return wrong. Value received:' + str(accumulate_realized_return))

        month_count = 0
        for accumulate_total_return in accumulate_total_returns:
            month_count += 1
            self.assertAlmostEqual(accumulate_total_return, 
                                    accumulate_total_return_withcash_expects[month_count-1], 
                                    0, 
                                    '2020-0' + str(month_count) + ' with cash accumulate_realized_return wrong. Value received:' + str(accumulate_total_return))

        accumulate_realized_returns, accumulate_total_returns = self.report.getAccumulateReturnFromFiles(True, input_files)
    
        #-- test without cash 8 months data
        accumulate_realized_return_withoutcash_expects = [
            795081909.54,
            1538536250.69,
            2325101083.79,
            3396191868.07,
            4215969385.33,
            5041546691.66,
            5952435128.42,
            6787545938.78
        ]
    
        accumulate_total_return_withoutcash_expects = [
            468008054.9,
            1773058680,
            1476253122,
            2765741323,
            3411031660,
            4219391414,
            5195900331,
            6089839787
        ]

        month_count = 0
        for accumulate_realized_return in accumulate_realized_returns:
            month_count += 1
            self.assertAlmostEqual(accumulate_realized_return, 
                                    accumulate_realized_return_withoutcash_expects[month_count-1], 
                                    0, 
                                    '2020-0' + str(month_count) + ' without cash accumulate_realized_return wrong. Value received:' + str(accumulate_realized_return))

        month_count = 0
        for accumulate_total_return in accumulate_total_returns:
            month_count += 1
            self.assertAlmostEqual(accumulate_total_return, 
                                    accumulate_total_return_withoutcash_expects[month_count-1], 
                                    0, 
                                    '2020-0' + str(month_count) + ' without cash accumulate_realized_return wrong. Value received:' + str(accumulate_total_return))

        
    def test_getAverageNavFromFiles_normal(self):
        
         #-- verify avg nav with cash
        last_year_end_nav = 177801674041.66
        impairment = 3212689500
        cutoff_month = 7
        filepaths = [
            'tests/testdata/investment positions 2020-01.txt',
            'tests/testdata/investment positions 2020-02.txt',
            'tests/testdata/investment positions 2020-03.txt',
            'tests/testdata/investment positions 2020-04.txt',
            'tests/testdata/investment positions 2020-05.txt',
            'tests/testdata/investment positions 2020-06.txt',
            'tests/testdata/investment positions 2020-07.txt',
            'tests/testdata/investment positions 2020-08.txt'
        ]
        input_files = self._get_file_iterator(filepaths)

        #-- test 8 months data
        avg_nav_withcash_expects = [
            178862489321.83,
            179654509989.67,
            181706314938.85,
            183256791748.77,
            184887150491.03,
            186512145974.12,
            187949907557.90,
            189426010312.31
        ]

        avg_navs = self.report.getAverageNavFromFiles(True, cutoff_month, impairment, last_year_end_nav, input_files)

        month_count = 0
        for avg_nav in avg_navs:
            month_count += 1
            self.assertAlmostEqual(avg_nav, 
                                    avg_nav_withcash_expects[month_count-1], 
                                    0, 
                                    '2020-0' + str(month_count) + ' with cash avg_navs wrong. Value received:' + str(avg_navs))
        
        #-- verify avg nav without cash
        last_year_end_nav = 177800934590.20
        impairment = 3212689500
        cutoff_month = 7
        filepaths = [
            'tests/testdata/investment positions 2020-01.txt',
            'tests/testdata/investment positions 2020-02.txt',
            'tests/testdata/investment positions 2020-03.txt',
            'tests/testdata/investment positions 2020-04.txt',
            'tests/testdata/investment positions 2020-05.txt',
            'tests/testdata/investment positions 2020-06.txt',
            'tests/testdata/investment positions 2020-07.txt',
            'tests/testdata/investment positions 2020-08.txt'
        ]
        input_files = self._get_file_iterator(filepaths)

        #-- test 8 months data
        avg_nav_withcash_expects = [
            178202412228.44,
            179053923336.87,
            180651954607.04,
            182129154073.73,
            183498189848.02,
            185009441602.27,
            186264602699.66,
            187879692204.51
        ]

        avg_navs = self.report.getAverageNavFromFiles(False, cutoff_month, impairment, last_year_end_nav, input_files)

        month_count = 0
        for avg_nav in avg_navs:
            month_count += 1
            self.assertAlmostEqual(avg_nav, 
                                    avg_nav_withcash_expects[month_count-1], 
                                    0, 
                                    '2020-0' + str(month_count) + ' without cash avg_navs wrong. Value received:' + str(avg_navs))

    def _get_file_iterator(self, input_file_list):
        for input_file in input_file_list:
            yield input_file