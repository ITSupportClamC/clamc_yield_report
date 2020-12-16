import sys
import os
from clamc_yield_report.report import Report
from clamc_yield_report.ima import ReportIMA

def main():
    # print command line arguments
    if len(sys.argv) > 1:
        report_type                 = sys.argv[1]
        if report_type == 'report':
            if len(sys.argv) > 6:
                with_cash           = sys.argv[2]
                input_cutoff_month  = sys.argv[3]
                impairment          = sys.argv[4]
                last_year_end_nav   = sys.argv[5]
                upload_dir          = sys.argv[6]
                Report().run(with_cash, input_cutoff_month, impairment, last_year_end_nav, upload_dir)
            else:
                print("Insufficient argument")
                print_menu()
        elif report_type == 'ima':
            if (len(sys.argv) > 2):
                filename            = sys.argv[2]
                ReportIMA().run(filename)
            else:
                print("Insufficient argument")
                print_menu()
        else:
            print("Unknown report type:" + report_type)
    else:
        print_menu()

def print_menu():
    print("To run Report                : python -m clamc_yield_report report <with_cash> <input_cutoff_month> <impairment> <last_year_end_nav> <upload_dir>")
    print("Sample Input (withcash)      : python -m clamc_yield_report report 1 7 3212689500 177801674041.66 \"clamc_yield_report\\samples\"")
    print("Sample Input (without cash)  : python -m clamc_yield_report report 0 7 3212689500 177800934590.2 \"clamc_yield_report\\samples\"")
    print("To run unit Test             : python -m unittest2 \"clamc_yield_report\\tests\\test_report.py\"")
    print("")
    print("To run IMA Report            : python -m clamc_yield_report ima <filename>")
    print("Sample Input (2020-01)       : python -m clamc_yield_report ima \"clamc_yield_report\\samples\\daily interest 2020-01.txt\"")
    print("To run unit Test             : python -m unittest2 \"clamc_yield_report\\tests\\test_ima_steven.py\"")

if __name__ == "__main__":
    main()