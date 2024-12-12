""" A dictionary holding various header field names to store 4.5D navigation information in the form of: t (utc time), x (longitude), y (latitude), z (depth: below sea level), a (altitude: above seafloor)"""
import os
import json
import copy

myDir = os.path.dirname(os.path.abspath(__file__))
version = {}
with open(os.path.join(myDir,"version.py")) as fp:
    exec(fp.read(), version)
	
version = version['__version__']

apis = {
		'osis_underway':'https://osis.geomar.de/api/v1/',
		'osis_app': 'https://osis.geomar.de/app/'
		}

pos_header = {
		# Field/column name definition for internally handling this kind of t,y,x,z,h position data
		"mariqt":{
			'utc':'utc',		# YYYY-MM-DD HH:ii:ss.sssss+0000 (UTC!!!) -> t-axis
			'lat':'lat',		# Decimal degrees, WGS84 / EPSG4362 -> y-axis
			'lon':'lon',		# Decimal degrees, WGS84 / EPSG4326 -> x-axis
			'dep':'dep',		# Depth of the signal, sample, platform, ... *in the water* -> z-axis, positive when submerged, negative when in air
			'alt':'alt',
			'hgt':'hgt',		# Height above the seafloor -> relative measure!
			'uncert':'uncert' 	# Coorindate uncertainty in standard deviation
		},

		# Definition of field/column names according to the iFDO specification:
		# https://gitlab.hzdr.de/datahub/marehub/ag-videosimages/metadata-profiles-fdos/-/blob/master/MareHub_AGVI_iFDO.md
		"ifdo":{'utc':'image-datetime','lat':'image-latitude','lon':'image-longitude','dep':'image-depth','hgt':'image-meters-above-ground'},

		# Definition of field/column names according to the "Acquisition, Curation and Management Workflow"
		# for marine image data https://www.nature.com/articles/sdata2018181
		"acmw":{'utc':'SUB_datetime','lat':'SUB_latitude','lon':'SUB_longitude','dep':'SUB_depth','hgt':'SUB_distance'},

		# Definition of field/colum names as they occur in a DSHIP export file

		# for RV Sonne posidonia beacons
		"SO_NAV-2_USBL_Posidonia":{1:{'utc':'date time','lat':'USBL.PTSAG.1.Latitude','lon':'USBL.PTSAG.1.Longitude','dep':'USBL.PTSAG.1.Depth'},
									2:{'utc':'date time','lat':'USBL.PTSAG.2.Latitude','lon':'USBL.PTSAG.2.Longitude','dep':'USBL.PTSAG.2.Depth'},
									4:{'utc':'date time','lat':'USBL.PTSAG.4.Latitude','lon':'USBL.PTSAG.4.Longitude','dep':'USBL.PTSAG.4.Depth'},
									5:{'utc':'date time','lat':'USBL.PTSAG.5.Latitude','lon':'USBL.PTSAG.5.Longitude','dep':'USBL.PTSAG.5.Depth'}
		},

		# for RV Sonne itself (GPS)
		"SO_NAV-1_GPS_Saab":{'utc':'date time','lat':'SYS.STR.PosLat','lon':'SYS.STR.PosLon'},


		# for RV Maria S Merian sonardyne beacons
		"MSM_NAV-2_USBL_Sonardyne":{2104:{'utc':'date time','lat':'Ranger2.PSONLLD.2104.position_latitude','lon':'Ranger2.PSONLLD.2104.position_longitude','dep':'Ranger2.PSONLLD.2104.depth'},
									2105:{'utc':'date time','lat':'Ranger2.PSONLLD.2105.position_latitude','lon':'Ranger2.PSONLLD.2105.position_longitude','dep':'Ranger2.PSONLLD.2105.depth'}
		},

		# for RV Maria S Metian itself (GPS)
		"MSM_NAV-1_GPS_Debeg4100":{'utc':'date time','lat':'SYS.STR.PosLat','lon':'SYS.STR.PosLon'},

		# for Meteor
		"MET_NAV-2_USBL_Posidonia":{0:{'utc':'date time','lat':'POSI.PTSAG.0.position_latitude','lon':'POSI.PTSAG.0.position_longitude','dep':'POSI.PTSAG.0.Depth_BUC'},
									1:{'utc':'date time','lat':'POSI.PTSAG.1.position_latitude','lon':'POSI.PTSAG.1.position_longitude','dep':'POSI.PTSAG.1.Depth_BUC'},
									2:{'utc':'date time','lat':'POSI.PTSAG.2.position_latitude','lon':'POSI.PTSAG.2.position_longitude','dep':'POSI.PTSAG.2.Depth_BUC'},
									3:{'utc':'date time','lat':'POSI.PTSAG.3.position_latitude','lon':'POSI.PTSAG.3.position_longitude','dep':'POSI.PTSAG.3.Depth_BUC'},
									4:{'utc':'date time','lat':'POSI.PTSAG.4.position_latitude','lon':'POSI.PTSAG.4.position_longitude','dep':'POSI.PTSAG.4.Depth_BUC'},
		},
		"MET_NAV-1_GPS_C":{'utc':'date time','lat':'SYS.STR.PosLat','lon':'SYS.STR.PosLon'},

		# Definition of field/column names according to the DSM Workbench
		"workbench": {},

		# Definition of field/column names required for assigning EXIF infos to a JPG file
		"exif":{'utc':'CreateDate','lat':'GPSLatitude','lon':'GPSLongitude','dep':'GPSAltitude','hgt':'GPSDestDistance'},

		# Definition of field/column names according to the AWI O2A GeoCSV standard
		# https://confluence.digitalearth-hgf.de/display/DM/O2A+GeoCSV+Format
		# Warning: GeoCSVs need an additional WKT column: geometry [point] with values like: POINT(latitude longitude)
		# Warning: depth and altitude are guessed as i could not find it in the documentation
		"o2a":{'utc':'datetime','lat':'latitude [deg]','lon':'longitude [deg]','dep':'depth [m]','hgt':'altitude [m]'},

		# Definition of field/column names according to the OFOP software
		# Warning: OFOP requires two separate columns for date and time
		# Warning: Depth can also be in column SUB1_USBL_Depth
		# ---- USBL depth kommt vom USBL System, nur depth von einem (online/logging) Drucksensor, manchmal gibt es nur USBL.
		# Warning: It does not have to be SUB1 it can also be SUB2, SUB3, ...
		"ofop":{'utc':'Date\tTime','lat':'SUB1_Lat','lon':'SUB1_Lon','dep':'SUB1_Depth','hgt':'SUB1_Altitude'},

		# Definition of field/column names according to the world data center PANGAEA
		"pangaea":{
				'utc':'DATE/TIME',								# (1599)
				'lat':'LATITUDE',								# (1600)
				'lon':'LONGITUDE',								# (1601)
				'dep':'DEPTH, water [m]',						# (1619)
				'hgt':'Height above sea floor/altitude [m]'		# (27313)
				},

		# Definition of field/column names according to the annotation software BIIGLE
		"biigle":{'utc':'taken_at','lat':'lat','lon':'lng','dep':'gps_altitude','hgt':'distance_to_ground'}

}

