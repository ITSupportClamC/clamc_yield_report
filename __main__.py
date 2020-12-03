import sys
import os
from report import Report

def main():
    # print command line arguments
    if len(sys.argv) > 5:
        with_cash           = sys.argv[1]
        input_cutoff_month  = sys.argv[2]
        impairment          = sys.argv[3]
        last_year_end_nav   = sys.argv[4]
        upload_dir          = sys.argv[5]
		#-- current impairment retrieved from excel "CLO bond yield withCash .csv"
		#impairment = 3212689500
		#with_cash = 1
		#input_cutoff_month = 7
		#last_year_end_nav = 177801674041.66
        Report().run(with_cash, input_cutoff_month, impairment, last_year_end_nav, upload_dir)
    else:
        print("To run program               : python __main__.py <with_cash> <input_cutoff_month> <impairment> <last_year_end_nav> <upload_dir>")
        print("Sample Input (withcash)      : python __main__.py 1 7 3212689500 177801674041.66 samples")
        print("Sample Input (without cash)  : python __main__.py 0 7 3212689500 177800934590.2 samples")
        print("To run unit Test             : python -m unittest2")

if __name__ == "__main__":
    main()