import datetime
import math
import mariqt.core as miqtc
from abc import ABC, abstractmethod
import cmath
import numpy as np
import pymap3d
import copy
import utm
import statistics
import json

import mariqt.variables as miqtv

class NumDataTimeStamped(ABC):
	""" Abstract class for data in form of a dict with UNIX timestamps in milliseconds as key """
	@abstractmethod
	def interpolateAtTime(self,utc:int,sorted_time_points:list = [] ,startIndex:int = 0):
		pass

	@abstractmethod
	def len(self):
		pass

class Position:
	""" A class defining a 4.5D position, encoded by a utc time (unix in milliseconds), latitude, longitude, depth, height and coordinate uncertainty. Depth, height and coordinate uncertainty are optional."""
	def __init__(self,utc:int,lat:float,lon:float,dep:float=0,hgt:float=-1,uncert:float=-1):
		self.lat = lat
		self.lon = lon
		self.utc = utc
		self.dep = dep
		self.hgt = hgt
		self.uncert = uncert
		# utm 
		self.east = None
		self.north = None
		self.zone = None
		self.Nhemis = None # is northern hemisphere 

	def __eq__(self, other):
		""" Does not compare utc, uncert and utm """
		return self.lat == other.lat and self.lon == other.lon and self.dep == other.dep and self.hgt == other.hgt

	def dateTime(self):
		return datetime.datetime.utcfromtimestamp(self.utc / 1000)

	def __str__(self) -> str:
		return "utc: " + str(self.dateTime()) + ", lat: " + str(self.lat) + ", lon: " + str(self.lon) + ", dep: " + str(self.dep) + ", hgt: " + str(self.hgt) + ", uncert: " + str(self.uncert)

	def containsNoneValue(self):
		if self.lat is None or self.lon is None or self.dep is None or self.hgt is None or self.uncert is None:
			return True
		return False

	def cotainsNoneValuesInRequiredFields(self):
		if self.lat is None or self.lon is None or self.dep is None:
			return True
		return False

	def calculateUTM(self):
		self.east,self.north,self.zone,self.Nhemis = latLon2utm(self.lat,self.lon)

