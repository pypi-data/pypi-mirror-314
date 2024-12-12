import os
import subprocess
import math
import re
import copy
import threading
import time
import shutil

# chick if windows, for which python-xmp-toolkit is not supported
global onWindows
onWindows = False
if os.name == 'nt':
    onWindows = True
if not onWindows:
    try:
        import libxmp
    except ModuleNotFoundError as er:
        raise ModuleNotFoundError(str(er.args) + "\n Install with e.g. $ pip install python-xmp-toolkit")

import mariqt.core as miqtc
import mariqt.directories as miqtd
import mariqt.variables as miqtv
import mariqt.files as miqtf
import mariqt.provenance as miqtp
from mariqt.variables import exiftool_path

def getVideoRuntime(path):
	""" Uses FFMPEG to determine the runtime of a video in seconds. Returns 0 in case their was any issue"""

	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")
	params = "-v fatal -show_entries format=duration -of default=noprint_wrappers=1:nokey=1".split(" ") + [path]
	result = runFfprobe(params)

	try:
		return float(result.stdout)
	except:
		return 0


def getVideoStartTime(path):
	""" Uses FFMPEG to determine the start time of a video from the metadata of the video file. Returns an empty string in case there was any issue"""
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")
	params = "-v fatal -show_entries format_tags=creation_time -of default=noprint_wrappers=1:nokey=1".split(" ") + [path]
	result = runFfprobe(params)
	return result.stdout.decode("utf-8").strip()


def runFfprobe(parameters:list):
	command = ["ffprobe"] + parameters
	try:
		result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	except FileNotFoundError:
		try:
			# in case ffmpeg was installed via snap
			command[0] = "ffmpeg." + command[0]
			result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		except FileNotFoundError:
			raise Exception("Error: ffprobe not found.")
	return result


def exifToolfound():
	command = [miqtv.exiftool_path+"exiftool"]
	try:
		result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		return True
	except FileNotFoundError:
		return False


def getVideoUUID(path):
	""" For multiple photos per directory getImageUUIDsForFolder() is much faster.
		Uses exiftool to query an video file for a UUID in its metadata (-identifier) or for mkv uses mkvinfo and 'Segment UID'. 
		Returns tuple parsed_uuid, completeMessage. parsed_uuid is an empty string if there is no UUID encoded in the file. """
	
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")

	ext = path.split('.')[-1]
	if ext.casefold() != 'mkv':

		# for all videos except mkv (matroska)
		command = [miqtv.exiftool_path+"exiftool", "-api", "largefilesupport=1","-identifier",path]
		try:
			result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		except FileNotFoundError:
			print("Error: exiftool not found at " + miqtv.exiftool_path +". Install with e.g. apt-get install exiftool")
			return "",""
		all = result.stdout.decode("utf-8").strip()
		if all != "":
			# Get last line of response
			txt = all.split("\n")[-1]
			# Omit Perl warnings
			if txt[0:14] == "perl: warning:":
				txt = ""
			# Omit other warings (e.g. Warning: [minor] Unrecognized MakerNotes)
			elif txt[0:8] == "Warning:":
				txt = ""
			# Omit other errors
			elif txt[0:5] == "Error":
				txt = ""
			else:
				txt = txt.split(":")[1].strip()
		else:
			txt = ""
		return txt, all
	
	else:
		# for mkv (matroska)
		return readSegmentUIDfromMkv(path)


def readSegmentUIDfromMkv(file):
	# so much fun with translations and different mkvinfo versions
	segmentUIDstr, all = __readSegmentUIDfromMkv(file)
	if segmentUIDstr.strip() == "":
		segmentUIDstr, all = __readSegmentUIDfromMkv(file,["--ui-language","en"])
		if segmentUIDstr.strip() == "":
			segmentUIDstr, all = __readSegmentUIDfromMkv(file,["--ui-language","en_US"])
	return segmentUIDstr, all

