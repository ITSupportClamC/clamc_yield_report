# coding=utf-8
#
# Functions needed to calculate IMA yield
# 
import csv
import re
import logging
import logging.config
import os
from constants import Constants
from datetime import datetime
from io import StringIO
from os.path import abspath, dirname
from utils import Utils

#-- These 3 functions  for running the test case provided
getCurrentDirectory = lambda : \
	dirname(abspath(__file__))

def getDailyInterestAccrualDetailPositions(file):
	return ReportIMA().getDailyInterestAccrualDetailPositions(file)

def getTaxlotInterestIncome(positions):
	return ReportIMA().getTaxlotInterestIncome(positions)

class ReportIMA:

	def __init__(self):
		#=========\add logger from configuration files\=========
		logging.config.fileConfig("logging_config.ini", defaults={'date':datetime.now().date().strftime('%Y-%m-%d')})
		self.logger = logging.getLogger("sLogger")	

	def run(self, filename):
		self.logger.info('Input filename: ' + filename)
		#-- validate and convert numeric input
		d = self.getTaxlotInterestIncome(list(self.getDailyInterestAccrualDetailPositions(filename)))
		total_interest = sum(d[key] for key in d)
		self.logger.info('The total Interest Income from the file is: ' + str(total_interest))

	def getCurrentDirectory(self):
		return dirname(abspath(__file__))

	def getDailyInterestAccrualDetailPositions(self, file):
		"""
		[String] file => [Iterable] positions

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
		#-- read file
		try:
			#-- sample files are in utf_16 format (UCS2 LE BOM)
			f = open(file, 'rU', encoding='utf_16')
		except OSError:
			self.logger.error("Could not open/read file: " + file)
			return
		
		#-- get the file type
		filetype = Utils.get_file_type(file)
		#-- if the file is unknown, just skip this file
		if (filetype != Constants.FILENAME_DAILY_INTEREST):
			self.logger.warn("This file type is not daily interest: " + file)
			return

		#-- split file to extract sections
		with f:
			csv_files = f.read()
			#-- sections are separated with single empty line. 
			#-- Handled cases when the empty tab or space
			csv_files = re.split(r'\n\s*\n',csv_files)
			#-- only need to get the 1st and 2nd section only
			csv_file_pos = csv_files[0]
			#-- use DictReader to generate the list of position dictionaries
			#-- StringIO is needed to convert the string to file reader
			position_reader = csv.DictReader(StringIO(csv_file_pos), delimiter="\t", quoting=csv.QUOTE_MINIMAL, quotechar='"')
			#-- create a list of dictionary (not iterator)
			list_positions = list(position_reader)
				
		#-- convert date field format from mm/dd/yyyy to yyyy-mm-dd or throw exception
		def format_date(input_column_name, input_position, input_row_count):
			try:
				date_time_object = datetime.strptime(input_position['Date'],'%m/%d/%Y')
				new_format = date_time_object.strftime('%Y-%m-%d')
				return new_format
			except KeyError:
				error_message = input_column_name + " value missing at row " + str(input_row_count)
				self.logger.error(error_message)
				raise KeyError(error_message)
			except ValueError:
				error_message = input_column_name + " Not a float at row " + str(input_row_count)
				self.logger.error(error_message)
				raise ValueError(error_message)
		
		row_count = 0
		for pos in list_positions:
			row_count += 1
			pos['Date'] = format_date('Date', pos, row_count)

		#-- format to float value or throw exception
		def parse_float_num(input_column_name, input_position, input_row_count):
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

		#-- format Textbox84, Textbox85, LotQuantity, LotSumOfChangeInAI, 
		#-- LotSumOfBeginBalanceLocal, LotSumOfChangeAILocal, 
		#-- LotSumOfPurSoldPaidRecLocal, LotSumOfEndAccrualBalanceLocal
		#-- LotSumOfChangeInAIBook, LotSumOfEndBalanceBook to float value
		row_count = 0
		for pos in list_positions:
			row_count += 1
			pos['Textbox84'] = parse_float_num("Textbox84", pos, row_count)
			pos['Textbox85'] = parse_float_num("Textbox85", pos, row_count)
			pos['LotQuantity'] = parse_float_num("LotQuantity", pos, row_count)
			pos['LotSumOfChangeInAI'] = parse_float_num("LotSumOfChangeInAI", pos, row_count)
			pos['LotSumOfBeginBalanceLocal'] = parse_float_num("LotSumOfBeginBalanceLocal", pos, row_count)
			pos['LotSumOfChangeAILocal'] = parse_float_num("LotSumOfChangeAILocal", pos, row_count)
			pos['LotSumOfPurSoldPaidRecLocal'] = parse_float_num("LotSumOfPurSoldPaidRecLocal", pos, row_count)
			pos['LotSumOfEndAccrualBalanceLocal'] = parse_float_num("LotSumOfEndAccrualBalanceLocal", pos, row_count)
			pos['LotSumOfChangeInAIBook'] = parse_float_num("LotSumOfChangeInAIBook", pos, row_count)
			pos['LotSumOfEndBalanceBook'] = parse_float_num("LotSumOfEndBalanceBook", pos, row_count)

		positions = Utils.create_iterator(list_positions)

		return positions

	def getTaxlotInterestIncome(self, positions):
		"""
		[List] positions
		=> [Dictionary] ([String] tax lot id -> [Float] interest income)

		From positions of a daily interest accrual detail report, compute
		interest income for each tax lot.
		"""
		#-- tax_lot_d. A dictionary of total interest income of each tax_lot_id
		tax_lot_d = dict()
		#-- calculate the "interest received during the period"
		pos_by_investment_date_d = dict()
		#-- group positions based on investment and date in a dictionary
		for pos in positions:
			investment_date_key = pos['Investment'] + pos['Date']
			#-- declare the dict value as a list element
			if investment_date_key not in pos_by_investment_date_d:
				# if type(pos_by_investment_date_d[investment_key]) is not list:
				pos_by_investment_date_d[investment_date_key] = []
			#-- add the position
			pos_by_investment_date_d[investment_date_key].append(pos)

		#-- find the total received interest payment for tax lot
		for investment_date_key, pos_list in pos_by_investment_date_d.items():
			#-- for each investment_date positions group (per investmnet per day)
			#-- 1. calculate the total Interest payment
			#-- 2. sum of quantity for each tax lot id
			#-- 3. sum of payment deduction
			tax_lot_quantity_d = dict()
			total_interest_payment = 0
			total_deduction = 0
			total_quantity = 0
			#-- has_interest_payment_event: mark if this group has any interest payment event 
			has_interest_payment_event = False
			for pos in pos_list:
				lot_id = pos['LotID']
				if pos['LotSumOfPurSoldPaidRecLocal'] > 0:
					total_interest_payment += pos['LotSumOfChangeInAIBook']
					#-- this group has 1 or more interest payment event
					has_interest_payment_event = True
				else:
					if pos['LotQuantity'] > 0:
						#-- add up LotQuantity of each LotID
						if lot_id not in tax_lot_quantity_d:
							tax_lot_quantity_d[lot_id] =  0
						tax_lot_quantity_d[lot_id] += pos['LotQuantity']
						#-- add up total qty per investment per day
						total_quantity += pos['LotQuantity']
					else:
						#-- add up for deduction process
						total_deduction += pos['LotSumOfChangeInAIBook']
			#-- Reduction Process
			#-- total interest payment = total interest payment - LotSumOfChangeInAIBook of the tax lot removed
			#-- if there are no has_interest_payment_event, no deduction process will be done
			if (has_interest_payment_event):
				#--  substract the abs value as total_deduction is a -ve value
				total_interest_payment = total_interest_payment - abs(total_deduction)
			else:
				total_interest_payment = 0
			#-- calculate the interest payment received per tax lot id and add to tax_lot_d
			for tax_lot_id, tax_lot_id_qty in tax_lot_quantity_d.items():
				if tax_lot_id not in tax_lot_d:
					tax_lot_d[tax_lot_id] =  0
				tax_lot_d[tax_lot_id] += tax_lot_id_qty / total_quantity * total_interest_payment
		
		#-- To find the starting and ending accrued interest of each tax_lot_id in the period
		#-- 1. group positions based on tax lot id
		pos_by_tax_lot_id_d = {}
		for pos in positions:
			if pos['LotID'] not in pos_by_tax_lot_id_d:
				pos_by_tax_lot_id_d[pos['LotID']] = []
			pos_by_tax_lot_id_d[pos['LotID']].append(pos)
		#-- sort the list of dictionary based on ascending tax_lot_id for easier debugging purpose
		#-- (if need to compare the value with excel)
		pos_by_tax_lot_id_d = {tax_lot_id: pos_by_tax_lot_id_d[tax_lot_id] for tax_lot_id in sorted(pos_by_tax_lot_id_d)}
		for tax_lot_id, pos_by_tax_lot_id_l in pos_by_tax_lot_id_d.items():
			#-- In each group, sort the positons based by field Date in ascending order
			#--   and find the earliest item with LotQuantity > 0
			sorted_pos_by_tax_lot_id_l = sorted(pos_by_tax_lot_id_l, key=lambda k: k['Date'])
			starting_accured_interest_pos = 0
			for pos in sorted_pos_by_tax_lot_id_l:
				if pos['LotQuantity'] > 0:
					starting_accured_interest_pos = pos['LotSumOfEndBalanceBook'] - pos['LotSumOfChangeInAIBook']
					break
			#-- to get the last position of the period, sort the positons in descending order
			#--   and find the earliest item with LotSumOfEndBalanceBook > 0
			sorted_pos_by_tax_lot_id_l = sorted(pos_by_tax_lot_id_l, key=lambda k: k['Date'], reverse=True)
			ending_accured_interest_pos = 0
			for pos in sorted_pos_by_tax_lot_id_l:
				if pos['LotSumOfEndBalanceBook'] > 0:
					ending_accured_interest_pos = pos['LotSumOfEndBalanceBook']
					break
			#-- interest income = ending value of accrued interest of the period - 
			#--    starting value of accrued interest of the period +
			#--    interest received during the period
			if tax_lot_id not in tax_lot_d:
				tax_lot_d[tax_lot_id] = 0
			#-- keep commented code for printing tax_lot_id|total_received|start_ai|end_ai to debug file
			#self.logger.debug(str(tax_lot_id) + " " +
			#	str(tax_lot_d[tax_lot_id]) + " " + 
			#	str(starting_accured_interest_pos) + " " + 
			#	str(ending_accured_interest_pos))
			tax_lot_d[tax_lot_id] += ending_accured_interest_pos - starting_accured_interest_pos
		
		#-- keep commented code for printing negative account to debug log if needed
		#tax_lot_d = {x:y for x,y in tax_lot_d.items() if y<0}
		#for tax_lot_id in tax_lot_d:
		#	self.logger.debug(str(tax_lot_id) + " " + str(tax_lot_d[tax_lot_id]))
		return tax_lot_d
