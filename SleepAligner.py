## Sleep Aligner, Version 1.0
## Last update:  6/11/2017, Aaron Coyner


## Program combines two user-selected datasets for the Harvard sleep study. 
## Created by: Connor Smith, Sean Babcock and Aaron Coyner
## OHSU BMI 552B/652B, AMIA design challenge

## Datasets from sleep log data (converted externally to CSV from XLS) and actitgraphy data originally 
## in CSV format

## Output:  Single .csv file aligning data by date.  Sleep log and actigraphy data pertaining to wake 
## and sleep times listed first with calculations of delta times.  Remaining sleep log data and 
## Actigraphy "sleep" data appended to the end of each row.


import sys
import csv
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, qApp, QMainWindow,
								QLineEdit, QFileDialog, QMessageBox, QAction, QLabel)
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import QtCore

class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.home()


	def home(self):
		## create button for loading actigraphy data
		self.btn_act = QPushButton('Load Actigraphy Data', self)
		self.btn_act.setToolTip('Opens file selector for seleciton of actigraphy data file')
		self.btn_act.resize(self.btn_act.sizeHint())
		self.btn_act.move(25, 25)

		## link button to file dialog pop-up window
		self.btn_act.clicked.connect(self.select_act)

		## display currently selected actigraphy data file
		self.act = QLineEdit(self)
		self.act.resize(350, 25)
		self.act.move(225, 25)
		self.act.setAlignment(QtCore.Qt.AlignCenter)
		self.act.setStyleSheet('QLineEdit {color: red}')
		self.act.setText('Not Selected')
		self.act.setReadOnly(True)



		## create button for loading sleep log data
		self.btn_log = QPushButton('Load Sleep Log Data', self)
		self.btn_log.setToolTip('Opens file selector for seleciton of sleep log data file')
		self.btn_log.resize(self.btn_act.sizeHint())
		self.btn_log.move(25, 75)

		## link button to file dialog pop-up window
		self.btn_log.clicked.connect(self.select_log)

		# display currently selected sleep log data file
		self.log = QLineEdit(self)
		self.log.resize(350, 25)
		self.log.move(225, 75)
		self.log.setAlignment(QtCore.Qt.AlignCenter)
		self.log.setStyleSheet('QLineEdit {color: red}')
		self.log.setText('Not Selected')
		self.log.setReadOnly(True)



		## create button for selecting output folder
		self.btn_dest = QPushButton('Set Destination Folder', self)
		self.btn_dest.setToolTip('Opens folder selector for selection of output file')
		self.btn_dest.resize(self.btn_act.sizeHint())
		self.btn_dest.move(25, 125)

		## link button to file dialog pop-up window
		self.btn_dest.clicked.connect(self.select_dest)

		# display currently selected output folder
		self.dest = QLineEdit(self)
		self.dest.resize(350, 25)
		self.dest.move(225, 125)
		self.dest.setAlignment(QtCore.Qt.AlignCenter)
		self.dest.setStyleSheet('QLineEdit {color: red}')
		self.dest.setText('Not Selected')
		self.dest.setReadOnly(True)



		self.label = QLabel(self)
		self.label.setText('Output file name')
		self.label.move(90, 175)

		# display current output file name
		self.out_file_name = 'result_file'
		self.out_file = QLineEdit(self)
		self.out_file.setFocus()
		self.out_file.resize(350, 25)
		self.out_file.move(225, 175)
		self.out_file.setText(self.out_file_name)



		## create 'run' button
		self.btn_run = QPushButton('Run', self)
		self.btn_run.setToolTip('Runs program: combines loaded actigraphy and sleep ' + 
			'log data files and outputs the results to the destination foler')
		self.btn_run.resize(self.btn_run.sizeHint())
		self.btn_run.move(275, 225)

		## link button to main source code for file alignment
		self.btn_run.clicked.connect(self.run)

		## connect Return button press to run button click
		self.out_file.returnPressed.connect(self.btn_run.click)


		## set window title, placement and dimensions
		self.setFixedSize(600, 275)
		self.setWindowTitle('Sleep Aligner v1.1')    
		self.show()


	## opens file dialog for actigraphy data selection
	def select_act(self):
		self.act_file, _ = QFileDialog.getOpenFileName(self, 'Select Actigraphy Data File',
			filter='Actigraphy data files (*.csv)')

		if self.act_file == '':
			pass
		else:
			self.act_file = str(self.act_file)
			self.act.setText(self.act_file)
			self.act.setStyleSheet('QLineEdit {color: black}')
			self.act.setAlignment(QtCore.Qt.AlignLeft)


	## opens file dialog for sleep log data selection
	def select_log(self):
		self.log_file, _ = QFileDialog.getOpenFileName(self, 'Select Sleep Log Data File',
			filter='Sleep log data files (*.csv)')

		if self.log_file == '':
			pass
		else:
			self.log_file = str(self.log_file)
			self.log.setText(self.log_file)
			self.log.setStyleSheet('QLineEdit {color: black}')
			self.log.setAlignment(QtCore.Qt.AlignLeft)


	## opens file dialog for destination folder selections
	def select_dest(self):
		self.dest_folder = str(QFileDialog.getExistingDirectory(self, 'Select Destination Folder'))
		if self.dest_folder == '':
			pass
		else:
			self.dest.setText(self.dest_folder)
			self.dest.setStyleSheet('QLineEdit {color: black}')	
			self.dest.setAlignment(QtCore.Qt.AlignLeft)


	def close_application(self):
		sys.exit()


	## implements code to align files and return output file
	def run(self):
		## make sure all files and folders are selected and warn user if not
		if self.act.text()  == 'Not Selected':
			msg = 'Please select an actigraphy data file'
			reply = QMessageBox.warning(self, 'Warning!', msg, QMessageBox.Ok)

		elif self.log.text()  == 'Not Selected':
			msg = 'Please select a sleep log data file'
			reply = QMessageBox.warning(self, 'Warning!', msg, QMessageBox.Ok)

		elif self.dest.text()  == 'Not Selected':
			msg = 'Please select a destination folder'
			reply = QMessageBox.warning(self, 'Warning!', msg, QMessageBox.Ok)


		## if all files and folders are selected, run code...
		else:

			try:

				inFile = open(self.act_file, "r")
				actData = list(csv.reader(inFile))
				inFile.close()

				inFile = open(self.log_file, "r")
				logData = list(csv.reader(inFile))
				inFile.close()

				# Store subset of actigraph statistics data: REST, ACTIVE, SLEEP, DAILY
				# Capture header in actHeader
				restList = []
				activeList = []
				sleepList = []
				dailyList = []
				for elem in actData:
					 if len(elem) > 0:
						 if elem[0] == "REST":
							 restList.append(elem)
						 elif elem[0] == "ACTIVE":
							 activeList.append(elem)
						 elif elem[0] == "SLEEP":
							 sleepList.append(elem)
						 elif elem[0] == "DAILY":
							 dailyList.append(elem)
						 if elem[0] == 'Interval Type':
							 actHeader = elem
						 if elem[0] == 'Full Name:':
							 # or use 'Identity:' if this is the patient identity and not just actigraph
							 ID = elem[1]

				# Configure date from mm/dd/yy format to mm/dd/yyyy format
				def date_config(inDate):
					parts = inDate.split("/")
					year = "20" + parts[2]
					newDate = inDate.replace(parts[2], year)
					return(newDate)

				# Store sleep log information.  Remove header and store in logHeader
				logHeader = logData[0]
				logData.pop(0)
				# Last row empty so remove
				logData.pop(-1)
				rowNum = 1
				while rowNum < len(logData):
					logData[rowNum][2] = date_config(logData[rowNum][2])
					rowNum += 1

				# Store all sleep log dates and actigraph dates to use when linking data
				logDates = []
				sleepDates = []
				for row in logData:
					inDate = row[2]
					parts = inDate.split("/")
					logDates.append(int(parts[1]))
				for row in sleepList:
					inDate = row[2]
					parts = inDate.split("/")
					sleepDates.append(int(parts[1]))


				# Create linked database list
				# Oreder: 0: sleep log data, 1: daily, 2: sleep, 3: rest, 4: active.  Date offset 5
				#  Matcvh by date.  If either log date or actigraph date missing then fill with N/A
				dateList = [] 
				linkList = []
				i = 0
				j = 0
				if len(logDates) >= len(sleepDates):
					done = len(logDates) - 1
				else:
					done = len(sleepDates) - 1
				skip = 0
				while done != 0:
					if (logDates[i] == sleepDates[j]) and skip == 0:
						linkList.append(logData[i])
						linkList.append(dailyList[j])
						linkList.append(sleepList[j])
						linkList.append(restList[j])
						linkList.append(activeList[j])
						dateList.append(logData[i][2])
						i += 1
						j += 1
					elif (logDates[i] < sleepDates[j]) and skip == 0:
						linkList.append(logData[i])
						linkList.append(["N/A"])
						linkList.append(["N/A"])
						linkList.append(["N/A"])
						linkList.append(["N/A"])
						dateList.append(logData[i][2])
						i += 1
					elif (logDates[i] < sleepDates[j]) and skip == 1:
						linkList.append(["N/A"])
						linkList.append(dailyList[j])
						linkList.append(sleepList[j])
						linkList.append(restList[j])
						linkList.append(activeList[j])
						dateList.append(dailyList[j][2])
						j += 1
					elif (logDates[i] > sleepDates[j]) and skip == 0:
						linkList.append(["N/A"])
						linkList.append(dailyList[j])
						linkList.append(sleepList[j])
						linkList.append(restList[j])
						linkList.append(activeList[j])
						dateList.append(dailyList[j][2])
						j += 1
					elif (logDates[i] > sleepDates[j]) and skip == 1:
						linkList.append(logData[i])
						linkList.append(["N/A"])
						linkList.append(["N/A"])
						linkList.append(["N/A"])
						linkList.append(["N/A"])
						dateList.append(logData[i][2])
						i += 1
					# Check for end of list for unequal lists
					if (i == len(logDates)) and (j < len(sleepDates) - 1):
						i = len(logDates) - 1
						skip = 1
						done -= 1
					elif (j == len(sleepDates)) and (i < len(logDates) - 1):
						j = len(sleepDates) - 1
						skip = 1
						done -= 1
					else:
						done -= 1  

				# Define all functions
				# time builder.  Combines hours, mins, AM/PM into one string
				def build_time(hr, min, ap):
					time = hr + ':' + min
					if ap == '0':
						time = time + ' AM'
					elif ap == '1':
						time = time + ' PM'
					return(time)

				# Break time into hours, min, sec and remove AM/PM
				def split_time(timeIn):
					Tnum = timeIn.split(' ')
					Tnum = Tnum[0].split(':')
					hr = int(Tnum[0])
					min = int(Tnum[1])
					if len(Tnum) > 2:
						sec = int(Tnum[2])
					else: 
						sec = 0
					return(hr, min, sec)

				# Calculate differences in two times (td1 - td2)
				def time_diff(td1, td2):
					# in date/time format
					# check for N/A 
					if (td1 == 'N/A') or (td2 == 'N/A'):
						return('N/A')
					
					temp1 = td1.split(' ')
					temp2 = td2.split(' ')
					if len(temp1) > 2:
						time1 = time_convert(temp1[1] + ' ' + temp1[2])
						time2 = time_convert(temp2[1] + ' ' + temp2[2])
					else:
						time1 = temp1[1]
						time2 = temp2[1]
					#print(time1, time2)
					h1, m1, s1 = split_time(time1)
					h2, m2, s2 = split_time(time2)
					date1 = temp1[0].split('/')
					date2 = temp2[0].split('/')
					if int(date1[1]) == int(date2[1]):
						deltaHours = h2 - h1
					else:
						dd = int(date2[1]) - int(date1[1])
						deltaHours = ((h2 - h1) + 24) + ((dd - 1) * 24)
					# Calculation ignoring seconds at this time
					Sout = 0
					Tdiff = abs((deltaHours * 60) + (m2 - m1))
					if Tdiff // 60 >= 1:
						Hout = Tdiff // 60
						Mout = Tdiff - ((Tdiff // 60) * 60)
					else:
						Hout = 0
						Mout = Tdiff
					timeOut = str(abs(Hout)) + ':' + str(abs(Mout)) + ':' + str(Sout)
					return(timeOut)

				# Add two times. Return as a string with AM/PM 
				def time_add(t1, t2):
					temp1 = t1.split(' ')
					if len(temp1) > 1:
						ampm = 1
						h1, m1, s1 = split_time(temp1[0])
					else:
						ampm = 0
						h1, m1, s1 = split_time(t1)
					h2, m2, s2 = split_time(t2)
					ht = h1 + h2
					mt = m1 + m2
					if mt >= 60:
						ht += 1
						mt = mt - 60
					if ampm == 1:
						if (ht == 12) & (temp1[1] == 'PM'):
							temp1[1] = 'AM'
						elif (ht > 12) & (temp1[1] == 'PM'):
							ht = ht - 12
							temp1[1] = 'AM'
						outTime = str(ht) + ':' + str(mt) + ':' + '00' + ' ' + temp1[1]
					else:
						if ht == 24:
							ht = 0
						elif ht > 24:
							ht = ht - 24
						outTime = str(ht) + ':' + str(mt) + ':' + '00'
					return(outTime)

				def time_convert(timeIn):
					# Converts standard/military time. Assumes time is a string
					Tformat = timeIn.split(' ')
					if len(Tformat) > 1:
						# Standard time
						Th, Tm, Ts = split_time(timeIn)
						if Tformat[1] == 'PM':
							Th = Th + 12
						timeStr = str(Th) + ':' + str(Tm) + ':' + str(Ts)
					else:
						Th, Tm, Ts = split_time(timeIn)
						if Th > 12:
							Th = Th - 12
							Tx = 'PM'
						elif Th == 12:
							Tx = 'PM'
						else:
							Tx = 'AM'
						timeStr = str(Th) + ':' + str(Tm) + ':' + str(Ts) + ' ' + Tx
					return(timeStr)

				# Build date/time format.  Span dates depending on AM/PM.  Use for sleep log 
				def append_date(Tin, D1, D2):
					temp = Tin.split(' ')
					if temp[1] == 'PM':
						DTout = D1 + ' ' + Tin
					else:
						DTout = D2 + ' ' + Tin
					return(DTout)

				# Main
				# build dictionary of sleep log data locations
				logLoc = {}
				index = 0
				for elem in logHeader:
					logLoc.update({elem:index})
					index += 1
				#print(' ')
				#print(logLoc)

				# build dictionary of actigraph data locations
				actLoc = {}
				index = 0
				for elem in actHeader:
					actLoc.update({elem:index})
					index += 1
				#print(' ')
				#print(actLoc)

				# build output header
				outHeader = ['SUBJ_ID', 'DATE_START', 'DATE_END', 'LOG_ACTIVE_START', 'ACT_ACTIVE_START', 
								'DIF_ACTIVE_START', 'LOG_BED_START', 'ACT_BED_START', 'DIF_BED_START',
								'LOG_SLEEP_START', 'ACT_SLEEP_START', 'DIF_SLEEP_START', 'LOG_SLEEP_END',
								'ACT_SLEEP_END', 'DIF_SLEEP_END', 'LOG_BED_END', 'ACT_BED_END',
								'DIF_BED_END', 'LOG_SLEEP_QUALITY']
				# Log portion
				logSkip = [logLoc['final_awake_time'], logLoc['bedtime_hr'], logLoc['bedtime_min'], 
							logLoc['bedtime_am_pm'], logLoc['fall_asleep_hr'], logLoc['fall_asleep_min'],
							logLoc['try_sleep_hr'], logLoc['try_sleep_min'], logLoc['try_sleep_am_pm'], 
							logLoc['awake_hr'], logLoc['awake_min'], logLoc['awake_am_pm'], 
							logLoc['final_awake_time'], logLoc['sleep_quality']]
				n = 0
				for elem in logHeader:
					if n in logSkip:
						pass
					else:
						outHeader.append('log_'+elem)
					n += 1
				actSkip = [actLoc['Start Date'], actLoc['Start Time'], actLoc['End Date'], 
							actLoc['End Time']]
				for elem in actHeader:
					if n in actSkip:
						pass
					else:
						outHeader.append('act_'+elem)
					n += 1

				# Walk through linkList to compute output list
				# time spans awake day1 through awake day2
				# sleep logs look ahead to get awake from day2
				# actigraph looks back one day to get awake time for that day (day1 - 1)
				outList = []
				offset = 0
				dateIndex = 0
				while offset < len(linkList):
					rowList = ['Name/ID']
					if dateIndex < len(dateList) - 1:
						date1 = dateList[dateIndex]
						date2 = dateList[dateIndex+1]
					else:
						date1 = dateList[dateIndex]
						date2 = 'N/A'
					# Walk through sleep log
					newRow1 = []
					if len(linkList[offset]) > 1:
						# For initial awake time make date the same since this is the start of the 
						# time period and will span midnight
						newRow1.append(append_date(linkList[offset][logLoc['final_awake_time']], 
										date1, date1))
						temp = build_time(linkList[offset][logLoc['bedtime_hr']], 
											linkList[offset][logLoc['bedtime_min']],
											linkList[offset][logLoc['bedtime_am_pm']])
						newRow1.append(append_date(temp, date1, date2))
						time2 = build_time(linkList[offset][logLoc['fall_asleep_hr']], 
											linkList[offset][logLoc['fall_asleep_min']], 'null')      
						time1 = build_time(linkList[offset][logLoc['try_sleep_hr']], 
											linkList[offset][logLoc['try_sleep_min']], 
											linkList[offset][logLoc['try_sleep_am_pm']])
						logSleep = time_add(time1, time2)
						newRow1.append(append_date(logSleep, date1, date2))
						if offset + 5 < len(linkList):
							if len(linkList[offset+5]) > 1:
								newRow1.append(append_date(linkList[offset+5][logLoc['final_awake_time']],
															date1, date2))
								temp = build_time(linkList[offset+5][logLoc['bed_out_hr']], 
													linkList[offset+5][logLoc['bed_out_min']], 
													linkList[offset+5][logLoc['bed_out_am_pm']])
								newRow1.append(append_date(temp, date1, date2))
								newRow1.append(linkList[offset+5][logLoc['sleep_quality']])
							else:
								newRow1.append('N/A')
								newRow1.append('N/A')
								newRow1.append('N/A')
						else:
							newRow1.append('N/A')
							newRow1.append('N/A')
							newRow1.append('N/A')
					else:
						newRow1 = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
					#print(newRow1)
					# Walk through actigraph data
					newRow2 = []
					# Check if actigraph data available for the current date
					if len(linkList[offset+1]) == 1:
						newRow2 = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
					else:
						if offset == 0:
							# Initial date has no previous data
							newRow2.append('N/A')
						elif len(linkList[(offset-5)+2]) > 1:
							newRow2.append(linkList[(offset-5)+2][actLoc['End Date']] + ' ' + 
											linkList[(offset-5)+2][actLoc['End Time']])
						else:
							newRow2.append('N/A')
						newRow2.append(linkList[offset+3][actLoc['Start Date']] + ' ' + 
										linkList[offset+3][actLoc['Start Time']])
						newRow2.append(linkList[offset+2][actLoc['End Date']] + ' ' + 
										linkList[offset+2][actLoc['End Time']])
						newRow2.append(linkList[offset+3][actLoc['End Date']] + ' ' + 
										linkList[offset+3][actLoc['End Time']])
						newRow2.append('N/A')
					
					# Combine rowLists and make calculations
					# Calculations in columns 3, 6, 9, 12, 15
					combRow = [ID, date1, date2]
					for n in range(len(newRow1)-1):
						combRow.append(newRow1[n])
						combRow.append(newRow2[n]) 
						combRow.append(time_diff(newRow1[n], newRow2[n]))
					combRow.append(newRow1[-1])

					# add remaining log/act data using sleep for act data (sleep offset = 2)
					n = 0
					if len(linkList[offset]) > 1:
						for elem in linkList[offset]:
							if n in logSkip:
								pass
							else:
								combRow.append(elem)
							n += 1
					else:
						for i in range(len(logHeader) - len(logSkip) + 1):
							combRow.append(' ')
					# remaining actigraph data
					n = 0
					for elem in linkList[offset+2]:
						if n in actSkip:
							pass
						else:
							combRow.append(elem)
						n += 1
					#print('Combined', combRow)
					# add new combined row list to outList
					outList.append(combRow)
					dateIndex += 1
					offset += 5

				#for elem in outList:
				#   print(elem)

				# Write CSV file to read into Excel 
				fh = open(str(self.dest_folder + '/' + self.out_file.text() + '.csv'), 'w')
				w = csv.writer(fh, delimiter=',')
				w.writerow(outHeader)
				w.writerows(outList[:])

				fh.close()


			except:
				msg = str('\tError aligning data. \n\nPlease ensure that proper actigraphy and sleep ' +
				 			'log data sets have been selected.')
				reply = QMessageBox.warning(self, 'Warning!', msg, QMessageBox.Ok)




## runs program
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Window()
	sys.exit(app.exec_())