def __readSegmentUIDfromMkv(file,additionlArguments:list=[]):
	#command = ["mkvinfo","--ui-language","en",file]
	command = ["mkvinfo",file] + additionlArguments

	try:
		result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell = miqtc.runningOnWindows())
	except FileNotFoundError:
		print("Error: mkvinfo not found. Install with e.g. apt-get install mkvtoolnix")
		return "",""
	all = result.stdout.decode("utf-8").strip()
	segmentUID_id = "Segment UID:"
	segmentUID_id_matches = [m.start() for m in re.finditer(segmentUID_id, all)]
	if len(segmentUID_id_matches) == 0:
		return "", all
	if len(segmentUID_id_matches) != 1:
		print("Caution! Multiple segments found, first occurrence of Segment UID used for file " + file)
	segmentUID_end = all.find('\n',segmentUID_id_matches[0])
	segmentUIDstr = all[segmentUID_id_matches[0]+len(segmentUID_id):segmentUID_end].replace(" 0x","").replace(" ","").strip()
	return segmentUIDstr, all


def getPhotoUUID(path, strict=True):
	""" For multiple files per directory getImageUUIDsForFolder() is much faster.
		uses exiftool to query an image file for a UUID in its metadata 0xa420 ImageUniqueID (-exif:imageuniqueid, unless strict == False) 
		Returns tuple parsed_uuid, completeMessage. parsed_uuid is an empty string if there is no UUID encoded in the file.
	Params:
		strict: if False uses -imageuniqueid which also allows for canon:imageuniqueid (0x0028 	ImageUniqueID) which is currently 
		NOT SUPPORTED by Elements!
	"""
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")
	if strict: 
		option = "-exif:imageuniqueid"
	else:
		option = "-imageuniqueid"
	command = [miqtv.exiftool_path+"exiftool", option, path]
	try:
		result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	except FileNotFoundError:
		print("Error: exiftool not found at " + miqtv.exiftool_path +". Install with e.g. apt-get install exiftool")
		return "",""
	all = result.stdout.decode("utf-8").strip()
	if all != "":
		# Get last line of response
		txt = all.split("\n")[-1]
		# Omit Perl warnings
		if txt[0:14] == "perl: warning:":
			txt = ""
		# Omit other warings (e.g. Warning: [minor] Unrecognized MakerNotes)
		elif txt[0:8] == "Warning:":
			txt = ""
		# Omit other errors
		elif txt[0:5] == "Error":
			txt = ""
		else:
			try:
				txt = txt.split(":")[1].strip()
			except:
				pass
	else:
		txt = ""
	# check if its maybe written to -identifier instead
	if txt == "":
		return getVideoUUID(path)
	return txt,all

def imageContainsValidUUID(file:str,verbose=False):
	""" returns whether image contains valid UUID and UUID. Throws exception if file extension not in variables.photo_types or variables.video_types
		For many files per directory use the faster imagesContainsValidUUID() """
	if os.path.splitext(file)[1][1:].lower() in miqtv.photo_types:
		uuid,msg = getPhotoUUID(file)
	elif os.path.splitext(file)[1][1:].lower() in miqtv.video_types:
		uuid,msg = getVideoUUID(file)
	else:
		raise Exception("Unsupported file type to determine UUID from metadata: "+os.path.splitext(file)[1][1:])
	
	if uuid == "":
		return False, uuid

	# check for validity
	if not miqtc.is_valid_uuid(uuid):
		if verbose:
			print("Image " + file + " contains invalid UUID " + uuid)
		return False, uuid
	return True, uuid


def imagesContainValidUUID(files:list):
	""" retruns dict {'file':{'uuid':str,'valid:bool'}} """
	# find different directories
	files = [miqtc.toUnixPath(e) for e in files]
	paths = []
	for file in files:
		path = os.path.dirname(file)
		if path not in paths:
			paths.append(path)

	allFilesUUIDs = {}
	prog = miqtc.PrintKnownProgressMsg("Reading files' UUIDs in directory", len(paths),modulo=1)
	for path in paths:
		prog.progress()
		allFilesUUIDsTmp1 = getImageUUIDsForFolder(path)
		# add paths
		allFilesUUIDsTmp2 = {}
		for item in allFilesUUIDsTmp1:
			allFilesUUIDsTmp2[miqtc.toUnixPath(os.path.join(path,item))] = allFilesUUIDsTmp1[item]
		allFilesUUIDs = {**allFilesUUIDs, **allFilesUUIDsTmp2}
	prog.clear()

	# check uuids
	ret = {}
	for item in allFilesUUIDs:
		if item in files:
			valid = False
			if miqtc.is_valid_uuid(allFilesUUIDs[item]):
				valid = True
			ret[item] = {'uuid':allFilesUUIDs[item],'valid':valid}
	
	return ret


