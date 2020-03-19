import threading
import DobotDllType as dType

PLATEAU = {
	'p1':{'x': 156, 'y': -52, 'z': -25, 'r': 0},
	'p2':{'x': 156, 'y':   0, 'z': -25, 'r': 0},
	'p3':{'x': 156, 'y':  52, 'z': -25, 'r': 0},
	'p4':{'x': 208, 'y': -52, 'z': -25, 'r': 0},
	'p5':{'x': 208, 'y':   0, 'z': -25, 'r': 0},
	'p6':{'x': 208, 'y':  52, 'z': -25, 'r': 0},
	'p7':{'x': 256, 'y': -52, 'z': -25, 'r': 0},
	'p8':{'x': 256, 'y':   0, 'z': -25, 'r': 0},
	'p9':{'x': 256, 'y':  52, 'z': -25, 'r': 0}
}

ZONE_DOBOT = {
	'z1':{'x': 70, 'y': 208, 'z': -25, 'r': 0},
	'z2':{'x': 47, 'y': 227, 'z': -25, 'r': 0},
	'z3':{'x': 50, 'y': 182, 'z': -25, 'r': 0},
	'z4':{'x': 95, 'y': 227, 'z': -25, 'r': 0},
	'z5':{'x': 95, 'y': 182, 'z': -25, 'r': 0}
}

ZONE_BASE = {'x': 208, 'y':   0, 'z': 100, 'r' : 0}
CIR_POINT = {'x': 208, 'y': 143, 'z':  15, 'r' : 0}

CON_STR = {
	dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
	dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
	dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

class MyDobot:
	def __init__(self):
		#Load Dll
		self.api = dType.load()
		self.state = dType.DobotConnect.DobotConnect_NotFound

		self.roundCount = 1

		self.zoneBase = [ZONE_BASE['x'],  ZONE_BASE['y'],  ZONE_BASE['z'], ZONE_BASE['r']]
		self.cirPoint = [CIR_POINT['x'], CIR_POINT['y'], CIR_POINT['z'], CIR_POINT['r']]
		
	def connectDobot(self, portcom="COM6", baudrate=115200):
		#Connect Dobot
		self.state = dType.ConnectDobot(self.api, portcom, baudrate)[0]
		print("Connect status:",CON_STR[self.state])

	def initDobot(self):
		if (self.state != dType.DobotConnect.DobotConnect_NoError):
			print("Robot occupied or not found")
			return False

		#Async Motion Params Setting
		# dType.SetHOMEParams(self.api, 250, 0, 50, 0, isQueued = 1)
		dType.SetPTPJointParams(self.api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
		dType.SetPTPCommonParams(self.api, 100, 100, isQueued = 1)

		#Clean Command Queued
		dType.SetQueuedCmdClear(self.api)

		#Start to Execute Command Queued
		dType.SetQueuedCmdStartExec(self.api)

		#Move to Default Location with open Gripper
		dType.SetPTPCmdEx(self.api, 1, self.zoneBase, 1)
		dType.SetEndEffectorGripperEx(self.api, 1, 0)
		dType.SetWAITCmdEx(self.api, 0.5, 1)
		dType.SetEndEffectorGripperEx(self.api, 0, 0)

		self.roundCount = 1

	def movePawnTo(self, location):

		if (self.state != dType.DobotConnect.DobotConnect_NoError):
			print("Robot occupied or not found")
			return False

		if(self.roundCount > 5):
			print("Too many round...")
			return False
		try:
			zone = "z{}".format(self.roundCount)
			currentZone = [ZONE_DOBOT[zone]['x'],  ZONE_DOBOT[zone]['y'],  ZONE_DOBOT[zone]['z'], ZONE_DOBOT[zone]['r']]
			currentZone_up = [ZONE_DOBOT[zone]['x'],  ZONE_DOBOT[zone]['y'],  ZONE_DOBOT[zone]['z'] + 30, ZONE_DOBOT[zone]['r']]
			
			currentLocation = [PLATEAU[location]['x'], PLATEAU[location]['y'], PLATEAU[location]['z'], PLATEAU[location]['r']]
			currentLocation_up = [PLATEAU[location]['x'], PLATEAU[location]['y'], PLATEAU[location]['z'] + 30, PLATEAU[location]['r']]

			dType.SetPTPCmdEx(self.api, 1, currentZone_up, isQueued=0)
			dType.SetPTPCmdEx(self.api, 2, currentZone, 1)

			dType.SetEndEffectorGripperEx(self.api, 1, 1)
			dType.SetWAITCmdEx(self.api, 0.5, 1)

			dType.SetPTPCmdEx(self.api, 2, currentZone_up, 1)
			dType.SetPTPCmdEx(self.api, 1, currentLocation_up, isQueued=0)
			dType.SetPTPCmdEx(self.api, 2, currentLocation, 1)

			dType.SetEndEffectorGripperEx(self.api, 1, 0)
			dType.SetWAITCmdEx(self.api, 0.5, 1)

			dType.SetEndEffectorGripperEx(self.api, 0, 0)
			dType.SetPTPCmdEx(self.api, 1, self.zoneBase, 1)

			self.roundCount += 1
		
		except Exception as e:
			print("Error occured")
			return False

		return True

	def disconnectDobot(self):
		#Stop to Execute Command Queued
		dType.SetQueuedCmdStopExec(self.api)

		#Disconnect Dobot
		dType.DisconnectDobot(self.api)
