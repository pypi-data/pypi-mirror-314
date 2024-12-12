""" This file contains various validation functions to check whether given parameters adhere to the MareHub AG V/I conventions"""

import os
import datetime
import copy
import packaging
import importlib.metadata
import jsonschema
# referencing is not compatible with pdflatex, they want different versions of attr as of okt. 2023
if packaging.version.parse(importlib.metadata.version("jsonschema")) >= packaging.version.parse("4.18.0"):
	import referencing

import mariqt.variables as miqtv
import mariqt.directories as miqtd
import mariqt.core as miqtc
import mariqt.image as miqti


# def isValidPerson(o:dict,msg=[]):
# 	""" Checks whether the dict contains the fields needed to identify a person"""
# 	if not isinstance(o,dict):
# 		msg.append("person is not a dict")
# 		return False
# 	req = miqtv.req_person_fields
# 	for r in req:
# 		if not r in o or o[r] == "":
# 			continue
		
# 		if r == "email" and not isValidEmail(o[r]):
# 			msg.append("invalid email")
# 			return False
# 		if r == "orcid" and not isValidOrcid(o[r]):
# 			msg.append("invalid orcid")
# 			return False
# 	return True

def validate_ifdo(ifdo:dict,short_msg=True):
	""" Validate ifdo against schema 
	Returns valid:bool, message:str """
	return validate_against_schema(ifdo,schema=miqtv.ifdo_schema,short_msg=short_msg,store=miqtv.schema_store)


def validate_against_schema(obj:dict,schema:dict,short_msg=True, store=None):
	""" validate ifdo aginst json schema.
	Returns valid:bool, message:str """
	try:
		if store is None:
			jsonschema.validate(instance=obj, 
								schema=schema,
								format_checker= jsonschema.FormatChecker())
			return True, ''

		else:
			jsonschema_version = importlib.metadata.version("jsonschema") #jsonschema.__version__
			# since version 4.18
			if packaging.version.parse(jsonschema_version) >= packaging.version.parse("4.18.0"):
				resources = []
				for id in store:
					schema_ = referencing.Resource.from_contents(store[id])
					resources.append((miqtc.assertSlash(id),schema_))
				
				registry = referencing.Registry().with_resources(resources)
				jsonschema.validate(instance=obj, 
									schema=schema,
									format_checker= jsonschema.FormatChecker(),
									registry=registry)
			else:
				# till 4.17
				resolver = jsonschema.RefResolver.from_schema(schema,store=store)
				jsonschema.validate(instance=obj, 
									schema=schema,
									format_checker= jsonschema.FormatChecker(),
									resolver=resolver)
			return True, ''
	except jsonschema.ValidationError as ex:
		if short_msg:
			msg = ' -> '.join([str(e) for e in list(ex.path)]) + ": " + str(ex)[0:str(ex).find("\n\n")]
		else:
			msg = str(ex)
		#print(ex)
		return False, msg


# check jsonschema'[format]' is installed
is_uri, msg = validate_against_schema("a",{"type": "string","format": "uri"})
if is_uri:
	raise ModuleNotFoundError("It looks like jsonschema[format] is not installed. Please install (e.g. pip install jsonschema[format]), otherwise jsonschema validation will be incomplete!")


def isValidDatapath(path:str):
	""" Check whether a path leads to a proper leaf data folder (raw, processed, etc.)"""
	try:
		d = miqtd.Dir(path)
		return d.validDataDir()
	except:
		return False


def isValidEventName(event:str):
	""" Check whether an event name follows the conventions: `<project>[-<project part>]_<event-id>[-<event-id-index>][_<device acronym>]` """
	tmp = event.split("_")
	if len(tmp) < 2 or len(tmp) > 3:
		return False
	tmp2 = tmp[0].split("-")
	if len(tmp2) == 2:
		try:
			int(tmp2[1])
		except:
			return False

	tmp2 = tmp[1].split("-")
	if len(tmp2) == 1:
		try:
			int(tmp2[0])
		except:
			return False
	elif len(tmp2) == 2:
		try:
			int(tmp2[0])
			int(tmp2[1])
		except:
			return False
	else:
		return False
	return True


def isValidEquipmentID(eqid:str):
	""" Check whether an equipment id follows the convention: <owner>_<type>-<type index[_<subtype>[_<name>]]>"""
	eq = eqid.split("_")
	if len(eq) < 2:
		print("too short")
		return False
	eq2 = eq[1].split("-")
	if len(eq2) != 2:
		print("second too short")
		return False
	try:
		int(eq2[1])
	except:
		print("second second no int")
		return False
	if eq2[0] not in miqtv.equipment_types:
		print(eq2[0],"not in eq types")
		return False
	return True


def isValidImageName(name:str):
	""" Check whether an image filename adheres to the convention: <event>_<sensor>_<date>_<time>.<ext>.
		Returns [valid:bool,msg:str] """
	event, sensor = miqti.parseImageFileName(name)
	if event == "" and sensor == "":
		return [False, "invalid equipment type, could not parse image file name"]
	
	# check if from field before sensor part till timestamp is valid equipment id (e.g. GMR_CAM-12)
	if not isValidEquipmentID(sensor):
		return [False, "\'" + sensor + "\' is not a valid equipment id"]

	if not isValidEventName(event):
		return [False, "\'" + event + "\' is not a valid event name"]

	# check if file extension in miqtv.image_types
	tmp = name.split("_")
	pos = tmp[-1].rfind(".")
	ext = tmp[-1][pos+1:].lower()
	if not ext in miqtv.image_types:
		return [False, "\'" + ext + "\'  is not a valid image type"]


	try:
		miqtc.parseFileDateTimeAsUTC(name)
	except:
		return [False,"cannot parse date time"]

	return [True, ""]