def getImagesExifFieldValuesForFolder(path:str,fieldName:str):
	""" Uses exiftool to query all images in folder path for the field value in their metadata (is much faster then doing it for each file separately). Returns a dict with filename -> UUID keys/values"""
	ret = {}
	if fieldName[0] != "-":
		fieldName = "-" + fieldName
	command = [miqtv.exiftool_path+"exiftool", "-api", "largefilesupport=1", "-T", "-filename", fieldName, path]
	try:
		result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	except FileNotFoundError:
		print("Error: exiftool not found at " + miqtv.exiftool_path +". Install with e.g. apt-get install exiftool")
		return ret
	txt = result.stdout.decode("utf-8").strip()
	if txt != "":
		lines = txt.split("\n")
		for line in lines:
			tmp = line.split("\t")
			if len(tmp) < 2:
				continue
			ret[tmp[0]] = tmp[1].strip()
	return ret                  


def getImagesAllExifValues(files:list,prov:miqtp.Provenance=None):
	""" Uses exiftool to query all images in folder path for all their exif metadata (is much faster then doing it for each file separately). Returns a dict with filename -> exif keys/values"""

	# find different directories
	paths = []
	for file in files:
		path = os.path.dirname(file)
		if path not in paths:
			paths.append(path)

	allFilesExifTags = {}
	prog = miqtc.PrintKnownProgressMsg("Reading files' Exif tags in directory", len(paths),modulo=1)
	for path in paths:
		prog.progress() 
		allFilesExifTagsTmp = getImagesAllExifValuesForFolder(path,prov,filesOnly=files)
		allFilesExifTags = {**allFilesExifTags, **allFilesExifTagsTmp}
	prog.clear()

	ret = allFilesExifTags
	return ret


def getImagesAllExifValuesForFolder(path_:str,prov:miqtp.Provenance=None,filesOnly=[]):
	""" Uses exiftool to query all images in folder path for all their exif metadata (is much faster then doing it for each file separately). Returns a dict with filename -> exif keys/values"""
	
	ret = {}

	if filesOnly != []:
		filesOnlyTmp = []
		for file in filesOnly:
			filesOnlyTmp.append(miqtc.toUnixPath(file))
		filesOnly = filesOnlyTmp 

	exifFieldsToIgnore=['Directory','File Permissions','File Access Date/Time']
	path_ = miqtc.toUnixPath(path_)
	command = [miqtv.exiftool_path+"exiftool","-api", "largefilesupport=1",path_]
	try:
		result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	except FileNotFoundError:
		print("Error: exiftool not found at " + miqtv.exiftool_path +". Install with e.g. apt-get install exiftool")
		return ret
	all = result.stdout.decode("utf-8").strip()
	# split per file
	perFile = all.split("========")
	for fileExif in perFile:
		fileExif = fileExif.strip()
		if fileExif == "":
			continue
		fileName = ""
		exif = {}
		i = 0
		for line in fileExif.split("\n"):
			i += 1
			if i == 1: # filename should be first line
				fileName = os.path.join(path_,line.strip())
				if filesOnly != [] and not fileName in filesOnly:
					break
				else:
					ret[fileName] = exif
					continue
			if line.strip() == "":
				continue
			separtorIndex = line.find(":")
			if separtorIndex == -1:
				msg = "Cannot parse exif tag from line: \'" + line + "\' in file: " + fileName
				if prov != None:
					prov.log(msg,dontShow=True)
				else:
					print(msg)
			elif line[0:separtorIndex].strip() not in exifFieldsToIgnore:
				exif[line[0:separtorIndex].strip()] = line[separtorIndex+1::].strip()

	return ret


