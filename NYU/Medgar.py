import pandas as pd 
import numpy as np

def readData():
	"""Reads in Lineup and Boxscore data to pandas Data Frame"""

	lu = pd.read_csv('Lineup.csv', header=1)
	bs = pd.read_csv('Boxscore.csv')

	lu = lu.drop(lu.index[len(lu)-1])

	return lu, bs

def playerNames(lu):
	"""Returns list of player names and lineup names"""
	
	lu_col = lu.columns

	player_names = []
	at_player = False
	index = 0
	while ('Unnamed:' not in lu_col[index]):
		if (at_player):
			player_names.append(lu_col[index])
		if (lu_col[index] == 'TS%'):
			at_player = True
		index += 1

	lineup_names = []
	index += 1
	while('Unnamed:' not in lu_col[index]):
		lineup_names.append(lu_col[index])
		index += 1

	return player_names, lineup_names

def calculateAdvancedStatistics(df, bs, temp_list):
	"""Calculates advanced statistics and appends to temp_list"""

	#MP
	temp_list.append(round(np.sum(df['Time']),1))

	#Possessions
	temp_list.append(round(np.sum(df['NYU Poss.'])))

	#+/-
	temp_list.append(int(np.sum(pd.to_numeric(df['PTS'], errors='coerce')) - np.sum(pd.to_numeric(df['PTS.1'], errors='coerce'))))

	#OffRtg
	if (np.sum(pd.to_numeric(df['NYU Poss.'])) == 0):
		temp_list.append(0)
	else:
		temp_list.append(round((np.sum(df['PTS'])/np.sum(df['NYU Poss.'])*100),1))

	#DefRtg
	if (np.sum(pd.to_numeric(df['Opp. Poss.'])) == 0):
		temp_list.append(0)
	else:	
		temp_list.append(round(np.sum(pd.to_numeric(df['PTS.1'], errors='coerce'))/np.sum(pd.to_numeric(df['Opp. Poss.'], errors='coerce'))*100,1))

	#NetRtg
	temp_list.append(round(temp_list[-2] - temp_list[-1],1))

	#TOV%
	#temp_list.append(round(int(bs.TO[bs['Player'] == temp_list[0]])/np.sum(pd.to_numeric(df['NYU Poss.'], errors='coerce'))*100,1))



	return temp_list

def advancedBoxscore(lu, bs, player_names):
	"""creates an advanced statistics boxscore for players and returns it as a dataframe"""

	col_headers = ['Player', 'MP', 'Poss.', '+/-', 'OffRtg', 'DefRtg', 'NetRtg']
	

	for i in range(len(player_names)):
		name = player_names[i]
		player_df = lu[lu[name] == 1]

		temp_list = [name]

		temp_list = calculateAdvancedStatistics(player_df, bs, temp_list)

		if (i == 0):
			advanced_boxscore_df = pd.DataFrame(np.array(temp_list).reshape(1,len(col_headers)))
			advanced_boxscore_df.columns = col_headers											 
		else:
			temp_list_df = pd.DataFrame(np.array(temp_list).reshape(1,len(col_headers)))
			temp_list_df.columns = col_headers
			advanced_boxscore_df = pd.concat([advanced_boxscore_df, temp_list_df], axis=0)
		
	
	team_list = ['Team']

	team_list = calculateAdvancedStatistics(lu, bs, team_list)

	team_list_df = pd.DataFrame(np.array(team_list).reshape(1,len(col_headers)))
	team_list_df.columns = col_headers
	advanced_boxscore_df = pd.concat([advanced_boxscore_df, team_list_df], axis=0)
	
	print(advanced_boxscore_df)
	return advanced_boxscore_df

lu, bs = readData()
player_names, lineup_names = playerNames(lu)
player_stats_df = advancedBoxscore(lu, bs, player_names)
lineup_stats_df = advancedBoxscore(lu, bs, lineup_names)

#player_stats_df.to_csv('MedgarPlayer.csv')
#lineup_stats_df.to_csv('MedgarLineup.csv')