class Positions(NumDataTimeStamped):
	""" A class that holds several 4.5D Positions in the form of a dictionary with UNIX timestamps in milliseconds as keys and containing (x,y,z,d,h) tuples. Decorator pattern of a dictionary"""

	def __init__(self,positions=None):
		if positions is None:
			positions = {}
		self.positions = positions
		self.__clearNoneCleandValueLists()
	def setPos(self,p:Position):
		self.positions[p.utc] = p
		self.__clearNoneCleandValueLists()
	def setVals(self,utc:int,lat:float,lon:float,dep:float=0,hgt:float=-1,uncert:float=-1):
		self.positions[utc] = Position(utc,lat,lon,dep,hgt,uncert)
		self.__clearNoneCleandValueLists()
	def remUTC(self,utc:int):
		del self.positions[utc]
		self.__clearNoneCleandValueLists()
	def remPos(self,p:Position):
		del self.positions[p.utc]
		self.__clearNoneCleandValueLists()
	def len(self):
		return len(self.positions)
	def __getitem__(self,utc:int):
		return self.positions[utc]
	def __setitem__(self,utc:int,p:Position):
		self.positions[utc] = p
		self.__clearNoneCleandValueLists()
	def keys(self):
		return self.positions.keys()

	def __str__(self):
		return str("\n".join([str(self.positions[e]) for e in self.positions]))

	def invert_lat(self):
		for pos in self.positions.values():
			pos.lat *= -1

	def invert_lon(self):
		for pos in self.positions.values():
			pos.lon *= -1

	def invert_dep(self):
		for pos in self.positions.values():
			pos.dep *= -1

	def invert_hgt(self):
		for pos in self.positions.values():
			pos.hgt *= -1

	
	def interpolateNones(self):
		""" fills None values by interpolation """

		time_points = list(self.positions.keys())
		sorted_time_points = copy.deepcopy(time_points)
		for utc in time_points:
			if self.positions[utc].lat is None and self.positions[utc].lon is None and self.positions[utc].dep is None and (self.positions[utc].hgt is None or self.positions[utc].hgt == -1):
				self.remUTC(utc)
				sorted_time_points.remove(utc)
		sorted_time_points.sort()

		startIndex = 0
		for utc in sorted_time_points:
			newPos, past_nearest_index = self.interpolateAtTime(utc,sorted_time_points,startIndex)
			self.positions[utc] = newPos
			startIndex = past_nearest_index

		time_points = list(self.positions.keys())
		for utc in time_points:
			if self.positions[utc].lat is None or self.positions[utc].lon is None or self.positions[utc].dep is None:
				print("deleted: ", self.positions[utc])
				self.remUTC(utc)

	def __fillNoneCleandValueLists(self,sorted_time_points):
		""" inits None cleaned value time point lists  """
		self.noneCleandTimePoints_lat = [t for t in sorted_time_points if not self.positions[t].lat is None]
		self.noneCleandTimePoints_lon = [t for t in sorted_time_points if not self.positions[t].lon is None]
		self.noneCleandTimePoints_dep = [t for t in sorted_time_points if not self.positions[t].dep is None]
		self.noneCleandTimePoints_hgt = [t for t in sorted_time_points if not self.positions[t].hgt is None]
		self.noneCleandTimePoints_uncert = [t for t in sorted_time_points if not self.positions[t].uncert is None]

	def __clearNoneCleandValueLists(self):
		self.noneCleandTimePoints_lat = []
		self.noneCleandTimePoints_lon = []
		self.noneCleandTimePoints_dep = []
		self.noneCleandTimePoints_hgt = []
		self.noneCleandTimePoints_uncert = []
	
	def interpolateAtTime(self,utc:int,sorted_time_points:list = [] ,startIndex:int = 0):
		""" returns pos_interpolated, lastIndex """

		if utc in self.positions and not self.positions[utc].containsNoneValue():
			return self.positions[utc], startIndex

		if sorted_time_points == []:
			sorted_time_points = list(self.positions.keys())
			sorted_time_points.sort()

		if len(self.noneCleandTimePoints_lat) == 0:
			self.__fillNoneCleandValueLists(sorted_time_points)

		# lat
		alpha,pre_utc,post_utc,past_nearest_index = self.getAlpha(self.noneCleandTimePoints_lat,utc,startIndex)
		if alpha is None:
			new_lat = None
		else:
			new_lat = self.positions[pre_utc].lat * (1-alpha) + self.positions[post_utc].lat * alpha

		# lon
		alpha,pre_utc,post_utc,past_nearest_index = self.getAlpha(self.noneCleandTimePoints_lon,utc,past_nearest_index)
		if alpha is None:
			new_lon = None
		else:	
			new_lon = self.positions[pre_utc].lon * (1-alpha) + self.positions[post_utc].lon * alpha

		# dep
		alpha,pre_utc,post_utc,past_nearest_index = self.getAlpha(self.noneCleandTimePoints_dep,utc,past_nearest_index)
		if alpha is None:
			new_dep = None
		else:
			new_dep = self.positions[pre_utc].dep * (1-alpha) + self.positions[post_utc].dep * alpha

		# hgt
		alpha,pre_utc,post_utc,past_nearest_index = self.getAlpha(self.noneCleandTimePoints_hgt,utc,past_nearest_index)
		if alpha is None:
			new_hgt = None
		else:
			new_hgt = self.positions[pre_utc].hgt * (1-alpha) + self.positions[post_utc].hgt * alpha

		# uncert
		alpha,pre_utc,post_utc,past_nearest_index = self.getAlpha(self.noneCleandTimePoints_uncert,utc,past_nearest_index)
		if alpha is None:
			new_uncert = None
		else:
			new_uncert = self.positions[pre_utc].uncert * (1-alpha) + self.positions[post_utc].uncert * alpha # TODO uncert? siehe navigation.splineToOneSecondInterval()

		return Position(utc,new_lat,new_lon,new_dep,new_hgt,new_uncert), past_nearest_index

	def getAlpha(self,sorted_time_points,utc,startIndex):
		""" returns None if utc out of range """
		try:
			prev_nearest_index, past_nearest_index = findNearestNeighbors(sorted_time_points,utc,startIndex)
		except FindNearestNeighborsException:
			return None,utc,utc,startIndex
		pre_utc = sorted_time_points[prev_nearest_index]
		try:
			post_utc = sorted_time_points[past_nearest_index]
		except Exception as e:
			print(past_nearest_index)
			raise e
		alpha = 1.0 * (utc - pre_utc) / (post_utc - pre_utc)
		return alpha,pre_utc,post_utc,past_nearest_index


	def checkPositionsContent(self):
		""" Check whether all nav data of one col are equal or empty.
		Returns seven booleans: lat_identical,lon_identical,dep_identical,hgt_identical,dep_not_zero,hgt_not_zero,uncert_not_zero."""

		lat_identical = True
		lon_identical = True
		dep_identical = True
		hgt_identical = True
		dep_not_zero = False
		hgt_not_zero = False
		uncert_not_zero = False
		for i,utc in enumerate(self.positions):
			if i > 0:
				if prev_lat != self.positions[utc].lat:
					lat_identical = False
				if prev_lon != self.positions[utc].lon:
					lon_identical = False
				if prev_dep != self.positions[utc].dep:
					dep_identical = False
				if prev_hgt != self.positions[utc].hgt:
					hgt_identical = False
			if self.positions[utc].dep != 0:
				dep_not_zero = True
			if self.positions[utc].hgt != -1:
				hgt_not_zero = True
			if self.positions[utc].uncert > 0:
				uncert_not_zero = True
			prev_lat = self.positions[utc].lat
			prev_lon = self.positions[utc].lon
			prev_dep = self.positions[utc].dep
			prev_hgt = self.positions[utc].hgt
		return lat_identical,lon_identical,dep_identical,hgt_identical,dep_not_zero,hgt_not_zero,uncert_not_zero

	def calculateUTM(self):
		for utc in self.positions:
			self.positions[utc].calculateUTM()

	def write2File(self,file,ignoreUTM=False):
		""" Writes positions to tab separated file """

		# Check whether depth and height are set
		lat_identical, lon_identical, dep_identical, hgt_identical, dep_not_zero, hgt_not_zero,uncert_not_zero = self.checkPositionsContent()

		# check UTM
		hasUTM = False
		if not ignoreUTM:
			for utc in self.positions:
				if not self.positions[utc].east is None:
					hasUTM = True
					break

		# Write to navigation txt file
		# header
		res = open(file, "w")
		res.write(miqtv.col_header['mariqt']['utc'])
		res.write("\t"+miqtv.col_header['mariqt']['lat'])
		res.write("\t"+miqtv.col_header['mariqt']['lon'])
		if dep_not_zero:
			res.write("\t"+miqtv.col_header['mariqt']['dep'])
		if hgt_not_zero:
			res.write("\t"+miqtv.col_header['mariqt']['hgt'])
		if uncert_not_zero:
			res.write("\t"+miqtv.col_header['mariqt']['uncert'])
		if hasUTM:
			res.write("\t"+'easting'+"\t"+'northing'+"\t"+'zone'+"\t"+'isNorthernHemisphere')
		res.write("\n")
		# data lines
		for utc in self.positions:
			res.write(datetime.datetime.fromtimestamp(utc / 1000,tz=datetime.timezone.utc).strftime(miqtv.date_formats['mariqt'])) 
			res.write("\t"+str(self.positions[utc].lat))
			res.write("\t"+str(self.positions[utc].lon))
			if dep_not_zero:
				res.write("\t"+str(self.positions[utc].dep))
			if hgt_not_zero:
				res.write("\t"+str(self.positions[utc].hgt))
			if uncert_not_zero:
				res.write("\t"+str(self.positions[utc].uncert))
			if hasUTM:
				res.write("\t"+str(self.positions[utc].east)+"\t"+str(self.positions[utc].north)+"\t"+str(self.positions[utc].zone)+"\t"+str(self.positions[utc].Nhemis))
			res.write("\n")
		res.close()


	def toGeoJson(self, collectionName:str):
		""" returns geojson dict """
		lat_identical, lon_identical, dep_identical, hgt_identical, dep_not_zero, hgt_not_zero,uncert_not_zero = self.checkPositionsContent()
		geojson = {'type': 'FeatureCollection', 'name': collectionName, 'features': []}
		for utc in self.positions:
			if dep_not_zero:
				geometry =  {'type': "Point", 'coordinates': 
								[self.positions[utc].lon, self.positions[utc].lat, self.positions[utc].dep]
							}
			else:
				geometry =  {'type': "Point", 'coordinates': 
								[self.positions[utc].lon, self.positions[utc].lat]
							}
			if True in [math.isnan(x) for x in geometry['coordinates']]:
				continue

			geojson['features'].append({'type': 'Feature', 'properties': {'id': datetime.datetime.fromtimestamp(utc / 1000,tz=datetime.timezone.utc).strftime(miqtv.date_formats['mariqt'])}, 'geometry': geometry })

		return geojson


	def toGeoJsonFile(self, collectionName:str, file:str):
		""" writes to geojson file """
		o = open(file,"w", errors="ignore", encoding='utf-8')
		json.dump(self.toGeoJson(collectionName), o, ensure_ascii=False, indent=4)
		o.close()


