# Created: 7/29
# Name: Andrew Hill

#This code reads in and prepares data for analysis

import pandas as pd 
import numpy as np 
from datetime import datetime

def readData():
	"""Reads in data from .csv, adds features, and stores dataframes in list"""
	
	team_name_list = ['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 
				'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL',
				'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC',
				'SAS', 'TOR', 'UTA', 'WAS']

	team_dict = {}

	for i in range(len(team_name_list)):

		file_name = 'NBA Gambling Model - ' + team_name_list[i] + '.csv'
		temp_df = pd.read_csv(file_name) 

		temp_df_features = temp_df[['Season', 'Rk', 'Tm', 'Opp', 'G', 'Date', 'Opp', 'Unnamed: 4', 
									'ORtg', 'DRtg', 'Pace']]

		temp_df_features.columns = ['Season', 'Rk', 'Team_Points', 'Opp_Points', 'G', 'Date', 'Opp', 'Home_Away', 
									'ORtg', 'DRtg', 'Pace']

		temp_df_features = HomeAndAwayDummies(temp_df_features)

		temp_df_features = calculateNetRtg(temp_df_features)

		temp_df_features = calculateTmRest(temp_df_features)
		
		team_dict[team_name_list[i]] = temp_df_features

	return team_dict


def calculateTmRest(df):
	"""Calculates number of days rest since last game"""

	rest_list = [np.NaN]
	date_format = "%Y-%m-%d"

	for i in range(1, len(df.Date)):
		a = datetime.strptime(df.Date.iloc[i - 1], date_format)
		b = datetime.strptime(df.Date.iloc[i], date_format)
		delta = b - a
		if (delta.days - 1 > 30):
			rest_list.append(np.NaN)
		else:
			rest_list.append(delta.days - 1)

	df['daysRest'] = pd.DataFrame(rest_list)

	return df

def calculateOppRest(df, team_dict):
	"""Adds column for opponent's rest"""

def HomeAndAwayDummies(df):
	"""Creates dummy variable for Home (1) and Away (0)"""

	df['homeDummy'] = df.loc[:,'Home_Away'].apply(lambda x: 0 if (x == '@') else 1)

	return df

def calculateNetRtg(df):
	"""Calculates NetRtg from ORtg and DRtg"""

	df['NetRtg'] = pd.to_numeric(df['ORtg']) - pd.to_numeric(df['DRtg'])

	return df

def addSeasonNetRtg(df):
	"""Adds season netRtg columns for team and opp. and difference between the two"""

	seasons = [2013, 2014, 2015, 2016, 2017, 2018]



def parseLatLong(str):
	"""Converts latitude and longitude to decimal format"""

def computeDistanceTravelled(df, team_name):
	"""Calculates distance travelled (miles) from city to city"""
	
def appendElevationLatLong(team_name):
	"""Matches elevation, latitude, and longitude data with home team data"""

	df = pd.read_csv('ElevationLatLong.csv', index_col='Team')

	return df.loc[team_name, 'Elevation']

def randomSelection(team_dict):
	"""randomly selects a sample size for analysis"""


team_dict = readData()