def is_valid_ifdo_field(field_name:str,field_value):
	""" Check field and throw IfdoException if invalid. 
	To iterate over many fields its much faster to use are_valid_ifdo_fields """
	# fake ifdo with field in header since item part schema validation does not return nice error message but only
	# 'not valid under any of the given schemas' cuz of oneOf
	item_test_ifdo = {'image-set-header':{field_name: field_value}}
	valid, msg = validate_against_schema(item_test_ifdo,miqtv.ifdo_schema_reduced_for_field_validation,short_msg=True,store=miqtv.schema_store)
	if not valid:
		raise miqtc.IfdoException(field_name,"invalid:",msg)

	# additional checks
	ifdo_field_additional_checks(field_name,field_value)


def ifdo_field_additional_checks(field_name:str,field_value):
	""" Run checks additional to schema validation. Throw IfdoException if invalid. """
	# additional checks
	if field_name in ['image-filename']:
		if not isValidImageName(field_value)[0]:
			raise miqtc.IfdoException('Invalid item name',str(field_value),isValidImageName(field_value)[1])
	elif field_name in ['image-datetime']:
		try:
			format = miqtv.date_formats['mariqt']
			datetime.datetime.strptime(field_value,format)
		except:
			raise miqtc.IfdoException('Invalid datetime value',str(field_value), "does not match format:",format)
	elif field_name in ['image-uuid','image-set-uuid']:
		if not miqtc.is_valid_uuid(field_value):
			raise miqtc.IfdoException(field_name,"invalid uuid 4:",str(field_value))


def are_valid_ifdo_fields(fields:dict, ignore_empty_fields = True):
	""" Check fields and throw IfdoException if an invalid field is found. Does not check if all required fields are there. """
	if ignore_empty_fields:
		fields = miqtc.recursivelyRemoveEmptyFields(fields)
	item_test_ifdo = {'image-set-header':fields}
	valid, msg = validate_against_schema(item_test_ifdo,miqtv.ifdo_schema_reduced_for_field_validation,short_msg=True,store=miqtv.schema_store)
	if not valid:
		msg = msg.replace('image-set-header','')
		raise miqtc.IfdoException(msg)
	
	for field_name,field_val in fields.items():
		ifdo_field_additional_checks(field_name,field_val)


def filesHaveUniqueName(files:list):
	""" checks if all files (with or without path) have unique file names. Returns True/False and list of duplicates"""
	fileNames_noPath = []
	duplicates = []
	prog = miqtc.PrintKnownProgressMsg("Checking files have unique names", len(files), modulo=1)
	for file in files:
		prog.progress()
		fileName_noPath = os.path.basename(file)
		if fileName_noPath in fileNames_noPath:
			duplicates.append(fileName_noPath)
		else:
			fileNames_noPath.append(fileName_noPath)
	
	prog.clear()
	if len(duplicates) == 0:
		return True, duplicates
	else:
		return False, duplicates


def isValidOrcid(orcid:str):
	""" returns whether  oricd is valid my using the MOD 11-2 check digit standard """
	# # e.g. "https://orcid.org/0000-0002-9079-593X"
	try:
		orcid = orcid[orcid.rindex("/")+1::]
	except ValueError:
		pass
	if len(orcid) != 19 or orcid[4] != "-" or orcid[9] != "-" or orcid[14] != "-":
		return False

	digits = []
	for char in orcid:
		if char.isdigit():
			digits.append(int(char))
		if char == "X" or char == "x":
			digits.append(10)

	if len(digits) != 16:
		return False

	# MOD 11-2 (see https://www.sis.se/api/document/preview/605987/)
	M = 11
	r = 2

	p = 0
	for digit in digits:
		s = p + digit
		p = s * r
	if s%M == 1:
		return True

	return False


def isValidEmail(mail:str):
	if mail.count("@") == 1:
		return True
	return False


def allImageNamesValidIn(path:miqtd.Dir,sub:str = "raw"):
	""" Validates that all image file names are valid in the given folder."""

	img_paths = miqti.browseForImageFiles(path.tosensor()+"/"+sub+"/")
	return allImageNamesValid(img_paths)

def allImageNamesValid(img_paths:dict):
	invalidImageNames = []
	prog = miqtc.PrintKnownProgressMsg("Checking files have valid names", len(img_paths), modulo=1)
	for file in img_paths:
		prog.progress()
		file_name = os.path.basename(file)
		if not isValidImageName(file_name)[0]:
			invalidImageNames.append(file)
	prog.clear()
	if len(invalidImageNames) != 0:
		return False,"Not all files have valid image names (<event>_<sensor>_<date>_<time>.<ext>)! Rename following files before continuing:\n-" + "\n- ".join(invalidImageNames)
	return True,"All filenames valid"