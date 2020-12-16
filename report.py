# coding=utf-8
# 
# Read Geneva report and generate output.
#
import os
import sys
import csv
import re
import time
import glob
import logging
import logging.config
import functools
import operator
import collections
from io import StringIO
from datetime import datetime
from itertools import tee
from clamc_yield_report.constants import Constants
from os import listdir
from os.path import isfile, join
from os import walk
from clamc_yield_report.utils import Utils

class Report:

	def __init__(self):
		#=========\add logger from configuration files\=========
		logging.config.fileConfig(join(Utils.get_current_directory(),"logging_config.ini"), 
									defaults={'date':datetime.now().date().strftime('%Y-%m-%d')}
									)
		self.logger = logging.getLogger("sLogger")

	def run(self, input_with_cash, input_cutoff_month, input_impairment, input_last_year_end_nav, upload_dir):
		self.logger.info('Start generating output.csv')
		self.logger.info('Input arguments: ' +
							str(input_with_cash) + " " +
							str(input_cutoff_month) + " " +
							str(input_impairment) + " " +
							str(input_last_year_end_nav) + " " +
							upload_dir
						)
		#-- validate and convert numeric input
		try:
			input_with_cash			= int(input_with_cash)
			input_cutoff_month		= int(input_cutoff_month)
			input_impairment 		= float(input_impairment)
			input_last_year_end_nav	= float(input_last_year_end_nav)
		except ValueError:
			error_message = "Value format of input_with_cash, input_cutoff_month, input_impairment, input_last_year_end_nav are not correct"
			self.logger.error(error_message)
			sys.exit()

		filepaths = [f for f in listdir(upload_dir) if isfile(join(upload_dir, f))]
		numbers = re.compile(r'(\d+)')
		def _numerical_sort(value):
			parts = numbers.split(value)
			parts[1::2] = map(int, parts[1::2])
			return parts

		#-- read filenames from directory, sort them numerically and append them to the "file" iterator
		filepaths = sorted(filepaths, key = _numerical_sort)
		filepaths = [upload_dir + "/" + s for s in filepaths]

		#-- split iterator into 2 for both functions to loop through	
		files = Utils.create_iterator(filepaths)
		#-- duplicate iterator files into 2 for feeding 2 functions below
		files, files2 = tee(files)

		#-- prepare data for exporting the csv file
		accumulate_realized_returns, accumulate_total_returns = self.getAccumulateReturnFromFiles(input_with_cash, files)
		average_NAV = list(self.getAverageNavFromFiles(input_with_cash, 
														input_cutoff_month, 
														input_impairment, 
														input_last_year_end_nav,
														files2))
		accumulate_realized_returns = list(accumulate_realized_returns)
		accumulate_total_returns = list(accumulate_total_returns)
		column_title = ["Month", 
						"Accumulated Realized Return", 
						"Return Rate", 
						"Accumulated Total Return", 
						"Return Rate", 
						"Average Nav"
						]
		
		#-- set up the Scenario field for the csv file 
		with_cash_title = ""
		if (input_with_cash):
			with_cash_title = "withCash"
		else:
			with_cash_title = "withoutCash"

		#-- export data as a csv file
		def outputCSV():
			with open(join(Utils.get_current_directory(), "output_" + with_cash_title + ".csv"), "w", newline="") as file:
				writer = csv.writer(file)
				writer.writerow(column_title)
				for x in range(0, len(average_NAV)):
					single_row_of_data = []
					single_row_of_data.append( (x+1) )
					single_row_of_data.append(accumulate_realized_returns[x])
					single_row_of_data.append(accumulate_realized_returns[x]/average_NAV[x]*100)
					single_row_of_data.append(accumulate_total_returns[x])
					single_row_of_data.append(accumulate_total_returns[x]/average_NAV[x]*100)
					single_row_of_data.append(average_NAV[x])
					writer.writerow(single_row_of_data)
				writer.writerow([" ", " "])
				writer.writerow(["Scenario", with_cash_title])
				writer.writerow(["Last Year End Nav", input_last_year_end_nav])	
				writer.writerow(["Impairment", input_impairment])
				writer.writerow(["Cutoff Month", input_cutoff_month])	

		outputCSV()
		self.logger.info('Generating output.csv completed')
		
	def getPositions(self, filename):
		#-- read file
		try:
			#-- sample files are in utf_16 format (UCS2 LE BOM)
			f = open(filename, 'rU', encoding='utf_16')
		except OSError:
			self.logger.error("Could not open/read file: " + filename)
			return
		
		#-- get the file type
		filetype = Utils.get_file_type(filename)
		#-- if the file is unknown, just skip this file
		if (filetype == Constants.FILETYPE_UNKNOWN):
			self.logger.warn("This file type is unknown: " + filename)
			return

		#-- split file to extract sections
		with f:
			csv_files = f.read()
			#-- sections are separated with single empty line. 
			#-- Handled cases when the empty tab or space
			csv_files = re.split(r'\n\s*\n',csv_files)
			#-- only need to get the 1st and 2nd section only
			csv_file_pos = csv_files[0]
			csv_file_meta = csv_files[1]
			#-- use DictReader to generate the list of position dictionaries
			#-- StringIO is needed to convert the string to file reader
			position_reader = csv.DictReader(StringIO(csv_file_pos), delimiter="\t", quoting=csv.QUOTE_MINIMAL, quotechar='"')
			#-- create a list of dictionary (not iterator)
			list_positions = list(position_reader)
			#-- create meta data dictionary
			meta_data = {}
			meta_data_reader = csv.reader(StringIO(csv_file_meta), delimiter="\t", quoting=csv.QUOTE_MINIMAL, quotechar='"')
			for row in meta_data_reader:
				#-- row[0] - metainfo variable name
				#-- row[1] - metainfo variable value
				meta_data[row[0]] = row[1]
				
		#=====================\format metadata\=======================
		def format_date(old_format):
			date_time_object = datetime.strptime(old_format,'%m/%d/%Y %H:%M')
			new_format = date_time_object.strftime('%Y-%m-%d')
			return new_format
		#-- Convert PeriodEndDate and PeriodStartDate date format from mm/dd/yyyy HH:MM to yyyy-mm-dd
		if "PeriodEndDate" in meta_data:
			meta_data['PeriodEndDate'] = format_date(meta_data['PeriodEndDate'])
		if "PeriodStartDate" in meta_data:
			meta_data['PeriodStartDate'] = format_date(meta_data['PeriodStartDate'])

		#========================\format positions data\==========================
		row_count = 0
		error_flag = 0
		error_rows = ""
		def parseFloatNum(input_column_name, input_position, input_row_count):
			try:
				return float(input_position[input_column_name].replace(',', ''))
			except KeyError:
				error_message = input_column_name + " value missing at row " + str(input_row_count)
				self.logger.error(error_message)
				raise KeyError(error_message)
			except ValueError:
				error_message = input_column_name + " Not a float at row " + str(input_row_count)
				self.logger.error(error_message)
				raise ValueError(error_message)
		def parsePercentageNum(input_column_name, input_position, input_row_count):
			try:
				return float(input_position[input_column_name].replace('%', '')) / 100
			except KeyError:
				error_message = input_column_name + " value missing at row " + str(input_row_count)
				self.logger.error(error_message)
				raise KeyError(error_message)
			except ValueError:
				error_message = input_column_name + " Not a float at row " + str(input_row_count)
				self.logger.error(error_message)
				raise ValueError(error_message)

		for pos in list_positions:
			row_count += 1
			if (filetype == Constants.FILETYPE_INVESTMENT):
				pos['MarketValueBook'] = parseFloatNum("MarketValueBook", pos, row_count)
				pos['Invest'] = parsePercentageNum("Invest", pos, row_count)
				pos['AccruedInterest'] = parseFloatNum("AccruedInterest", pos, row_count)
			elif (filetype == Constants.FILETYPE_PROFIT_LOSS):
				pos['Interest'] = parseFloatNum("Interest", pos, row_count)
				pos['Dividend'] = parseFloatNum("Dividend", pos, row_count)
				pos['OtherIncome'] = parseFloatNum("OtherIncome", pos, row_count)
				pos['RealizedPrice'] = parseFloatNum("RealizedPrice", pos, row_count)
				pos['RealizedFX'] = parseFloatNum("RealizedFX", pos, row_count)
				pos['RealizedCross'] = parseFloatNum("RealizedCross", pos, row_count)
				pos['UnrealizedPrice'] = parseFloatNum("UnrealizedPrice", pos, row_count)
				pos['UnrealizedFX'] = parseFloatNum("UnrealizedFX", pos, row_count)
				pos['UnrealizedCross'] = parseFloatNum("UnrealizedCross", pos, row_count)

		positions = Utils.create_iterator(list_positions)
		if (error_flag):
			error_rows = error_rows[:-2] + ". " + Constants.BG_NORMAL + "\n======================================================"
			self.logger.error(Constants.BG_WARNING + "Invest Not a float. Replace as 0. Row: " + error_rows)

		return meta_data, positions
	#===========================\end of function\===========================

	#===================\getReturnFromPositions function\===================
	def getReturnFromPositions(self, input_with_cash, input_positions):
		#-- initialise monthly totals as 0
		monthly_interest_income = 0
		monthly_realized_return = 0
		monthly_unrealized_gain_loss = 0
		monthly_total_return = 0
		adjustment = [0, 0]
		error_flag = 0
		
		#-- go through the iterator and add up each line of data to monthly total
		for each_position in input_positions:

			#-- calculate interest income
			try:
				each_interest_income = sum([each_position['Interest'], each_position['Dividend'], each_position['OtherIncome']])
				monthly_interest_income += each_interest_income
			except KeyError:
				each_interest_income = 0
				raise KeyError("One or more key(s) not found")
			
			#-- calculate realized return
			try:
				each_realized_return = sum([each_interest_income, each_position['RealizedPrice'], each_position['RealizedFX'], each_position['RealizedCross']])
				monthly_realized_return += each_realized_return
			except KeyError:
				each_realized_return = 0
				raise KeyError("One or more key(s) not found")

			#-- calculate unrealized gain loss
			try:
				each_unrealized_gain_loss = sum([each_position['UnrealizedPrice'], each_position['UnrealizedFX'], each_position['UnrealizedCross']])
				monthly_unrealized_gain_loss += each_unrealized_gain_loss
			except KeyError:
				each_unrealized_gain_loss = 0
				raise KeyError("One or more key(s) not found")
	
			#-- calculate monthly total return
			each_total_return = each_realized_return + each_unrealized_gain_loss
			monthly_total_return += each_total_return

			#-- calculate adjustments basing on "with cash" state
			if input_with_cash:
				if (each_position['PrintGroup'] == "Cash and Equivalents"):					
					adjustment[0] += each_interest_income
					adjustment[1] += each_interest_income
			else:
				if (each_position['PrintGroup'] == "Cash and Equivalents"):
					adjustment[0] += each_realized_return
					adjustment[1] += each_total_return


			#-- calculate adjustments which are the same for both with/ without cash case for CN Energy positions
			if (each_position['PrintGroup'] == "Corporate Bond") and ("CERCG" in each_position['Description']):
				adjustment[0] += each_interest_income
				adjustment[1] += (each_interest_income + each_unrealized_gain_loss)

		#-- apply the adjustments to the calculated realized return & total return
		monthly_realized_return -= adjustment[0]
		monthly_total_return -= adjustment[1]

		#-- log error if any key is missing
		if (error_flag):
			self.logger.error(Constants.BG_WARNING + "Input file's not a profit loss report, one or more key(s) not found: realized return & total return calculation failed, setting values to 0" + Constants.BG_NORMAL)
			raise KeyError("One or more key(s) not found")
		else:
			self.logger.debug(Constants.BG_OKBLUE + "Monthy Realized Return: " + str(monthly_realized_return) + Constants.BG_NORMAL)
			self.logger.debug(Constants.BG_OKBLUE + "Monthy Total Return: " + str(monthly_total_return) + Constants.BG_NORMAL)

		return monthly_realized_return, monthly_total_return
	#===========================\end of function\===========================

	#=====================\getNavFromPositions function\=====================
	def getNavFromPositions(self, input_with_cash, input_cutoff_month, input_impairment, input_meta_data, input_positions):
		#-- validate and convert the input data to float and int
		try:
			input_with_cash			= int(input_with_cash)
			input_cutoff_month		= int(input_cutoff_month)
			input_impairment 		= float(input_impairment)
		except ValueError:
			error_message = "Value format of input_with_cash, input_cutoff_month, input_impairment are not correct"
			self.logger.error(error_message)
			raise ValueError(error_message)	
		#-- month names for debugging & logging (not important for function execution)
		month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
		
		#-- default case as 1
		case = 1
		#-- compare PeriodEndDate from metaData with input cutoff month to determine which case to use
		try:
			period_end_month = datetime.strptime(input_meta_data['PeriodEndDate'], "%Y-%m-%d").month
			if (int(period_end_month) <= int(input_cutoff_month)):
				case = 2
			else:
				case = 1
		except ValueError:
			error_message = "Unable to retrieve PeriodEndDate, case value defaulted to 1"
			self.logger.error(Constants.BG_WARNING + error_message + Constants.BG_NORMAL)
			raise ValueError(error_message)
		#-- initialise monthly NAV & adjustment as 0
		monthly_NAV = 0
		error_flag = 0
		adjustment = 0

		#-- go through the iterator and add up each line of data to monthly NAV
		for each_position in input_positions:
			try:
				monthly_NAV += each_position['AccruedInterest'] + each_position['MarketValueBook']
				# temp += each_position['AccruedInterest'] + each_position['MarketValueBook']
			except KeyError:
				raise KeyError("One or more key(s) not found")
			
			#-- calculate adjustments basing on "with cash" state
			if input_with_cash:
				#-- included AccruedInterest of CN Energy positions in the adjustment for case 1
				if (case == 1):
					if (each_position['SortKey'] == "Corporate Bond") and ("CERCG" in each_position['Description']):
						try:
							adjustment += each_position['AccruedInterest']
						except KeyError:
							adjustment = 0
							raise KeyError("One or more key(s) not found")		
			else:
				#-- AccruedInterest and MarketValueBook of cash positions are included in the adjustment in both cases
				if ( (each_position['SortKey'] == "Cash and Equivalents") and (each_position['LongShortDescription'] == "Cash Long") ):
					try:
						adjustment += each_position['AccruedInterest'] + each_position['MarketValueBook']
					except KeyError:
						adjustment = 0
						raise KeyError("One or more key(s) not found")
				#-- included AccruedInterest of CN Energy positions in the adjustment for case 1	
				if (case == 1):
					if (each_position['SortKey'] == "Corporate Bond") and ("CERCG" in each_position['Description']):
						try:
							adjustment += each_position['AccruedInterest']
						except KeyError:
							adjustment = 0
							raise KeyError("One or more key(s) not found")
		
		#-- impairment is included in the adjustment for both with/ without cash state and for both case 1 & 2 so we'll add it at the end here
		adjustment += input_impairment
		#-- apply the adjustments to the calculated monthly NAV
		monthly_NAV -= adjustment
		#-- log error & set monthly NAV to be 0 if any key is missing
		if (error_flag):
			monthly_NAV = 0
			self.logger.error(Constants.BG_WARNING + "Input file's not an investment positions file, one or more key(s) not found: NAV calculation failed, setting value to 0" + Constants.BG_NORMAL)
		else:
			self.logger.debug(Constants.BG_OKBLUE + "Period end month: " + str(period_end_month) + Constants.BG_OKGREEN + "(" + month_names[period_end_month-1] + ")" + Constants.BG_NORMAL)
			self.logger.debug(Constants.BG_OKBLUE + "Monthy NAV for " + Constants.BG_OKGREEN + month_names[period_end_month-1] + Constants.BG_OKBLUE + ": " + str(monthly_NAV) + Constants.BG_NORMAL)
			self.logger.debug(Constants.BG_OKBLUE + "Case: " + str(case) + Constants.BG_NORMAL)
		
		return monthly_NAV
	#===========================\end of function\===========================

	def getAccumulateReturnFromFiles(self, input_with_cash, input_files):
		#-- initialise empty list for accumulate realized returns & accumulate total returns as 0
		accumulate_realized_returns_list = []
		accumulate_total_returns_list = [] 

		#-- initialise final accumulate realized returns & final accumulate total returns as 0
		total_accumulate_realized_returns = 0
		total_accumulate_total_returns = 0

		#-- go through each file
		for each_file in input_files:
			#-- check if file is a "profit and loss" file exactly
			if (Utils.get_file_type(each_file) == Constants.FILETYPE_PROFIT_LOSS):
				#-- log the current working file
				self.logger.debug(Constants.BG_OKBLUE + "Retrieved file: " + Constants.BG_OKGREEN + str(each_file) + Constants.BG_NORMAL)

				#-- get metaData, positions, mouthly realized returns & monthly total returns with previous functions
				metaData, positions = self.getPositions(each_file)
				each_realized_returns, each_total_returns = self.getReturnFromPositions(input_with_cash, positions)
				
				#-- add the current returns to the accumulated values
				total_accumulate_realized_returns += each_realized_returns
				total_accumulate_total_returns += each_total_returns

				#-- append the current accumulated values until this month to the lists
				accumulate_realized_returns_list.append(total_accumulate_realized_returns)
				accumulate_total_returns_list.append(total_accumulate_total_returns)
			else:	
				#-- file is "investment positions" file, operation abort
				self.logger.debug(Constants.BG_WARNING + "Skip as not 'profit loss' files: " + each_file + Constants.BG_NORMAL)	

		#-- log the resulted lists
		self.logger.debug(Constants.BG_OKBLUE + "Accumulate Realized Returns monthly iterated: " + str(accumulate_realized_returns_list) + Constants.BG_NORMAL)
		self.logger.debug(Constants.BG_OKBLUE + "Accumulate Total Returns monthly iterated: " + str(accumulate_total_returns_list) + Constants.BG_NORMAL)

		#-- return the results
		accumulate_realized_returns = Utils.create_iterator(accumulate_realized_returns_list)
		accumulate_total_returns = Utils.create_iterator(accumulate_total_returns_list)
		return accumulate_realized_returns, accumulate_total_returns

	def getAverageNavFromFiles(self, input_with_cash, input_cutoff_month, input_impairment, input_last_year_end_nav, input_files):
		#-- validate and convert the input data to float and int
		try:
			input_with_cash			= int(input_with_cash)
			input_cutoff_month		= int(input_cutoff_month)
			input_impairment 		= float(input_impairment)
			input_last_year_end_nav	= float(input_last_year_end_nav)
		except ValueError:
			error_message = "Value format of input_with_cash, input_cutoff_month, input_impairment, input_last_year_end_nav are not correct"
			self.logger.error(error_message)
			raise ValueError(error_message)
		#-- initialise accumulate NAV as the previous year end's NAV
		accumulate_NAV = input_last_year_end_nav
		#-- initialise empty list for accumulate realized returns & accumulate total returns as 0
		accumulate_NAV_list = []
		total_month = 2

		#-- go through each file
		for each_file in input_files:
			#-- check if file is an "investment positions" file exactly
			if (Utils.get_file_type(each_file) == Constants.FILETYPE_INVESTMENT):
			#-- get metaData, positions & mouthly nav with previous functions
				metaData, positions = self.getPositions(each_file)
				mouthly_NAV = self.getNavFromPositions(input_with_cash, input_cutoff_month, input_impairment, metaData, positions)
				
				#-- add the mouthly NAV to the accumulate NAV
				accumulate_NAV += mouthly_NAV

				#-- calculate this month's average NAV and append it to the average NAV list
				avg_NAV = accumulate_NAV/total_month
				accumulate_NAV_list.append(avg_NAV)

				#-- add 1 to the total number of months calculated
				total_month += 1
			else:	
				#-- file is "profit loss" file, operation abort
				self.logger.debug(Constants.BG_WARNING + "Skip as not 'investment positions' files: " + each_file + Constants.BG_NORMAL)
					
		#-- log the resulted lists
		self.logger.debug(Constants.BG_OKBLUE + "Averge NAV monthly iterated: " + str(accumulate_NAV_list) + Constants.BG_NORMAL)
		
		#-- return the result
		NAV = Utils.create_iterator(accumulate_NAV_list)
		return NAV

	#-- return and indicate if the file is one of the following
	#-- 	1: investment position
	#--		2: profit loss
	# def _get_file_type(self, input_filepath):
	# 	head, filename = os.path.split(input_filepath)
	# 	if (Constants.FILENAME_INVESTMENT_POSITION in filename.lower()):
	# 		return Constants.FILETYPE_INVESTMENT
	# 	elif (Constants.FILENAME_PROFIT_LOSS in filename.lower()):
	# 		return Constants.FILETYPE_PROFIT_LOSS
	# 	else:
	# 		return Constants.FILETYPE_UNKNOWN

	#-- function for constucting iterator
	# def _create_iterator(self, input_list):
	# 	for item in input_list:
	# 		yield item