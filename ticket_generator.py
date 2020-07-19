import os
import sys
from datetime import datetime
from random import randint

import xlwt 


class HousieTicketGenerator:
	def __init__(self):
		self.first_row = []
		self.second_row = []
		self.third_row = []
		self.numbers_per_line = 5
		self.ticket_counter = 0
		self.numbers_per_ticket = []
		self.empty_separator = '--'
		self.total_indexes_per_ticket = set(range(0, 9))
		self.column_indexes_per_ticket = set()
		self.row_status = [False, False, False]
		self.workbook = xlwt.Workbook()
		self.ticket_folder_name = 'HousieTickets'
		self.ticket_file_name = os.path.join(self.ticket_folder_name, 'Housie_Tickets_{}.xls'.format(datetime.now().strftime("%d_%m_%Y__%H_%M_%S")))
		self.housie_sheet = self.workbook.add_sheet('Housie_Tickets')
		self.user_names = self.read_names()
		self.make_ticket_dir()

	def make_ticket_dir(self):
		os.makedirs(self.ticket_folder_name, exist_ok=True)

	@staticmethod
	def read_names():
		with open('names.txt', 'r') as f:
			data = f.readlines()
		users = [name.strip() for name in data]
		return users

	def get_five_random_row_indexes(self, last_row=False):
		tmp = []
		while True:
			if last_row:
				tmp = list(self.total_indexes_per_ticket.difference(self.column_indexes_per_ticket))
				last_row = False
			else:
				random_index = randint(0, 8)
				if random_index not in tmp:
					tmp.append(random_index)
					self.column_indexes_per_ticket.add(random_index)
			if len(tmp) == self.numbers_per_line:
				break
		return tmp

	def get_numbers_for_indexes(self, random_indexes):
		tmp = []
		for index in random_indexes:
			while True:
				starting_range = index * 10
				ending_range = (index * 10) + 9
				if starting_range == 0:
					starting_range = 1
				if ending_range == 89:
					ending_range = 90
				random_num = randint(starting_range, ending_range)
				if random_num not in self.numbers_per_ticket:
					tmp.append(random_num)
					self.numbers_per_ticket.append(random_num)
					break
			if len(tmp) == self.numbers_per_line:
				break
		return tmp

	@staticmethod
	def convert_int_to_str(num):
		return str(num)
		# return '{:02}'.format(num)

	def populate_row(self, last_row=False):
		tmp = [self.empty_separator for _ in range(9)]
		random_indexes = self.get_five_random_row_indexes(last_row=last_row)
		numbers_for_indexes = self.get_numbers_for_indexes(random_indexes)
		for index, num in zip(random_indexes, numbers_for_indexes):
			tmp[index] = self.convert_int_to_str(num)
		return tmp

	def write_to_excel(self, username=""):
		xlwt.add_palette_colour("custom_colour", 0x21)
		self.workbook.set_colour_RGB(0x21, 66, 236, 245)

		style = xlwt.easyxf('font: bold 1; font: height 600; pattern: pattern solid, fore_color custom_colour;'
							'align: horiz center; borders: top thick, bottom thick, left thick, right thick;')		

		self.housie_sheet.write_merge(self.ticket_counter, self.ticket_counter, 0, 8, 'Ticket - {}'.format(username), style)

		style = xlwt.easyxf('font: bold 1; font: height 800; pattern: pattern solid, fore_color custom_colour;'
							'align: horiz center; borders: top thick, bottom thick, left thick, right thick;')		

		for index, num in enumerate(self.first_row):
			self.housie_sheet.write(self.ticket_counter + 1, index, num, style)

		for index, num in enumerate(self.second_row):
			self.housie_sheet.write(self.ticket_counter + 2, index, num, style)

		for index, num in enumerate(self.third_row):
			self.housie_sheet.write(self.ticket_counter + 3, index, num, style)

		self.ticket_counter += 6

	def display(self, user_name):
		print('Ticket - {}'.format(user_name))
		for ticket_row in [self.first_row, self.second_row, self.third_row]:
			for num in ticket_row:
				print('{:>2}'.format(num), end=' ')
			print()
		print('\n')

	@staticmethod
	def check_for_int(arg):
		try:
			int(arg)
			return True
		except ValueError:
			return False

	def parse_args(self):
		if '-h' in sys.argv or '--help' in sys.argv:
			self.print_help()
			exit()
		args = sys.argv
		if len(args) > 1:
			self.user_names.clear()
			if len(args) == 2:
				arg = args[1]
				is_digit = self.check_for_int(arg)
				if is_digit:
					self.user_names = list(range(1, int(arg) + 1))
					return
			for arg in args[1:]:
				self.user_names.append(arg)

	@staticmethod
	def print_help():
		print('\nUsage :')
		print('\n1. python ticket_generator.py')
		print('This will read names.txt for any valid names (separated by newline)')
		print('\n2. python ticket_generator.py <15>')
		print('This will generate a total of <15> Housie Tickets (Ticket -1 to Ticket - 15')
		print('\n3. python ticket_generator.py <Tyrion Bran "Jon Snow" Sansa>')
		print('This will generate a total of <3> Housie Tickets (Ticket - Tyrion, Ticket - Bran, Ticket - Jon Snow, Ticket - Sansa)')

	def get_random_row_index(self):
		while True:
			random_row_index = randint(0, 2)
			if not self.row_status[random_row_index]:
				self.row_status[random_row_index] = True
				return random_row_index

	def sort_columns(self):
		tmp = [self.first_row, self.second_row, self.third_row]
		for col_index in range(0, 9):
			col_i_first_element = int(tmp[0][col_index]) if tmp[0][col_index] != self.empty_separator else self.empty_separator
			col_i_second_element = int(tmp[1][col_index]) if tmp[1][col_index] != self.empty_separator else self.empty_separator
			col_i_third_element = int(tmp[2][col_index]) if tmp[2][col_index] != self.empty_separator else self.empty_separator

			tmp_2 = []
			if col_i_first_element != self.empty_separator:
				tmp_2.append([0, col_i_first_element])
			if col_i_second_element != self.empty_separator:
				tmp_2.append([1, col_i_second_element])
			if col_i_third_element != self.empty_separator:
				tmp_2.append([2, col_i_third_element])

			for i in range(1, 4):
				for index, (_, ele) in enumerate(tmp_2[:len(tmp_2) - 1]):
					if ele > tmp_2[index + 1][1]:
						temp = tmp_2[index][1]
						tmp_2[index][1] = tmp_2[index + 1][1]
						tmp_2[index + 1][1] = temp

			for updated_index, ele in tmp_2:
				if updated_index == 0:
					self.first_row[col_index] = self.convert_int_to_str(ele)
				
				if updated_index == 1:
					self.second_row[col_index] = self.convert_int_to_str(ele)
				
				if updated_index == 2:
					self.third_row[col_index] = self.convert_int_to_str(ele)

	def populate_rows(self):
		rows_indexes_order = []
		for i in range(3):
			rows_indexes_order.append(self.get_random_row_index())

		for index, row_index in enumerate(rows_indexes_order):
			last_row = False
			if index == 2:
				last_row = True
				
			if row_index == 0:
				self.first_row = self.populate_row(last_row=last_row)
			elif row_index == 1:
				self.second_row = self.populate_row(last_row=last_row)
			elif row_index == 2:
				self.third_row = self.populate_row(last_row=last_row)
		self.sort_columns()

	def re_init(self):
		self.first_row.clear()
		self.second_row.clear()
		self.third_row.clear()
		self.numbers_per_ticket.clear()
		self.column_indexes_per_ticket.clear()
		self.row_status = [False, False, False]

	def main(self):
		self.parse_args()
		if self.user_names:
			print('Generating Tickets for : {}\n'.format(self.user_names))
			for user_name in self.user_names:
				if user_name:
					self.populate_rows()
					self.display(user_name)
					self.write_to_excel(user_name)
					self.re_init()
			self.workbook.save(self.ticket_file_name)
			print('Tickets Generated : {}'.format(self.ticket_file_name))
		else:
			print('No Valid User Names were found...!!!')


if __name__ == '__main__':
	HousieTicketGenerator().main()