def getImageUUIDsForFolder(path:str):
	""" Uses exiftool to query all images in folder path for the UUID in their metadata (is much faster then doing it for each file separately). 
	Returns a dict with filename -> UUID keys/values. """
	ret = {}

	# photos
	retTmp = getImagesExifFieldValuesForFolder(path,"exif:imageuniqueid")
	ret = {**ret, **retTmp}

	# videos
	retTmp = getImagesExifFieldValuesForFolder(path,"xmp:identifier")

	# make sure for photos valid previous entries are not overridden by invalid ones here 
	toRemove = []
	for file in retTmp:
		if os.path.splitext(file)[1][1:].lower() in miqtv.photo_types:
			if not miqtc.is_valid_uuid(retTmp[file]) or miqtc.is_valid_uuid(ret[file]):
				toRemove.append(file)
	for item in toRemove:
		del retTmp[item]
	ret = {**ret, **retTmp}
	## mkv
	retTmp = {}
	for file in os.listdir(path):
		if file.endswith(".mkv"):
			uuid,all = getVideoUUID(os.path.join(path,file))
			retTmp[file] = uuid
	ret = {**ret, **retTmp}
	return ret


def browseForImageFiles(path:str,extensions:list = miqtv.image_types,recursive=True,skipConfigFiles=True,
						sub_folders_ignore:list=[]):
	""" Recursively scans a folder for media files (specified by the given file extension you are looking for).

	The result variable contains a dictionary with the found file paths as keys and
	a triple for each of those files with the file size, runtime and file extension:
	<name>:[<size>,<runtime>,<ext>]
	sub_folder_ignore: list of strings containing names of folders which are to be ignored while
	scanning folder for image data 
	"""

	ret = {}
	s = miqtc.PrintLoadingMsg("Browsing for image files")
	files = miqtf.browseForFiles(path,extensions,recursive,skipConfigFiles,ignoreSubDirs=sub_folders_ignore)
	s.stop()
	videoFiles = []
	prog = miqtc.PrintKnownProgressMsg("Reading file stats ", len(files), modulo=1)
	for file in files:
		prog.progress()
		file_ext = file.split(".")[-1].lower()
		ret[file] = [os.stat(file).st_size,-1,file_ext]
		if file_ext in miqtv.video_types:
			videoFiles.append(file)
	prog.clear()

	prog = miqtc.PrintKnownProgressMsg("Reading video stats ", len(videoFiles), modulo=1)
	#start = time.time()
	getVideosRuntime_multiThread(videoFiles,ret,8,prog)
	#end = time.time()
	#print(f"Runtime of the program is {end - start}")
	prog.clear

	return ret


def getVideosRuntime_multiThread(files:list,ret:dict,nrThreads:int,prog=None):
	""" calls getVideoRuntime() in separate threads to speed up the process """
	
	if len(files) == 0:
		return

	if prog != None:
		prog.modulo = nrThreads

	if nrThreads > len(files):
		nrThreads = len(files)

	splitlen = int(len(files)/nrThreads)
	threads=[]
	exceptions = []
	for i in range(nrThreads):
		if i == nrThreads-1:
				filesSub = copy.deepcopy(files[i*splitlen::])
		else:
			filesSub = copy.deepcopy(files[i*splitlen:(i+1)*splitlen])
		
		retSub = {k:ret[k] for k in ret if k in filesSub}
		exception = [None] # list to make it call by reference
		threads.append(threading.Thread(target=__getVideosRuntime, args=(filesSub,retSub,exception,prog)))
		exceptions.append(exception)

	for thread in threads:
		thread.start()
	
	for thread in threads:
		thread.join()

	for e in exceptions:
		if e[0] != None:
			raise e[0]


def __getVideosRuntime(files:list,ret:dict,exception:list=[None],prog=None):
	
	for file in files:
		if prog != None:
			prog.progress()
		# exception within threads are not notived by parent thread, musst be passed manually
		try:
			ret[file][1] = getVideoRuntime(file)
		except Exception as e:
			exception[0] = e


def browseFolderForImages(path:str,types:list = miqtv.image_types):
	raise Exception("DEPRECATED, use browseForImageFiles instead")
	