class Attitude:
	""" A class defining an attitude, encoded by a utc time (unix in milliseconds) and yaw, pitch, roll in degrees which are by default 0."""
	def __init__(self,utc:int,yaw:float=0,pitch:float=0,roll:float=0):
		self.utc = utc
		try:
			self.yaw = float(yaw)
		except Exception as ex:
			if yaw is None:
				self.yaw = None
			else:
				raise ex
		try:
			self.pitch = float(pitch)
		except Exception as ex:
			if pitch is None:
				self.pitch = None
			else:
				raise ex
		try:
			self.roll = float(roll)
		except Exception as ex:
			if roll is None:
				self.roll = None
			else:
				raise ex

	def dateTime(self):
		return datetime.datetime.utcfromtimestamp(self.utc / 1000)

	def __eq__(self, __o: object) -> bool:
		if self.yaw == __o.yaw and self.pitch == __o.pitch and self.roll == __o.roll:
			return True
		return False

	def __str__(self) -> str:
		return "utc: " + str(self.dateTime()) + ", yaw: " + str(self.yaw) + ", pitch: " + str(self.pitch) + ", roll: " + str(self.roll)

	def containsNoneValue(self):
		if self.yaw is None or self.pitch is None or self.roll is None:
			return True
		return False

	def cotainsNoneValuesInRequiredFields(self):
		return False