att_header = {
	"mariqt":{
			'yaw':'yaw',		# in degrees
			'pitch':'pitch',	# in degrees
			'roll':'roll',		# in degrees
		},
}

navigation_equipment = {
	'SO':{'satellite':'SO_NAV-1_GPS_Saab','underwater':'SO_NAV-2_USBL_Posidonia'},
	'MSM':{'satellite':'','underwater':''}
}

date_formats = {"pangaea":"%Y-%m-%dT%H:%M:%S",
				"mariqt":"%Y-%m-%d %H:%M:%S.%f",
				"mariqt_files":"%Y%m%d_%H%M%S",
				"mariqt_short":"%Y-%m-%d %H:%M:%S",
				"gx_track":"%Y-%m-%dT%H:%M:%SZ",
				"dship":"%Y/%m/%d %H:%M:%S",
				"underway":"%Y-%m-%dT%H:%M:%S.%fZ"}

col_header = {	'pangaea':{'annotation_label':'Annotation label'},
				'mariqt':{	'uuid':'image-uuid',
							'img':'image-filename',
							'utc':'image-datetime',
							'lat':'image-latitude',
							'lon':'image-longitude',
							'dep':'image-depth',
							'hgt':'image-meters-above-ground',
							'alt':'image-altitude-meters',
							'hash':'image-hash-sha256',
							'acqui':'image-acquisition-settings',
							'uncert':'image-coordinate-uncertainty-meters',
							'yaw':'image-camera-yaw-degrees',
							'pitch':'image-camera-pitch-degrees',
							'roll':'image-camera-roll-degrees',
							'pose':'image-camera-pose'
							},
				'exif':{	'img':'SourceFile',
							'uuid':'imageuniqueid'}
}