def createImageList(path:miqtd.Dir,overwrite=False,write_path:bool=False,img_types = miqtv.image_types):
	""" Creates a text file that contains one line per image file found in path

	Can overwrite an existing file list file if told so.
	Can add the full absolute path to the text file if told so (by providing the absolute path you want as the write_path variable)
	Can filter which images (or actually all file types) to put into the file. Default is all image types.
	"""

	if not path.exists():
		return False,"Path not found"

	# Potentially create output folder
	path.createTypeFolder(["intermediate"])

	# Check whether the full path shall be written
	if write_path == True:
		write_path = path
	else:
		write_path = ""

	# Scan the directory and write all files to the output file
	dst_path = path.tosensor()+"intermediate/"+path.event()+"_"+path.sensor()+"_images.lst"
	if not os.path.exists(dst_path) or overwrite:
		try:
			lst = open(dst_path,"w")
			files = os.listdir(path.tosensor()+"raw/")
			for file in files:
				if file[0] == ".":
					continue
				fn, fe = os.path.splitext(file)
				if fe[1:].lower() in img_types:
					lst.write(write_path+file+"\n")
			lst.close()
			return True,"Created output file."
		except:
			return False,"Could not create output file."
	else:
		return True,"Output file exists."


def computeImageScaling(area_file:str, data_path:str, dst_file:str, img_col:str = "Image number/name", area_col:str = "Image area", area_factor_to_one_square_meter:float = 1.0):
	""" Turns an ASCII file with image->area information into an ASCII file with image->scaling information

	Path to the source file is given, path to the result file can be given or is constructed from the convention
	"""

	miqtc.assertExists(area_file)

	area_data = miqtf.tabFileData(area_file,[img_col,area_col],key_col = img_col,graceful=True)

	o = open(dst_file,"w")
	o.write("image-filename\timage-pixel-per-millimeter\n")

	for img in area_data:

		with Image.open(data_path + img) as im:
			w,h = im.size

			scaling = math.sqrt(w*h / (float(area_data[img][area_col]) * area_factor_to_one_square_meter * 1000000))
			o.write(img + "\t" + str(scaling) + "\n")

def createImageItemsDictFromImageItemsList(items:list):
	""" Creates from a list of item dicts a dict of dicts with the 'image-filename' value becoming the respective dicts name """
	itemsDict = {}
	for item in items:
		# in case of video files there are list entries for different time stamps. Possibly also for the same time stamp, those are merged here
		if isinstance(item,list):

			for subItem in item:
				if 'image-filename' not in subItem:
					raise Exception("subitem",subItem,"does not contain a field 'image-filename'")
				tmp_itemsDict = {subItem['image-filename']:subItem}
				log = miqtc.recursivelyUpdateDicts(itemsDict, tmp_itemsDict)

		else:
			if 'image-filename' not in item:
				raise Exception("item",item,"does not contain a field 'image-filename'")
			tmp_itemsDict = {item['image-filename']:item}
			log = miqtc.recursivelyUpdateDicts(itemsDict, tmp_itemsDict)
	return itemsDict

def createImageItemsListFromImageItemsDict(items:dict):
	""" Creates from a dict of item dicts a list of dicts with the 'image-filename' value becoming an item field again """
	itemsList = []
	for item in items:
		if isinstance(items[item],list):
			itemDictList = []
			for v in items[item]:
				itemDict = copy.deepcopy(v)
				itemDict['image-filename'] = item
				itemDictList.append(itemDict)
			itemsList.append(itemDictList)
		else:
			itemDict = copy.deepcopy(items[item])
			itemDict['image-filename'] = item
			itemsList.append(itemDict)
	return itemsList

def parseImageFileName(name:str):
	""" 
	Parses info from file name according to convetion: <event>_<sensor>_<date>_<time>.<ext> 
	Returns event, sensor or "","" in case of invalid equipment type (see variables.equipment_types).
	"""
	tmp = name.split("_")

	# Find the sensor part of the name
	eq_type_idx = -1
	for i in range(0,len(tmp)):
		tmp2 = tmp[i].split("-")
		if tmp2[0] in miqtv.equipment_types:
			eq_type_idx = i
			break
	if eq_type_idx < 0:
		return "",""

	# everthing before sensor part is tested on being a valid event name
	event = tmp[0]
	for i in range(1,eq_type_idx-1):
		event += "_" + tmp[i]

	eqid = tmp[eq_type_idx-1]
	for i in range(eq_type_idx,len(tmp)-2):
		eqid += "_" + tmp[i]

	return event, eqid