class Attitudes(NumDataTimeStamped):
	""" A class that holds several Attitudes in the form of a dictionary with UNIX timestamps in milliseconds as keys and containing (yaw,pitch,roll) tuples. Decorator pattern of a dictionary"""

	def __init__(self,attitudes={}):
		self.attitudes = attitudes
		self.__clearNoneCleandValueLists()
	def setAtt(self,a:Attitude):
		self.attitudes[a.utc] = a
		self.__clearNoneCleandValueLists()
	def setVals(self,utc:int,yaw:float=0,pitch:float=0,roll:float=0):
		self.attitudes[utc] = Attitude(utc,yaw,pitch,roll)
		self.__clearNoneCleandValueLists()
	def remUTC(self,utc:int):
		del self.attitudes[utc]
		self.__clearNoneCleandValueLists()
	def remAtt(self,a:Attitude):
		del self.attitudes[a.utc]
		self.__clearNoneCleandValueLists()
	def len(self):
		return len(self.attitudes)
	def __getitem__(self,utc:int):
		return self.attitudes[utc]
	def __setitem__(self,utc:int,a:Attitude):
		self.attitudes[utc] = a
		self.__clearNoneCleandValueLists()
	def keys(self):
		return self.attitudes.keys()

	def __str__(self):
		return str("\n".join([str(self.attitudes[e]) for e in self.attitudes]))

	def __fillNoneCleandValueLists(self,sorted_time_points):
		""" inits None cleaned value time point lists  """
		# here it's assumed yaw, pitch and roll come from same record so they are not checked separatelys for None entries
		self.noneCleandTimePoints_att = [t for t in sorted_time_points if not self.attitudes[t].containsNoneValue()]

	def __clearNoneCleandValueLists(self):
		self.noneCleandTimePoints_att = []

	def invert_yaw(self):
		for att in self.attitudes.values():
			att.yaw *= -1

	def invert_pitch(self):
		for att in self.attitudes.values():
			att.pitch *= -1

	def invert_roll(self):
		for att in self.attitudes.values():
			att.roll *= -1

	def interpolateAtTime(self,utc:int,sorted_time_points:list = None ,startIndex:int = 0):
		""" returns att_interpolated, lastIndex """

		if utc in self.attitudes and not self.attitudes[utc].containsNoneValue():
			return self.attitudes[utc], startIndex

		if sorted_time_points is None:
			sorted_time_points = list(self.attitudes.keys())
			sorted_time_points.sort()

		if len(sorted_time_points) == 0 or utc < sorted_time_points[0] or utc >  sorted_time_points[-1]:
			return Attitude(utc,None,None,None), startIndex

		if len(self.noneCleandTimePoints_att) == 0:
			self.__fillNoneCleandValueLists(sorted_time_points)

		try:
			prev_nearest_index, past_nearest_index = findNearestNeighbors(self.noneCleandTimePoints_att,utc,startIndex)
		except FindNearestNeighborsException:
			return Attitude(utc,None,None,None), startIndex 
		pre_utc = self.noneCleandTimePoints_att[prev_nearest_index]
		post_utc = self.noneCleandTimePoints_att[past_nearest_index]

		new_yaw = interpolateAngles(pre_utc,self.attitudes[pre_utc].yaw,utc,post_utc,self.attitudes[post_utc].yaw,anglesInDegrees=True)
		new_pitch = interpolateAngles(pre_utc,self.attitudes[pre_utc].pitch,utc,post_utc,self.attitudes[post_utc].pitch,anglesInDegrees=True)
		new_roll = interpolateAngles(pre_utc,self.attitudes[pre_utc].roll,utc,post_utc,self.attitudes[post_utc].roll,anglesInDegrees=True)

		return Attitude(utc,new_yaw,new_pitch,new_roll), past_nearest_index 

