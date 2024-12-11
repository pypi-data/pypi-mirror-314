class Server(object):

	def __init__(self, si):

		self.si = []

		for i in si.split('\t'):
			try:
				value = int(i)
				self.si.append(value)
				continue
			except:
				pass

			try:
				value = float(i)
				self.si.append(value)
				continue
			except:
				pass

			try:
				value = str(i)
				self.si.append(value)
			except:
				pass

		self.reservedSlots = self.si[29]
		self.wallTime = self.si[28]
		self.team2 = self.si[27]
		self.team1 = self.si[26]
		self.ranked = self.si[25]
		self.autoBalanceTeam = self.si[24]
		self.timeLimit = self.si[23]
		self.worldSize = self.si[22]
		self.modDir = self.si[21]
		self.gameMode = self.si[20]
		self.timeLeft = self.si[19]
		self.roundTime = self.si[18]
		self.team2_null = self.si[17]
		self.team2_tickets = self.si[16]
		self.team2_startTickets = self.si[15]
		self.team2_TicketState = self.si[14]
		self.team2_Name = self.si[13]
		self.team1_null = self.si[12]
		self.team1_tickets = self.si[11]
		self.team1_startTickets = self.si[10]
		self.team1_TicketState = self.si[9]
		self.team1_Name = self.si[8]
		self.serverName = self.si[7]
		self.nextMapName = self.si[6]
		self.currentMapName = self.si[5]
		self.joiningPlayers = self.si[4]
		self.connectedPlayers = self.si[3]
		self.maxPlayers = self.si[2]
		self.currentGameStatus = self.si[1]
		self.version = self.si[0]

class Player():

	def __init__(self, player):
		self.player = player

		self.index = self.player[0]
		self.getName = self.player[1]
		self.getTeam = self.player[2]
		self.getPing = self.player[3]
		self.isConnected = self.player[4]
		self.isValid = self.player[5]
		self.isRemote = self.player[6]
		self.isAIPlayer = self.player[7]
		self.isAlive = self.player[8]
		self.isManDown = self.player[9]
		self.getProfileId = self.player[10]
		self.isFlagHolder = self.player[11]
		self.getSuicide = self.player[12]
		self.getTimeToSpawn = self.player[13]
		self.getSquadId = self.player[14]
		self.isSquadLeader = self.player[15]
		self.isCommander = self.player[16]
		self.getSpawnGroup = self.player[17]
		self.getAddress = self.player[18]
		self.scoreDamageAssists = self.player[19]
		self.scorePassengerAssists = self.player[20]
		self.scoreTargetAssists = self.player[21]
		self.scoreRevives = self.player[22]
		self.scoreTeamDamages = self.player[23]
		self.scoreTeamVehicleDamages = self.player[24]
		self.scoreCpCaptures = self.player[25]
		self.scoreCpDefends = self.player[26]
		self.scoreCpAssists = self.player[27]
		self.scoreCpNeutralizes = self.player[28]
		self.scoreCpNeutralizeAssists = self.player[29]
		self.scoreSuicides = self.player[30]
		self.scoreKills = self.player[31]
		self.scoreTKs = self.player[32]
		self.vehicleType = self.player[33]
		self.kitTemplateName = self.player[34]
		self.kiConnectedAt = self.player[35]
		self.deaths = self.player[36]
		self.score = self.player[37]
		self.vehicleName = self.player[38]
		self.rank = self.player[39]
		self.position = self.player[40]
		self.idleTime = self.player[41]
		self.keyhash = self.player[42]
		self.punished = self.player[43]
		self.timesPunished = self.player[44]
		self.timesForgiven = self.player[45]

class Players():

	def __init__(self, pl):
		self.pl = {}
		self.pi = []

		self.players = None
		self.playersTeam1 = 0
		self.playersTeam2 = 0

		self.scoreTeam1 = 0
		self.scoreTeam2 = 0

		self.killsTeam1 = 0
		self.killsTeam2 = 0

		self.deathsTeam1 = 0
		self.deathsTeam2 = 0

		self.pingTeam1 = 0.00
		self.pingTeam2 = 0.00

		self.kdrTeam1 = 0.00
		self.kdrTeam2 = 0.00

		self.pingTeam1_all = 0
		self.pingTeam2_all = 0

		for pi_ in pl.split('\r'):
			self.pi = []
			for p in pi_.split('\t'):
				try:
					value = int(p)
					self.pi.append(value)
					continue
				except:
					pass

				try:
					value = float(p)
					self.pi.append(value)
					continue
				except:
					pass

				try:
					value = str(p)
					self.pi.append(value)
				except:
					pass
			if self.pi[0] == '': break
			self.pl[self.pi[0]] = self.pi

		self.players = self.pl

		for i, y in self.players.items():
			try:
				if y[2] == 1:
					self.playersTeam1 += 1
					self.scoreTeam1 += y[37]
					self.killsTeam1 += y[31]
					self.deathsTeam1 += y[36]
					self.pingTeam1_all += y[3]
			except:
				pass

			try:
				if y[2] == 2:
					self.playersTeam2 += 1
					self.scoreTeam2 += y[37]
					self.killsTeam2 += y[31]
					self.deathsTeam2 += y[36]
					self.pingTeam2_all += y[3]
			except:
				pass

		try:
			self.kdrTeam1 = float('{:.2f}'.format(self.killsTeam1 / self.deathsTeam1))
			self.kdrTeam2 = float('{:.2f}'.format(self.killsTeam2 / self.deathsTeam2))

			self.pingTeam1 = float('{:.2f}'.format(self.pingTeam1_all / self.playersTeam1))
			self.pingTeam2 = float('{:.2f}'.format(self.pingTeam2_all / self.playersTeam2))
		except ZeroDivisionError as e:
			pass

class Bf2cc():
	def __init__(self, client):
		self.__client = client

	def pause(self):
		self.__client._has_full_drive()
		return self.__client.rcon_invoke("bf2cc pause")

	def unpause(self):
		self.__client._has_full_drive()
		return self.__client.rcon_invoke("bf2cc unpause")

	@property
	def info(self):
		self.__client._has_full_drive()
		return self.__client.rcon_invoke("bf2cc check")

	@property
	def server(self):
		self.__client._has_full_drive()
		data = self.__client.rcon_invoke("bf2cc si")
		return Server(data)

	#@property
	#def players(self):
	#	self.__client._has_full_drive()
	#	data = self.__client.rcon_invoke("bf2cc pl")
	#	return Server(data)