def checkFilesUUIDsInDir(path,recursive=True,progressBar=None,ProgressBarRatio=None):
	"""
	Checks UUIDs of files in path (sud its subdirs if recursive==True).
	Retruns lists files_recognized, files_no_uuid_supported,files_no_uuid_unsupported
	"""
	recognizedFileTypes = [e.casefold() for e in miqtv.video_types + miqtv.photo_types]
	content = miqtf.browseForFiles(path,recognizedFileTypes,recursive)
	files_recognized = []
	files_unsupported = []
	i = 0
	for cont in content:
		i +=1
		if not progressBar is None and not ProgressBarRatio is None:
			progressBar.value = 100 * ProgressBarRatio + (100 - 100 * ProgressBarRatio)/2 * i/len(content)
		filename, file_extension = os.path.splitext(cont)
		if os.path.isfile(cont):
			ext = file_extension.replace(".","").casefold()
			if ext in recognizedFileTypes:
				files_recognized.append(cont)
				if ext in miqtv.unsupportedFileTypes:
					files_unsupported.append(cont)

	files_no_uuid = []      
	uuids = imagesContainValidUUID(files_recognized)
	for file in uuids:
		if not uuids[file]['valid']:
			files_no_uuid.append(file)
	
	files_no_uuid_supported = [e for e in files_no_uuid if e not in files_unsupported]
	files_no_uuid_unsupported = [e for e in files_no_uuid if e in files_unsupported]
	return files_recognized, files_no_uuid_supported,files_no_uuid_unsupported

def writeUUIDtoPhoto(path, overwrite_original=False):
	""" Uses exiftool to write UUID to copy of photo. Original will be saved as path+'_original'.
	Caution: check if file contains an uuid already, otherwise its overwritten which should not happen.
	Returns success, new name of original file """
	if not os.path.exists(path):
		raise Exception("file " + path + " not found!")
	uuid = str(miqtc.uuid4())
	if overwrite_original:
		command = [miqtv.exiftool_path+"exiftool", "-overwrite_original", "-exif:imageuniqueid=" + uuid, path]
	else:
		if os.path.isfile(path + '_original'):
			raise Exception("writeUUIDtoPhoto: original file <file>_original already exists.")
		command = [miqtv.exiftool_path+"exiftool", "-exif:imageuniqueid=" + uuid, path]

	result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	all = result.stdout.decode("utf-8").strip()
	if all != "":
		if all[0:5] == "Error":
			raise Exception(all)    
	return True, path + '_original'

def writeUUIDtoVideo(path,overwrite_original=False,test_val=""):
        """ Uses XMP Toolkit to write UUID to copy of file in XMP namespace Dublin Core metadata field 'identifier'. 
		Original will be saved as path+'_original'.
		Caution: check if file contains an uuid already, otherwise its overwritten which should not happen. 
		Returns success, new name of original file """

        # testing only
        if test_val != "":
            uuid = test_val
        else:
            uuid = str(miqtc.uuid4())

        if not os.path.exists(path):
            raise Exception("file " + path + " not found!")

        if not overwrite_original:
            # check <file>_original does not exist yet 
            if os.path.isfile(path + '_original'):
                raise Exception("writeUUIDtoVideo: original file <file>_original already exists.")

            path_original = path
            path_split = path.split('.')
            path_split[-2] = path_split[-2] + "_tmp"
            path_new = ".".join(path_split)
            shutil.copyfile(path_original, path_new)
            path = path_new

        xmpfile = libxmp.XMPFiles( file_path=path, open_forupdate=True )
        xmp = xmpfile.get_xmp()
        success = False
        try:
            # Change the XMP property
            xmp.set_property( libxmp.consts.XMP_NS_DC, 'identifier',uuid)

            # Check if XMP document can be written to file and write it.
            if xmpfile.can_put_xmp(xmp):
                    xmpfile.put_xmp(xmp)
                    success = True
        except (libxmp.XMPError, AttributeError) as ex:
            print(str(ex))
            pass

        # XMP document is not written to the file, before the file
        # is closed.
        xmpfile.close_file()

        path_original_new = ""
        if not overwrite_original:
            if success:
                # rename originals
                path_original_new = path_original + "_original"
                os.rename(path_original, path_original_new)
                # rename news
                os.rename(path, path_original)
            else:
                os.remove(path)
        else:
            path_original_new = path

        return success, path_original_new