photo_types = ['jpg','png','bmp','raw','jpeg','tif']
video_types = ['mp4','mov','avi','mts','mkv','wmv']
image_types = photo_types + video_types
unsupportedFileTypes = ["mts",'bmp','raw']

equipment_types = ['CAM','HYA','ENV','NAV','SAM','PFM']

colors = ['#94B242','#24589B','#DCB734','#E7753B','#A0BAAC','#CAD9A0','#82C9EB','#E9DCA6','#ED9A72','#D0DDD6','#EFF5E4','#E6F5FB','#F7F1DC','#F9DED2','#E8EEEB']
color_names = {'entity':'#94B242','process':'#24589B','infrastructure':'#DCB734','missing':'#ED9A72','error':'#E7753B','green':'#94B242','light_green':'#EFF5E4','blue':'#24589B','light_blue':'#E6F5FB','yellow':'#DCB734','light_yellow':'#F7F1DC','red':'#E7753B','light_red':'#F9DED2','grey':'#A0BAAC','light_grey':'#E8EEEB','mid_green':'#CAD9A0','mid_blue':'#82C9EB','mid_yellow':'#E9DCA6','mid_red':'#ED9A72','mid_grey':'#D0DDD6','dark_grey':'#6D7F77',}



############# iFDO ###########################################

_ifdo_schema_file = os.path.join(os.path.join(os.path.join(myDir,'resources'),'fair-marine-images/docs/schemas'),'ifdo-v2.0.1.json')
_provenance_schema_file = os.path.join(os.path.join(os.path.join(myDir,'resources'),'fair-marine-images/docs/schemas'),'provenance-v0.1.0.json')
_annotation_schema_file = os.path.join(os.path.join(os.path.join(myDir,'resources'),'fair-marine-images/docs/schemas'),'annotation-v2.0.0.json')

with open(_provenance_schema_file) as f:
	provenance_schema = json.load(f)
with open(_annotation_schema_file) as f:
	annotation_schema = json.load(f)
with open(_ifdo_schema_file) as f:
	as_str = f.read()
	if provenance_schema['$id']  not in as_str or annotation_schema['$id'] not in as_str:
		raise Exception("procenacen of annotation schema id not found in ifdo schema")
	ifdo_schema = json.loads(as_str)

# store to use local schema files instead of online ones to avoid version conflicts
schema_store = {
    provenance_schema['$id'] : provenance_schema,
    annotation_schema['$id'] : annotation_schema,
}

iFDO_version = ifdo_schema['$id'].split('-')[-1].replace(".json","")


ifdo_schema_reduced_for_field_validation = copy.deepcopy(ifdo_schema)
del ifdo_schema_reduced_for_field_validation['required']
del ifdo_schema_reduced_for_field_validation['properties']['image-set-header']['required']

image_set_header_key = 'image-set-header'
image_set_items_key =  'image-set-items'


# exiftool path in case its not in PATH
global exiftool_path
exiftool_path = ""
def setExiftoolPath(exiftool_path_:str):
	""" Sets the basepath for Exiftool if its not in PATH """
	global exiftool_path
	exiftool_path = exiftool_path_

# verbosity setting
global _verbose
_verbose = True
def setGlobalVerbose(verbose:bool):
	global _verbose
	_verbose = verbose
def getGlobalVerbose():
	global _verbose
	return _verbose