class AngularInterpolater():
	""" Allows for interpolation of angular values via .interpolateAt(). source_t must be list of floats. 
		Angular quantities can not be simply interpolated (e.g. middle of 175 and -175 would be zero but should be 180).
		This class handles such cases properly """

	def __init__(self,source_t:list,source_x:list,source_t_is_sorted=False,anglesInDegrees=True):
		""" Allows for interpolation of angular values via .interpolateAt(). source_t must be list of floats. 
		 	Angular quantities can not be simply interpolated (e.g. middle of 175 and -175 would be zero but should be 180).
			This class handles such cases properly """
		if len(source_t) != len(source_x):
			raise Exception("AngularInterpolater: time and data vector must be of same length!")

		self.source_dict = dict(zip(source_t, source_x))
		self.anglesInDegrees = anglesInDegrees

		if not source_t_is_sorted:
			self.source_t_sorted = copy.deepcopy(source_t)
			self.source_t_sorted.sort()
		else:
			self.source_t_sorted = source_t

		self.startIndex = 0

	def interpolateAt(self,target_t:float):

		if target_t in self.source_dict:
			return self.source_dict[target_t]

		prev_nearest_index, past_nearest_index = findNearestNeighbors(self.source_t_sorted ,target_t,self.startIndex)
		
		pre_target_t = self.source_t_sorted[prev_nearest_index]
		post_target_t = self.source_t_sorted[past_nearest_index]

		# set start for next interpolation
		self.startIndex = past_nearest_index

		return interpolateAngles(pre_target_t,self.source_dict[pre_target_t],target_t,post_target_t,self.source_dict[post_target_t],anglesInDegrees=self.anglesInDegrees)


