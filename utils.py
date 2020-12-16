import os
from os.path import abspath, dirname
from clamc_yield_report.constants import Constants

class Utils:

	#-- return and indicate if the file is one of the following
	#--		1: investment position
	#--		2: profit loss
	#--		3: daily interest
	@staticmethod
	def get_file_type(input_filepath):
		head, filename = os.path.split(input_filepath)
		filename = filename.lower()
		if (Constants.FILENAME_INVESTMENT_POSITION in filename):
			return Constants.FILETYPE_INVESTMENT
		elif (Constants.FILENAME_PROFIT_LOSS in filename):
			return Constants.FILETYPE_PROFIT_LOSS
		elif (Constants.FILENAME_DAILY_INTEREST in filename):
			return Constants.FILENAME_DAILY_INTEREST
		else:
			return Constants.FILETYPE_UNKNOWN

	#-- function for constucting iterator
	@staticmethod
	def create_iterator(input_list):
		for item in input_list:
			yield item

	#-- function for constucting iterator
	@staticmethod
	def get_current_directory():
		return dirname(abspath(__file__))