def interpolateAngles(t_pre:float,x_pre:float,t_target:float,t_post:float,x_post:float,anglesInDegrees=True):
	""" interpolates angle at t_target between to angles x_pre and x_post, with respective times t_pre and t_post"""
	if x_pre is None or x_post is None:
		return None
	if anglesInDegrees:
		x_pre = math.radians(x_pre)
		x_post = math.radians(x_post)

	alpha = 1.0 * (t_target - t_pre) / (t_post - t_pre)
	# angular quantities can not be simply interpolated (e.g. middle of 175 and -175 would be zero but should be 180), therefore angular values α are applied as arguments of unit complex numbers
	# e^jα . The resulting complex numbers can then, if necessary, be weighted by ω, added together and the phase of the result provides a valid mean/interpolation
	target_x = cmath.phase( cmath.exp(complex(0,x_pre)) * (1-alpha) + cmath.exp(complex(0,x_post))  * alpha )

	# try to get same sign (interpolationm might add an irrelevant 360 degrees offset)
	if x_pre - target_x > 3:
		target_x += 2*math.pi
	elif x_pre - target_x < -3:
		target_x -= 2*math.pi
	if anglesInDegrees:
		target_x = math.degrees(target_x)
	return target_x

class FindNearestNeighborsException(Exception):
	""" Exception type purely related to iFDO issues """
	pass

# TODO move to core?
def findNearestNeighbors(values_sorted:list,value, startIndex):
	""" returns prev_nearest_index, past_nearest_index of value in values starting the search at startIndex. Throws exception if value out of range"""

	if len(values_sorted) == 0 or value < values_sorted[0] or value > values_sorted[-1]:
		raise FindNearestNeighborsException("value " + str(value) + " out of range")

	if startIndex < 0:
		startIndex = 0
	if startIndex >= len(values_sorted):
		startIndex = len(values_sorted) -1

	if values_sorted[startIndex] == value:
		if startIndex == 0:
			return startIndex,startIndex+1
		else:
			return startIndex-1,startIndex
	if values_sorted[startIndex] < value:
		increment = 1
		limit = len(values_sorted)
		def passed(value1,value2):
			return value1 >= value2
	else:
		increment = -1
		limit = -1
		def passed(value1,value2):
			return value1 <= value2

	for i in range(startIndex,limit,increment):
		if passed(values_sorted[i],value):
			if increment == 1:
				return i-1, i
			else:
				return i, i+1
	raise Exception("something went wrong")


def distanceLatLon(lat_1,lon_1,lat_2,lon_2):
	""" Computes a distance in meters from two given decimal lat/lon values."""

	lat_1_r = math.radians(lat_1)
	lon_1_r = math.radians(lon_1)
	lat_2_r = math.radians(lat_2)
	lon_2_r = math.radians(lon_2)

	lat_offset = lat_1_r - lat_2_r
	lon_offset = lon_1_r - lon_2_r

	alpha = 2 * math.asin(math.sqrt(math.pow(math.sin(lat_offset / 2), 2) + math.cos(lat_1_r) * math.cos(lat_2_r) * math.pow(math.sin(lon_offset / 2), 2)))
	return alpha * 6371000 # Earth's radius


def distancePositions(p1:Position,p2:Position):
	""" Computes a distance in meters from two given positions"""
	return distanceLatLon(p1.lat,p1.lon,p2.lat,p2.lon)


def getDecDegCoordinate(val):
	""" Asserts that the given value is a decimal degree float value"""
	if isinstance(val, float):
		return val
	else:
		return decmin2decdeg(val)


def decdeg2decmin(val,xy = ""):
	""" Turns a float representation of a coordinate (lat/lon) into a string representation using decimal minutes"""
	if val < 0:
		dec = math.ceil(val)
		if xy == "lat":
			xy = "S"
			dec *= -1
			val *= -1
		elif xy == "lon":
			xy = "W"
			dec *= -1
			val *= -1
	else:
		dec = math.floor(val)
		if xy == "lat":
			xy = "N"
		elif xy == "lon":
			xy = "E"
	min = str(round(60*(val - dec),3))
	add = ""
	for i in range(len(min[min.find(".")+1:]),3):
		add += "0"
	return str(dec)+"°"+min+add+xy


def decmin2decdeg(str):
	""" Converts a decimal degree string ("117° 02.716' W") to a decimal degree float"""
	str = str.strip()
	try:
		return float(str)
	except:
		p1 = str.find(chr(176))# This is an ISO 8859-1 degree symbol: °
		p2 = str.find(chr(39))# This is a single tick: '
		deg = int(str[0:p1].strip())
		min = float(str[p1+1:p2].strip())
		reg = str[p2+1:].strip()

		if reg.lower() == "s" or reg.lower() == "w":
			deg *= -1
			return deg - min/60
		else:
			return deg + min/60

def Rx(angle:float):
    """ Rotation matrix around x, take angle in degrees """
    c = np.cos(np.deg2rad(angle))
    s = np.sin(np.deg2rad(angle))
    return np.array([   [1, 0, 0],
                        [0, c,-s],
                        [0, s, c]])

def Ry(angle:float):
    """ Rotation matrix around y, take angle in degrees """
    c = np.cos(np.deg2rad(angle))
    s = np.sin(np.deg2rad(angle))
    return np.array([   [c, 0, s],
                        [0, 1, 0],
                        [-s,0, c]])

def Rz(angle:float):
    """ Rotation matrix around z, take angle in degrees """
    c = np.cos(np.deg2rad(angle))
    s = np.sin(np.deg2rad(angle))
    return np.array([   [c,-s, 0],
                        [s, c, 0],
                        [0, 0, 1]])

def R_YawPitchRoll(yaw,pitch,roll):
    """ return yaw pitch roll rotation matrix, takes angle in degrees """
    return np.dot(Rz(yaw),Ry(pitch)).dot(Rx(roll))

def R_XYZ(angle_x,angle_y,angle_z):
    """ return rotation matrix for consecutive rotations around fixed axis x,y,z"""
    return np.dot(Rz(angle_z),Ry(angle_y)).dot(Rx(angle_x))

def yawPitchRoll(R:np.array):
    """ retruns [yaw,pitch,roll] in degrees from yaw,pitch,roll rotation matrix """
    yaw = np.degrees(np.arctan2(R[1,0],R[0,0]))
    pitch = np.degrees(np.arctan2(-R[2,0],np.sqrt(R[2,1]**2 + R[2,2]**2)))
    roll = np.degrees(np.arctan2(R[2,1],R[2,2]))
    return [yaw,pitch,roll]


def addLeverarms2LatLonDepAlt(orig_lat,orig_lon,orig_depth,orig_alt,offset_x,offset_y,offest_z,yaw,pitch,roll):
	""" 
	Adds and offest in vehicle coordinates to an original lat, lon, depth(downward positive), altitude position (wgs84)
	and returns new lat, lon, depth, alt. altitude has no influence on results and can be set to anything/ignored if not needed. 
	Angles in degrees, offsets in meters 
	"""

	# get offest in NED
	offest_xyz = np.array([offset_x,offset_y,offest_z])
	offset_NED = R_YawPitchRoll(yaw,pitch,roll).dot(offest_xyz)

	try:
		ell = pymap3d.Ellipsoid.from_name("wgs84")
	except AttributeError:
		# pymap3d 2.x support
		ell = pymap3d.Ellipsoid("wgs84")
	lat_lon_h_new =  pymap3d.ned2geodetic(offset_NED[0], offset_NED[1], offset_NED[2],orig_lat,orig_lon,-orig_depth,ell=ell)
	lat_new = lat_lon_h_new[0]
	lon_new = lat_lon_h_new[1]
	depth_new = -lat_lon_h_new[2]
	alt_new = orig_alt - (depth_new - orig_depth)

	return lat_new, lon_new, depth_new, alt_new


def writeSimpleUtmWorldFile(outputFile:str,easting:float,northing:float,zone:int,IsNorthernHemisphere:bool,imageWidth:int,imageHeight:int,heading:float,altitude:float,focalLenghPixelsX:float,focalLenghPixelsY:float):
	"""
	Writes a simple world file with UTM coordinates assuming the camera looks straight down, the principal point is in the center of the image and quadratic pixels
	* altitude in meters
	* focal length in pixels
	* heading in degrees
	"""

	pixelSizeHorizontal = altitude/focalLenghPixelsX
	pixelSizeVertical = altitude/focalLenghPixelsY

	principal_x = (imageWidth - 1) / 2
	principal_y = (imageHeight - 1) / 2

	hemisphere = 'S'
	if IsNorthernHemisphere:
		hemisphere = 'N'

	cosalpha = math.cos(heading / 180.0 * math.pi)
	sinalpha = math.sin(heading / 180.0 * math.pi)

	a11 = pixelSizeHorizontal * cosalpha
	a21 = (-1.0) * pixelSizeVertical * sinalpha
	a12 = (-1.0) * pixelSizeHorizontal * sinalpha
	a22 = (-1.0) * pixelSizeVertical * cosalpha

	# the world file specifies the coordinate of the top left corner
    # but lat/lon refers to the principal point (or image center), so we have to correct this
	x = easting - a11*principal_x - a12*principal_y
	y = northing - a21*principal_x - a22*principal_y

	# write a comment line just for us which coordinate system is used (ignored by GIS)
	comment = "#This file refers to UTM zone " + str(zone).zfill(2) + hemisphere

	f = open(outputFile, "w")
	f.write(str(a11) + "\n")
	f.write(str(a21) + "\n")
	f.write(str(a12) + "\n")
	f.write(str(a22) + "\n")
	f.write(str(x) + "\n")
	f.write(str(y) + "\n")
	f.write(str(comment) + "\n")
	f.close()

def convertImageNameToWorldFileName(imagefilename:str):
    # replaces next to last char with last char and last char with "w"
	extPontIndex = imagefilename.rfind('.')
	ext = imagefilename[extPontIndex+1::]
	wldExt = ext[:-2] + ext[-1] + 'w'
	#wldExt[-2] = wldExt[-1]
	#wldExt[-1] = 'w'

	return imagefilename[0:extPontIndex] + '.' + wldExt


def latLon2utm(lat:float,lon:float, ellps='WGS84'):
	""" returns easting,norting,zone:int,isNortherHemisphere:bool """
	utmx, utmy, zone, zl_2 = utm.from_latlon(lat,lon)
	isNortherHemisphere = True
	if lat<0:
		isNortherHemisphere = False
	return utmx,utmy,zone,isNortherHemisphere


def median2D(x_:list,y_:list,maxIteratinos = 1000,TerminationTolerance = 0.000001):
	""" Calculates geometric median. Returns [median_x,median_y],terminationCriterion"""
	if len(x_) != len(y_):
		raise Exception("median2D: x and y must have the same dimensions")
	if len(x_) == 1:
		return [x_[0],y_[0]], "only one point, nothing to smooth"
	if len(x_) == 0:
		raise Exception("median2D: no points provided")
	x = [np.array([x_[i],y_[i]]) for i in range(len(x_))]

	# mean values as starting estimation of geomedian
	estimation = np.array([statistics.mean(x_),statistics.mean(y_)])
	#Vector newEstimation;
	# iteration
	terminationCriterion = "maxIteratinos"
	for i in range(maxIteratinos):
		dividend = np.array([0.0,0.0])
		divisor = 0.0
		R = np.array([0.0,0.0])
		vardi = 0.0; # marker for vardi modification

		# going through sample points
		for j in range(len(x)):

			# check that current point is not equal to current estimate
			current = x[j]
			if not (estimation == current).all():
				distance = current - estimation
				magnDistance = np.linalg.norm(distance)
				dividend = dividend + (current / magnDistance)
				divisor = divisor + (1.0 / magnDistance)
				R = R + distance / magnDistance
			else:
				vardi = 1.0
		if R[0] == 0.0 and R[1] == 0.0:
			R[0] = 0.0000001
		if vardi == 0.0:
			newEstimation = dividend / divisor
		else:
			if divisor == 0.0: # estimation equals ALL sample points
				newEstimation = estimation
			else:
				magnR = np.linalg.norm(R)
				compare1 = [0.0, (1.0 - (vardi / magnR)) ]
				compare2 = [ 1.0, (vardi / magnR) ]
				newEstimation = max(compare1) * dividend / divisor + min(compare2) * estimation

		# stop iteration when termination accuracy is reached
		if abs(estimation[0] - newEstimation[0]) < TerminationTolerance and abs(estimation[1] - newEstimation[1]) < TerminationTolerance:
			estimation = newEstimation
			terminationCriterion = "TerminationTolerance"
			break
		estimation = newEstimation
	x_median = estimation[0]
	y_median = estimation[1]
	return [x_median,y_median], terminationCriterion
