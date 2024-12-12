""" This class provides functionalities to create, read and adapt iFDO files"""

from math import pi
import math
import yaml
import os
import json
import numpy as np
import ast
import copy
import datetime
from pprint import pprint
from deepdiff import DeepDiff
from packaging.version import Version
import statistics
import requests
import zipfile
import io
import warnings

import mariqt.core as miqtc
import mariqt.directories as miqtd
import mariqt.files as miqtf
import mariqt.variables as miqtv
import mariqt.image as miqti
import mariqt.tests as miqtt
import mariqt.navigation as miqtn
import mariqt.settings as miqts
import mariqt.provenance as miqtp
import mariqt.geo as miqtg
import mariqt.sources.osis as miqtosis
import mariqt.equipment as miqtequip


class nonCoreFieldIntermediateItemInfoFile:
    def __init__(self, fileName:str, separator:str, header:dict, datetime_format:str=miqtv.date_formats['mariqt']):
        self.fileName = fileName
        self.separator = separator
        self.header = header
        self.datetime_format = datetime_format

    def __eq__(self, other):
        if self.fileName==other.fileName and self.separator == other.separator and self.header==other.header and self.datetime_format==other.datetime_format:
            return True
        else:
            return False

def findField(ifdo_dict,keys):
        """ Looks for  keys ("key" or [key1,key2]) in ifdo_dict and returns its value or an empty string if key not found"""
        if not isinstance(keys, list):
            keys = [keys]

        ar = ifdo_dict
        for k in keys:
            if k in ar:
                ar = ar[k]
            else:
                try:
                    k = int(k)
                    if not isinstance(ar,list) or len(ar) < k:
                        raise ValueError("Index",k,"out of bounds",len(ar))
                except:
                    return ""
                ar = ar[k]
        return ar


class iFDO_Reader:
    " Provides convenient functions for reading data from iFDO files "

    def __init__(self, iFDOfile:str):
        " Provides convenient functions for reading data from iFDO files "
        
        self.iFDOfile = iFDOfile
        self.ifdo = iFDO.open_ifdo_file(self.iFDOfile)


    def __getitem__(self, keys):
        """ Returns copy of checked ifdo set or item field value, also considerng default values from header.
            Use keys as e.g. '<item>:<key>:...'. Can be used for header fields as well as item fields.
            Item index can be leglected, in case of video a dict {<image-datatime>:<value>,...} is returned.
            Raises IfdoException if item does not exist. """
        keys = keys.split(':')
        return iFDO._iFDO__getFieldValue(self.ifdo,keys)


    def getImagesPositions(self,image_types=miqtv.image_types):
        """ Returns images first position(s) 
            @return: {'imageName': [{'lat': value, 'lon': value, 'datetime': value}]}, image-coordinate-reference-system """
        
        retDict = {}
        retRefsys = self.ifdo[miqtv.image_set_header_key]['image-coordinate-reference-system']

        headerValLat = None
        try:
            headerValLat = self.ifdo[miqtv.image_set_header_key]['image-latitude']
        except KeyError:
            pass

        headerValLon = None
        try:
            headerValLon = self.ifdo[miqtv.image_set_header_key]['image-longitude']
        except KeyError:
            pass


        for fileName in self.ifdo[miqtv.image_set_items_key]:
            if fileName.split('.')[-1].lower() in image_types:
                retDict[fileName] = self.__getItemLatLon(fileName,headerValLat,headerValLon)

        return retDict, retRefsys


    def writeWorldFilesForPhotos(self,destDir:str,imageSourceDir:str):
        """ Writes world files for photos if all required fields are there under the assumption that the camera was looking straight down (pitch and roll are ignored!). 
            Returns a list of items for which creation failed: [[item,msg],...]"""

        # TODO get images online from broker

        iFDOexceptions = []

        # get images position
        positionsLatLon, refsys = self.getImagesPositions(image_types=miqtv.photo_types)
        crsFieldTmp = ''.join(e for e in refsys if e.isalnum()).lower()
        if crsFieldTmp == 'wgs84' or crsFieldTmp == 'epsg4326':
            refsys = "WGS84"
        else:
            iFDOexceptions.append(["","Coordinates reference system \"" + refsys + "\" can not be handled. Use preferably EPSG:4326 or WGS84"])
            return iFDOexceptions


        for photo in positionsLatLon:
            try:
                self.checkItemHash(photo,imageSourceDir) # TODO could be in different subfolder or from online broker

                # convert to utm to avoid precision issue with lat/lon values in world files
                lat = positionsLatLon[photo][0]['lat']
                lon = positionsLatLon[photo][0]['lon']
                easting,northing,zone,isNorth = miqtg.latLon2utm(lat,lon,refsys)
                exif = self.__getItemDefaultValue(photo,'image-acquisition-settings') # TODO what if not there? read from image directly? Should be checked if hash matches? Image could have been cropped after iFDO creation
                imageWidth = int(str(exif['Image Width']).strip('\''))
                imageHeight = int(str(exif['Image Height']).strip('\''))
                heading = self.__getItemDefaultValue(photo,'image-camera-yaw-degrees')
                altitude = self.__getItemDefaultValue(photo,'image-meters-above-ground')

                domePort,msg = self.__tryGetIsDomePort(photo)
                focalLenghPixels, msg = self.__tryGetFocalLengthInPixels(photo, domePort)
                if focalLenghPixels == [-1,-1] or focalLenghPixels == -1:
                    raise miqtc.IfdoException(msg)
                miqtg.writeSimpleUtmWorldFile(os.path.join(destDir,miqtg.convertImageNameToWorldFileName(photo)),easting,northing,zone,isNorth,imageWidth,imageHeight,heading,altitude,focalLenghPixels[0],focalLenghPixels[1])
            except miqtc.IfdoException as e:
                iFDOexceptions.append([photo,str(e.args)])

        return iFDOexceptions


    def checkItemHash(self,item:str,fileDir:str):
        """ compares file's hash with hash in iFDO and throws exception if they don't match """

        file = os.path.join(fileDir,item)
        if not os.path.isfile(file):
            raise miqtc.IfdoException("File \"" + item + "\" not found in dir \"" + fileDir + "\"")

        if isinstance(self.ifdo[miqtv.image_set_items_key][item],list): # in case of video with item as list the first entry holds the default and the hash cannot vary for the same image
            itemEntry = self.ifdo[miqtv.image_set_items_key][item][0] 
        else:
            itemEntry = self.ifdo[miqtv.image_set_items_key][item]
        if not itemEntry['image-hash-sha256'] == miqtc.sha256HashFile(file):
            raise miqtc.IfdoException(item, "iFDO entry is not up to date, image hash does not match.")

    def getImageDirectory(self):
        """ Returns the lowermost local directory containing the image files inferred from 'image-set-local-path'. If 'image-set-local-path' not provided for all image items the iFDO's parent directory is returned. """
        localPaths = []
        iFDOFileParentDir = os.path.dirname(os.path.dirname(self.iFDOfile))
        for item in self.ifdo[miqtv.image_set_items_key]:
            try:
                itemLocalPath = self.__getItemDefaultValue(item,'image-set-local-path')
            except miqtc.IfdoException:
                try:
                    itemLocalPath = self.__getItemDefaultValue(item,'image-local-path') # backwards compatibility
                except miqtc.IfdoException:
                    itemLocalPath = iFDOFileParentDir
            if itemLocalPath not in localPaths:
                localPaths.append(itemLocalPath)
        commonPath = os.path.commonpath(localPaths)
        if not os.path.isabs(commonPath):
            commonPath = os.path.normpath(os.path.join(os.path.dirname(self.iFDOfile), commonPath))
        return commonPath


    def __tryGetIsDomePort(self,item):
        """ Tries to read port type from 'image-camera-housing-viewport'[viewport-type] or 'image-flatport-parameters'/'image-domeport-parameters' 
            Returns True,msg if dome port, False,msg if flat port, None,msg otherwise """

        try:
            portTypeStr = self.__getItemDefaultValue(item,'image-camera-housing-viewport')
            portTypeStr = portTypeStr['viewport-type']
            if 'dome' in portTypeStr.lower() and not 'flat' in portTypeStr.lower():
                return True,"Parsed from 'image-camera-housing-viewport'['viewport-type']"
            elif not 'dome' in portTypeStr.lower() and 'flat' in portTypeStr.lower():
                return False,"Parsed from 'image-camera-housing-viewport'['viewport-type']"
            else:
                return None,"Could not read port type from 'image-camera-housing-viewport'['viewport-type'] in item: " + item
        except (miqtc.IfdoException, KeyError):
            pass

        flatPortParamsFound = False
        try: 
            flatPortParams = self.__getItemDefaultValue(item,'image-flatport-parameters')
            flatPortParamsFound = True
        except miqtc.IfdoException:
            pass
        domePortParamsFound = False
        try: 
            domePortParams = self.__getItemDefaultValue(item,'image-domeport-parameters')
            domePortParamsFound = True
        except miqtc.IfdoException:
            pass

        if flatPortParamsFound and domePortParamsFound:
            return None,"Could not read port type from item as it contains info on both flat and dome port: " + item
        if flatPortParamsFound:
            return False,"Assumed as flat port as 'image-flatport-parameters' found in item: " + item
        if domePortParamsFound:
            return True,"Assumed as dome port as 'image-domeport-parameters' found in item: " + item
        return None,"Could not read port type from item: " + item


    def __tryGetFocalLengthInPixels(self,item:str,domePort=None):
        """ 
        Tries to read/determine focal length in pixels either from 'image-camera-calibration-model'['calibration-focal-length-xy-pixel'] or from exif values.
        if domePort = False, flat port is assumed and a correction factor of 1.33 is applied for focal length determined from exif values
        Returns either focalLength, message or [focalLengthX,focalLengthY], message. If unsuccessful focalLength = -1
        """

        # try read from 'image-camera-calibration-model'['calibration-focal-length-xy-pixel']
        try:
            focalLengthXY = self.__getItemDefaultValue(item,'image-camera-calibration-model')
            try:
                focalLengthXY = focalLengthXY['calibration-focal-length-xy-pixel']
            except KeyError:
                raise miqtc.IfdoException(item,"does not contain 'image-camera-calibration-model'['calibration-focal-length-xy-pixel']")

            if not isinstance(focalLengthXY,list): # x and y value are identical
                focalLengthXY = [focalLengthXY,focalLengthXY]
            if len(focalLengthXY) != 2:
                raise miqtc.IfdoException(item,"Invalid entry for 'image-camera-calibration-model'['calibration-focal-length-xy-pixel'] : " + str(focalLengthXY) )

            if not isinstance(focalLengthXY[0],float) or not isinstance(focalLengthXY[0],int) or not isinstance(focalLengthXY[1],float) or not isinstance(focalLengthXY[1],int):
                try:
                    focalLengthXY = [float(focalLengthXY[0]),float(focalLengthXY[1])]
                except ValueError:
                    raise miqtc.IfdoException(item,"Invalid entry for 'image-camera-calibration-model'['calibration-focal-length-xy-pixel'] : " + str(focalLengthXY) )
            
            return focalLengthXY, "Parsed from 'image-camera-calibration-model'['calibration-focal-length-xy-pixel']"
        except miqtc.IfdoException:
            pass

        underwaterImage = True
        try:
            alt0 = self[item+'0:image-altitude-meters'] #self.__getItemDefaultValue(item, 'image-altitude-meters')
            if alt0 > 0:
                underwaterImage = False
        except miqtc.IfdoException:
            pass

        # add correction factor for flat port
        if domePort is None and underwaterImage:
            return [-1,-1], "Could not determine focal length from 'image-camera-calibration-model'['calibration-focal-length-xy-pixel'] and port type, which is required for correct evaluation of exif values, is not provided!"
        correctionFkt = 1.0
        if domePort == False and underwaterImage:
            correctionFkt = 1.33

        # otherwise try derive from exif tags
        exif = self.__getItemDefaultValue(item,'image-acquisition-settings')
        ## from Focal Length, Focal Plane X Resolution, Focal Plane Y Resolution, Focal Plane Resolution Unit
        focalLengthXY, msg = self.__tryDetermineFocalLenghtInPixelsFromExif_1(exif)
        if focalLengthXY != [-1,-1]:
            return [e*correctionFkt for e in focalLengthXY], 'Derived from exif tags Focal Length, Focal Plane X Resolution, Focal Plane Y Resolution, Focal Plane Resolution Unit'
        ## from from 35 mm equivalent focal length
        focalLengthXY, msg = self.__tryDetermineFocalLenghtInPixelsFromExif_2(exif)
        if focalLengthXY != [-1,-1]:
            return [e*correctionFkt for e in focalLengthXY], 'Derived from exif tag Focal Length with 35 mm equivalent'
 
        return [-1,-1], "Could not determine from focal length in pixels from neither 'image-camera-calibration-model'['calibration-focal-length-xy-pixel'] nor exif tags Focal Length, Focal Plane X Resolution, Focal Plane Y Resolution, Focal Plane Resolution Unit"


    def __tryDetermineFocalLenghtInPixelsFromExif_1(self,exifDict:dict):
        """ try to determine focal length in pixels from exif tags Focal Length, Focal Plane X Resolution, Focal Plane Y Resolution, Focal Plane Resolution Unit.
            Retruns [focalLengthPixels_x,focalLengthPixels_y], message
            Retruns focalLengthPixels = -1 if not successfull """

        try:
            focalLength = str(exifDict['Focal Length'])
            focalPlaneRes_x = float(str(exifDict['Focal Plane X Resolution']).strip('\''))
            focalPlaneRes_y = float(str(exifDict['Focal Plane Y Resolution']).strip('\''))
            focalPlaneRes_unit = str(exifDict['Focal Plane Resolution Unit']).strip('\'')
        except (KeyError, ValueError):
            return [-1,-1], "Could not find all required fields Focal Length, Focal Plane X Resolution, Focal Plane Y Resolution, Focal Plane Resolution Unit"
        
        # parse focal length from left (may be '7.5 mm (...)')
        focalLengthStripped = focalLength.strip()
        focalLengthFloat = None
        for i in range(len(focalLengthStripped)):
            try:
                focalLengthFloat = float(focalLengthStripped[0:i+1])
            except ValueError:
                pass
        if focalLengthFloat is None:
            return [-1,-1], "Could not parse forcal length from 'Focal Length': " + focalLength
        scaleFkt_focal = self.__unitConversionFact2mm(focalLength)
        if scaleFkt_focal == -1:
            return [-1,-1], "Could not parse forcal length unit from 'Focal Length': " + focalLength
        focalLength_mm = focalLengthFloat * scaleFkt_focal

        scaleFkt_res = self.__unitConversionFact2mm(focalPlaneRes_unit)
        if scaleFkt_res == -1:
            return [-1,-1], "Could not parse Focal Plane Resolution Unit from 'Focal Plane Resolution Unit': " + focalPlaneRes_unit

        focalLengthPixels_x = focalLength_mm * focalPlaneRes_x / scaleFkt_res
        focalLengthPixels_y = focalLength_mm * focalPlaneRes_y / scaleFkt_res

        return [focalLengthPixels_x,focalLengthPixels_y], ""


    def __tryDetermineFocalLenghtInPixelsFromExif_2(self,exifDict:dict):
        """ try to determine focal length in pixels from 35 mm equivalent focal length in exif tag Focal Length's add on e.g. '7.0 mm (35 mm equivalent: 38.8 mm)'.
            Retruns [focalLengthPixels_x,focalLengthPixels_y], message
            Retruns focalLengthPixels = -1 if not successfull """

        try:
            focalLength = str(exifDict['Focal Length'])
            imageWidth = int(str(exifDict['Image Width']).strip('\''))
        except (KeyError, ValueError):
            return [-1,-1], "Could not find all required fields Focal Length, Image Width"

        # try parse 35 mm equivalent from e.g.:  7.0 mm (35 mm equivalent: 38.8 mm)
        colonIndex = focalLength.find(':')
        if colonIndex == -1:
            return [-1,-1], "Could not parse 35 mm equivalent focal length from 'Focal Length': " + focalLength
        focalLengthEq35mmFloat = None
        equal35mmPart = focalLength[colonIndex+1::].strip()
        for i in range(len(equal35mmPart)):
            try:
                focalLengthEq35mmFloat = float(equal35mmPart[0:i+1])
            except ValueError:
                pass
        scaleFkt = self.__unitConversionFact2mm(focalLength[colonIndex+1::])
        if focalLengthEq35mmFloat is None or scaleFkt == -1:
            return [-1,-1], "Could not parse 35 mm equivalent focal length from 'Focal Length': " + focalLength
        
        focalLengthPixels = focalLengthEq35mmFloat * scaleFkt * imageWidth / 36.0
        return [focalLengthPixels,focalLengthPixels], ""


    def __unitConversionFact2mm(self,unit:str):
        """ looks for letter sequence in unit and checks if it's 'inches','m','cm','mm','um' or '' and returns respective conversion factor to mm (if there are no letters it returns 1). Otherwise return -1 """

        firstLetterSeq = ""
        firstFound = False
        for i in range(len(unit)):
            if unit[i].isalpha():
                firstFound = True
                firstLetterSeq += unit[i]
            if not unit[i].isalpha() and firstFound == True:
                break

        if firstLetterSeq.lower() == "inches":
            scaleFkt = 25.4
        elif firstLetterSeq.lower() == "m":
            scaleFkt = 1000.0;
        elif firstLetterSeq.lower() == "cm":
            scaleFkt = 10.0;
        elif firstLetterSeq.lower() == "mm":
            scaleFkt = 1.0;
        elif firstLetterSeq.lower() == "um":
            scaleFkt = 1/1000;
        elif firstLetterSeq.lower() == "":
            scaleFkt = 1;
        else:
            scaleFkt = -1

        return scaleFkt


    def __getItemDefaultValue(self,item:str,fieldName:str):
        """ returns item values (first entry in case of videos). Throws mariqt.core.IfdoException if field not found. """

        ret = self[":".join([item,'0',fieldName])]
        if ret == "":
           raise miqtc.IfdoException("Error: Field {0} neither found in item {1} nor header".format(fieldName,item))
        return ret


    def __getItemLatLon(self,item:str,headerValLat,headerValLon):
        """ returns {'lat': value, 'lon': value, 'datetime': value} of list of those """

        itemVal = self.ifdo[miqtv.image_set_items_key][item]
        if not isinstance(itemVal,list):
            ret = self.__parse2LatLonDict(itemVal,headerValLat,headerValLon)
        else:
            ret = []
            try:
                itemLatDefault = itemVal[0]['image-latitude']
            except KeyError:
                itemLatDefault = headerValLat
                #if itemLatDefault is None:
                #    raise Exception("Error: Field {0} neither found in item {1} nor header".format('image-latitude',item))

            try:
                itemLonDefault = itemVal[0]['image-longitude']
            except KeyError:
                itemLonDefault = headerValLon
                #if itemLonDefault is None:
                #    raise Exception("Error: Field {0} neither found in item {1} nor header".format('image-latitude',item))

            for subEntry in itemVal:
                ret.append(self.__parse2LatLonDict(subEntry,itemLatDefault,itemLonDefault))

        return ret
            

    def __parse2LatLonDict(self,itemVal,headerValLat,headerValLon):
        """ returns {'lat':lat,'lon':lon,'datetime':datetime} """
        datetime = itemVal['image-datetime']
        try:
            lat = itemVal['image-latitude']
        except KeyError:
            lat = headerValLat
            if lat is None:
                raise Exception("Error: Field {0} neither found in item {1} nor header".format('image-latitude',itemVal))
        try:
            lon = itemVal['image-longitude']
        except KeyError:
            lon = headerValLon
            if lon is None:
                raise Exception("Error: Field {0} neither found in item {1} nor header".format('image-longitude',itemVal))
        return {'lat':lat,'lon':lon,'datetime':datetime}


def iFDOFromFile(iFDOfile:str,handle_prefix='20.500.12085',provenance = None,verbose=True,ignore_image_files=False,writeTmpProvFile=True,
                 image_broker_uuid="ee277578-a911-484d-a515-9c781d79aa91",sub_folders_ignore:list=[]):
    """ Convenience function to create an iFDO object directly form an existing iFDO file. Tries to infer image files location from 'image-set-local-path'. Returns iFDO object. 
        - iFDOfile: string path to load an explicit iFDO file.
        - handle_prefix: string prefix of the handle server. Default: the one for Geomar.
        - provenance: mariqt.provencance.Provenance object to track data provenance. Default: a new provenance object is created in the 'protocol' subfolder.
        - verbose: bool whether to print out information. Processing is faster if verbose is False. Default: True.
        - ignore_image_files: bool whether it's accepted that there are not images yet in 'dir'. Default: False.
        - writeTmpProvFile: bool whether to write a temporary provenance file during the iFDO creation process which will be replaced by a final one in the end. Default: True
        - image_broker_uuid: uuid of image broker to create image handles as https://hdl.handle.net/<handle_prefix>/<image_broker_uuid>@<image-uuid> 
        - sub_folders_ignore: list of strings containing names of folders which are to be ignored while scanning dir for image data 
"""
    
    reader = iFDO_Reader(iFDOfile)
    imagesDir = miqtc.toUnixPath(os.path.normpath(miqtc.toUnixPath(reader.getImageDirectory())))
    baseDir = miqtc.toUnixPath(os.path.commonpath([iFDOfile,imagesDir]))
    imageDataTypeFolder = [e for e in imagesDir.replace(baseDir,"").split("/") if e != ""][0]
    if imageDataTypeFolder not in miqtd.Dir.dt.__members__:
        raise miqtc.IfdoException("Images are not located in a valid data type directory (raw, intermediate, processed, ...) in the same project as iFDO file.")
    imagesDataTypeDir = os.path.join(baseDir,imageDataTypeFolder)
    dirObj = miqtd.Dir("",imagesDataTypeDir, create=False, with_gear=False)
    return iFDO(dir=dirObj,handle_prefix=handle_prefix,provenance=provenance,verbose=verbose,ignore_image_files=ignore_image_files,writeTmpProvFile=writeTmpProvFile,
                iFDOfile=iFDOfile,image_broker_uuid=image_broker_uuid, create_all_type_folders=False,sub_folders_ignore=sub_folders_ignore)


class iFDO:
    " Class for creating and editing iFDO.yaml files "

    def __init__(self, dir:miqtd.Dir, handle_prefix='20.500.12085',provenance = None,verbose=True,ignore_image_files=False,writeTmpProvFile=True,iFDOfile=None,image_broker_uuid="ee277578-a911-484d-a515-9c781d79aa91", 
                create_all_type_folders=True, sub_folders_ignore:list=[]):
        """ Creates an iFOD object. Requires a valid directory containing image data or/and and iFDO file and a handle prefix if it's not the Geomar one. Loads directory's iFDO file if it exists already.
            - dir: mariqt.directories.Dir object pointing to a valid data type directory (raw, intermediate, processed, ...) containing the image data.
            - handle_prefix: string prefix of the handle server. Default: the one for Geomar.
            - provenance: mariqt.provencance.Provenance object to track data provenance. Default: a new provenance object is created in the 'protocol' subfolder.
            - verbose: bool whether to print out information. Default: True.
            - ignore_image_files: images files are ignored. They are not searched for in 'raw' and items values are not updated nor checked. Default = False
            - writeTmpProvFile: bool whether to write a temporary provenance file during the iFDO creation process which will be replaced by a final one in the end. Default: True
            - iFDOfile: string path to load an explicit iFDO file. If not provided a matching iFDO file (if it already exists) will be loaded from the 'products' subdirectory. Default: None 
            - image_broker_uuid: uuid of image broker to create image handles as https://hdl.handle.net/<handle_prefix>/<image_broker_uuid>@<image-uuid> 
            - create_all_type_folders: whether to create all type folders (external, intermediate, processed, ...) or only the needed ones 
            - sub_folders_ignore: list of strings containing names of folders which are to be ignored while scanning dir for image data 
        """

        # check that at dir or iFDOfile provided
        if dir is None and iFDOfile is None:
            raise miqtc.IfdoException("Neither dir nor iFDOfile provided for iFDO.")

        self.dir = dir
        self.imagesDir = dir.totype()
        if create_all_type_folders:
            self.dir.createTypeFolder()
        self.handle_prefix = "https://hdl.handle.net/" + handle_prefix
        self.image_handle_prefix = self.handle_prefix + "/" + image_broker_uuid
        self.ignore_image_files = ignore_image_files

        self.imageSetHeaderKey = miqtv.image_set_header_key
        self.imageSetItemsKey = miqtv.image_set_items_key
        self.ifdo_tmp = {self.imageSetHeaderKey: {},
                         self.imageSetItemsKey: {}}
        self.ifdo_parsed = None
        self.ifdo_checked = copy.deepcopy(self.ifdo_tmp)  # to be set by createiFDO() only!
        self.__allUUIDsChecked = False
        self.prov = provenance
        if provenance == None:
            tmpFilePath = ""
            if writeTmpProvFile:
                self.dir.createTypeFolder([self.dir.dt.protocol.name])
                tmpFilePath = self.dir.to(self.dir.dt.protocol)
            self.prov = miqtp.Provenance("iFDO",verbose=verbose,tmpFilePath=tmpFilePath)

        # set global verbosity
        miqtv.setGlobalVerbose(verbose)

        if not ignore_image_files and not dir.exists():
            raise Exception("directroy", dir.str(), "does not exist.")

        if not dir.validDataDir():
            raise Exception("directroy", dir.str(), "not valid. Does not comply with structure /base/project/[Gear/]event/sensor/data_type/")

        # check iFDO file
        self.iFDOfile_ = "" # is set by setiFDOFileName()
        loadediFDO = False
        if iFDOfile is not None:
            iFDOfile_ = iFDOfile
            self.setiFDOFileName(iFDOfile_, assert_name=False)
            if not os.path.isfile(iFDOfile_):
                raise miqtc.IfdoException("iFDO file not found: " + iFDOfile_)
        else:
            iFDOfile_ = self.dir.to(self.dir.dt.products)+self.constructiFDOfileName(self.dir.project(),self.dir.event(),self.dir.sensor())

        
        self._imagesInImagesDir = []
        if self.ignore_image_files:
            print("Caution! running in ignore_image_files mode.")
        else:
            self._imagesInImagesDir = miqti.browseForImageFiles(self.imagesDir, sub_folders_ignore=sub_folders_ignore)
        self._imagesInImagesDirSortedList = [file for file in self._imagesInImagesDir]
        self._imagesInImagesDirSortedList.sort()
        self._imageNamesImagesDir = [os.path.basename(file) for file in self._imagesInImagesDir]

        if len(self._imagesInImagesDir) == 0 and not ignore_image_files:
            raise Exception("No images files found in " + self.imagesDir + " and its subdirectories")

        unique, dup = miqtt.filesHaveUniqueName(self._imagesInImagesDir)
        if not unique:
            raise Exception(
                "Not all files have unique names. Duplicates: " + str(dup))

        allvalid, msg = miqtt.allImageNamesValid(self._imagesInImagesDir) 
        if not allvalid:
            raise Exception(msg)

        files_found_log_msg_append = " image files found"
        if len(sub_folders_ignore) != 0:
            files_found_log_msg_append += ", ignoring subfolders " + str(sub_folders_ignore)
        self.prov.log(str(len(self._imagesInImagesDir)) + files_found_log_msg_append)

        # intermediate files
        self.__initIntermediateFiles()    

        # try load existing iFDO file
        if(self.readiFDOfile(iFDOfile_)):
            loadediFDO = True
        else:
            try:
                path = self.dir.to(self.dir.dt.products)
                for file_ in os.listdir(path):
                    if file_[-10:-4] == "_iFDO." and self.readiFDOfile(path+file_):
                        loadediFDO = True
                        iFDOfile_ = path+file_
                        break
            except FileNotFoundError:
                pass        

        self.tryAutoSetHeaderFields()
        self.setHeaderImageLocalPathField()
        if loadediFDO:
            self.setiFDOFileName(iFDOfile_)


    @staticmethod
    def open_ifdo_file(file:str):  
        """ open ifdo json or yaml or zip file and return as dict. """
        
        # if file is zip, unzip
        if file.split('.')[-1] == 'zip':
            file_name = '.'.join(os.path.basename(file).split('.')[0:-1])
            zip_file    = zipfile.ZipFile(file)
            ifdo_file  = zip_file.open(file_name, 'r')
            with io.TextIOWrapper(ifdo_file, encoding="utf-8") as o:
                if file.split('.')[-1] == 'yaml':
                    ifdo_dct = yaml.load(o, Loader=yaml.CLoader)
                else:
                    ifdo_dct = json.load(o)

        else:
            try_yaml = False
            
            # if file is yaml file load it as such
            if file.split('.')[-1] == 'yaml':
                try_yaml = True
                file_yaml = file

            if not os.path.isfile(file):
                # if file does not exist check if yaml version exsist and try to load that one
                file_yaml = file.replace('.json','.yaml')
                if os.path.isfile(file_yaml):
                    try_yaml = True
                else:
                    raise miqtc.IfdoException("File not found: " + file)

            # try load json, otherwise try yaml
            if try_yaml:
                o = open(file_yaml, 'r')
                ifdo_dct = yaml.load(o, Loader=yaml.CLoader)
            else:
                o = open(file, 'r')
                ifdo_dct = json.load(o)
            o.close()

        return ifdo_dct


    def readiFDOfile(self,file:str):
        """ reads iFDO file """

        s = miqtc.PrintLoadingMsg("Loading iFDO file")
        try:
            self.ifdo_tmp = self.open_ifdo_file(file)
            self.ifdo_parsed = copy.deepcopy(self.ifdo_tmp)
            s.stop()
            self.prov.addPreviousProvenance(self.prov.getLastProvenanceFile(self.dir.to(self.dir.dt.protocol),self.prov.executable))
        except miqtc.IfdoException:
            s.stop()
            return False
        except Exception as e:
            s.stop()
            self.prov.log(str(e))
            return False

        # try to parse e.g. strings that represent dicts
        miqtc.recursiveEval(self.ifdo_tmp)

        if self.imageSetHeaderKey not in self.ifdo_tmp:
            raise Exception("Error loading iFDO file",file,"does not contain",self.imageSetHeaderKey)
        if self.imageSetItemsKey not in self.ifdo_tmp:
            raise Exception("Error loading iFDO file",file,"does not contain",self.imageSetItemsKey)

        if  self.ifdo_tmp[self.imageSetHeaderKey] == None:
            self.ifdo_tmp[self.imageSetHeaderKey] = {}
        if self.ifdo_tmp[self.imageSetItemsKey] == None:
            self.ifdo_tmp[self.imageSetItemsKey] = {}

        self.prov.log("iFDO file loaded: " + os.path.basename(file))

        # check iFDO version
        readVersion = "v.1.0.0" # did not have the 'image-set-ifdo-version' field yet
        try: 
            readVersion = self.findTmpField('image-set-ifdo-version')
        except KeyError:
            pass
        intReadVersion = Version(readVersion)
        intThisVersion = Version(miqtv.iFDO_version)
        if intReadVersion < intThisVersion:
            self.prov.log("Loaded iFDO has version " + readVersion + " and will be updated to version " + miqtv.iFDO_version)
        if intReadVersion > intThisVersion:
            self.prov.log("Caution! Loaded iFDO has version " + readVersion + " is ahead of version used here: " + miqtv.iFDO_version)

        try:
            self.convertToDefaultDateTimeFormat(self.ifdo_tmp)
        except Exception as ex:
            self.prov.log("Checking datetime formats: " + str(ex))

        self._try_upgrade_to_ifdo_version_2x()

        self.makePhotoItemsDictsIfLists(self.ifdo_tmp)

        # check read iFDO file
        try:
            if not self.ignore_image_files:
                self.createiFDO(self.ifdo_tmp[self.imageSetHeaderKey], miqti.createImageItemsListFromImageItemsDict(self.ifdo_tmp[self.imageSetItemsKey]))
            else:
                self.updateiFDO(self.ifdo_tmp[self.imageSetHeaderKey], miqti.createImageItemsListFromImageItemsDict(self.ifdo_tmp[self.imageSetItemsKey]),header_only=self.ignore_image_files)
        except miqtc.IfdoException as ex:
            self.prov.log("Loaded iFDO file not valid yet: " + str(ex))

        return True


    def write_ifdo_file(self,allow_missing_required=False, as_zip:bool=False):
        """ Writes an iFDO file to disk. Overwrites potentially existing file.
        as_zip: safe file as zip file """

        s = miqtc.PrintLoadingMsg("Writing iFDO file")

        self.dir.createTypeFolder([self.dir.dt.products.name, self.dir.dt.protocol.name])

        # check fields again if changed since last check (createiFDO)
        if self.ifdo_tmp != self.ifdo_checked:
            self.createiFDO(self.ifdo_tmp[self.imageSetHeaderKey], miqti.createImageItemsListFromImageItemsDict(self.ifdo_tmp[self.imageSetItemsKey]),
                            allow_missing_required=allow_missing_required)
        
        # add "$schema"
        self.ifdo_checked["$schema"] = miqtv.ifdo_schema['$id']
        
        iFDO_path = self.getiFDOFileName(overwrite=True)

        # puts everything in one line
        #with open(iFDO_path.replace("yaml","json"), 'w') as fp:
        #    json.dump(self.ifdo_checked, fp)

        # convert dictionary to JSON string
        json_data = json.dumps(self.ifdo_checked, indent = 4, sort_keys=True)

        # write the JSON string to a file
        if as_zip:
            with zipfile.ZipFile(iFDO_path + '.zip','w', zipfile.ZIP_DEFLATED) as zip:
                zip.writestr(os.path.basename(iFDO_path), json_data)
        else:
            with open(iFDO_path, 'w') as f:
                f.write(json_data)
        
        # log changes
        if not self.ifdo_parsed is None:
            ifdo_update = DeepDiff(self.ifdo_parsed,self.ifdo_checked)
            s.stop() 
            #pprint(ifdo_update)
            if ifdo_update != {}:
                self.prov.log("iFDO updated")
                self.prov.log(str(ifdo_update),dontShow=True)
        else:
             s.stop() 
        
        self.prov.write(self.dir.to(self.dir.dt.protocol))
        self.prov.log("Wrote iFDO to file " + iFDO_path)


    def writeiFDOfile(self,allow_missing_required=False):
        """ Deprecated - use write_ifdo_file """
        self.write_ifdo_file(allow_missing_required)


    def setiFDOFileName(self,iFDOfile:str, assert_name=True):
        """ Set the current iFDO file name with path. Set to "" in order to get default name and location. """
        self.iFDOfile_ = iFDOfile
        self.iFDOfile_ = self.getiFDOFileName() # construct default name if empty
        if assert_name and miqtc.assertSlash(os.path.dirname(self.iFDOfile_)) != miqtc.assertSlash(self.dir.to(self.dir.dt.products)):
            self.prov.log("Caution! iFDO file path is not in 'products' sub folder as recommended. Consider resetting with setiFDOFileName()." + os.path.basename(iFDOfile))
        try:
            event = self.findTmpField('image-event')['name']
            sensor = self.findTmpField('image-sensor')['name']
        except miqtc.IfdoException:
            event = self.dir.event()
            sensor = self.dir.sensor()

        iFDOfileName = os.path.basename(self.iFDOfile_)
        if assert_name and (not event in iFDOfileName or not iFDO.getShortEquipmentID(sensor) in iFDOfileName):
            self.prov.log("Caution! iFDO file name does not contain project, event and sensor name as recommended. Consider resetting with setiFDOFileName(). " +  os.path.basename(iFDOfile))


    def getiFDOFileName(self,overwrite=False):
        """ Returns the current iFDO file's name with path. If not set yet or overwrite==True it returns the one matching image-set-name. """
        if self.iFDOfile_ == "" or overwrite:
            file_name = self.findTmpField('image-set-name') + '_iFDO.json'
            if self.iFDOfile_ != "":
                # rename file but keep location
                if file_name != os.path.basename(self.iFDOfile_) and os.path.exists(self.iFDOfile_):
                    self.prov.log("Caution! ifdo file renamed to " + file_name)
                self.iFDOfile_ = os.path.join(os.path.dirname(self.iFDOfile_),file_name)
            else:
                self.iFDOfile_ = os.path.join(self.dir.to(self.dir.dt.products), file_name)
        return self.iFDOfile_


    def set_image_set_name_field_from_project_event_sensor(self):
        """ Sets field image-set-name from current tmp fields for project, event and sensor. 
        Returns image-set-name value. """
        
        new_image_set_name = self.get_image_set_name_field_from_project_event_sensor(self.ifdo_tmp)
        self.ifdo_tmp[self.imageSetHeaderKey]['image-set-name'] = new_image_set_name
        return new_image_set_name
        

    @staticmethod
    def get_image_set_name_field_from_project_event_sensor(ifdo:dict):
        """ Creates and returns image-set-name from current tmp fields for project, event and sensor. """
        new_image_set_name = iFDO.constructImageSetName(ifdo['image-set-header']['image-project']['name'],
                                                        ifdo['image-set-header']['image-event']['name'],
                                                        ifdo['image-set-header']['image-sensor']['name'])
        return new_image_set_name

    @staticmethod
    def constructImageSetName(project:str,event:str,sensor:str):
        """ returns <project>_<event>_<sensor>, with short version of <sensor> (only id), preventing potential doubling of <project>  """
        project = project.strip().replace(' ','-')
        event = event.strip().replace(' ','-')
        sensor = sensor.strip().replace(' ','-')
        sensor_short = iFDO.getShortEquipmentID(sensor)
        if len(event) > len(project) and event[0:len(project)] == project:
            image_set_name_ = event + "_" + sensor_short
        else:
            image_set_name_ = project + "_" + event + "_" + sensor_short
        return image_set_name_ # TODO include dataType?


    @staticmethod
    def getShortEquipmentID(equipmentID:str):
        """ returns equipment id without potentiall long <name> part, i.e.: <owner>_<type>-<type index[_<subtype>] """
        return '_'.join(equipmentID.split('_')[0:3])

    @staticmethod
    def constructiFDOfileName(project:str,event:str,sensor:str):
        """ returns <constructImageSetName()>_iFDO.json """
        return iFDO.constructImageSetName(project,event,sensor) + '_iFDO.json' 

    
    @staticmethod
    def __getFieldValue(ifdo:dict,keys:list,default_only = False):
        """ returns copy of set or item field value, also considerng default values from header.
            Use keys as e.g. [<item>,<key>,..]. Can be used for header fields as well as item fields.
            Item index can be neglected, in case of video a dict {<image-datatime>:<value>,...} is returned
            unless default_only = False, then default values at index 0 is returned.
            Raises IfdoException if keys do not exist. """

        if not miqtv.image_set_items_key in ifdo or not miqtv.image_set_header_key in ifdo:
            raise miqtc.IfdoException("Invalid ifdo dict, missing items or header key: " + str(ifdo))
        
        if not isinstance(keys,list):
            keys = [keys]

        # remove header or item prefixes if there
        if keys[0] == miqtv.image_set_items_key or keys[0] == miqtv.image_set_header_key:
            keys = keys[1::]

        header = ifdo[miqtv.image_set_header_key]
        items = ifdo[miqtv.image_set_items_key]
        # look for default value
        for skippedInHeader in range(len(keys)):
            defaultVal = findField(header,keys[skippedInHeader::])
            if defaultVal != "":
                break


        ## look for item value
        # header only value, don't check in items
        if findField(items,keys[0:1]) == "" and skippedInHeader == 0:
            ret = defaultVal
            if ret == "":
                raise miqtc.IfdoException("key does not exist:" + str(keys))
        else:
            # if first key not found in items, i.e. is not a image name, and first key is not a header key:
            if findField(items,keys[0:1]) == "" and skippedInHeader != 0:
                raise miqtc.IfdoException("item does not exist:" + str(keys[0:1]))

            # check if index provided
            indexProvided = True
            if len(keys) > 1:
                try:
                    index = int(keys[1])
                except Exception:
                    indexProvided = False
            elif len(keys) == 1:
                indexProvided = False
                
            imageItemTimePoints = items[keys[0]]

            if indexProvided:
                # if key is whole image add all values from header
                if len(keys) == 2:
                    defaultVal = header
                # add default from index 0
                if len(keys) > 1 and index != 0:
                    keys_0 = copy.deepcopy(keys)
                    keys_0[1] = 0
                    ret_0 = iFDO.__getItemValue(items,keys_0,skippedInHeader,defaultVal)
                    if isinstance(ret_0,dict):
                        defaultVal = {**defaultVal,**ret_0}
                ret = iFDO.__getItemValue(items,keys,skippedInHeader,defaultVal)
            
            else:
                # if key is whole image add all values from header
                if len(keys) == 1:
                    defaultVal = header

                # picture -> just one entry, insert index 0
                if type(imageItemTimePoints) == dict or (type(imageItemTimePoints) == list and len(imageItemTimePoints) == 1):
                    ret = iFDO.__getItemValue(items,keys,skippedInHeader,defaultVal)
                    
                # video -> return values for each time stamp
                else:
                    ret = {}
                    for i in range(len(imageItemTimePoints)):
                        timePointData = imageItemTimePoints[i]
                        keys_i = keys[0:1] + [i] + keys[1::]
                        val_i = iFDO.__getItemValue(items,keys_i,skippedInHeader,defaultVal)
                        # default only
                        if default_only:
                            ret = val_i
                            break
                        ret[timePointData['image-datetime']] = val_i
                        # remove image-datetime if there
                        if isinstance(ret[timePointData['image-datetime']],dict) and 'image-datetime' in ret[timePointData['image-datetime']]:
                            del ret[timePointData['image-datetime']]['image-datetime']
                        # video defaults
                        if i == 0:
                            if isinstance(ret[timePointData['image-datetime']],dict):
                                defaultVal = {**defaultVal,**ret[timePointData['image-datetime']]}
                            else:
                                defaultVal = ret[timePointData['image-datetime']]

                        i += 1

        if isinstance(ret,dict) or isinstance(ret,list):
            ret = copy.deepcopy(ret)
        if ret == "" or ret == {}:
            raise miqtc.IfdoException("keys do not exist:" + str(keys))
        return ret


    @staticmethod
    def __getItemValue(items,keys,skippedInHeader,defaultVal):
        itemValue = findField(items,keys)

        if itemValue == "":
            ret = defaultVal
        # in case of dicts joint header and item fields
        elif isinstance(itemValue,dict) and defaultVal != "":
            if not isinstance(defaultVal,dict):
                raise miqtc.IfdoException("Item field is dict but default value in header is not: " + str(keys))
            ret = {**defaultVal,**itemValue}
        else:
            ret = itemValue
        return ret


    @staticmethod
    def makePhotoItemsDictsIfLists(ifdo:dict, provenance:miqtp.Provenance = None):
        for item_name in ifdo[miqtv.image_set_items_key]:
            if item_name.split('.')[-1].lower() in miqtv.photo_types:
                item_entry = ifdo[miqtv.image_set_items_key][item_name]
                if isinstance(item_entry, list):
                    if len(item_entry) > 1:
                        error_msg = "Error! Image item '" + item_name + "'contains multiple entries! Please correct!"
                        if provenance is not None:
                            provenance.log(error_msg)
                        else:
                            print(error_msg)
                    else:
                        ifdo[miqtv.image_set_items_key][item_name] = ifdo[miqtv.image_set_items_key][item_name][0]


    def __str__(self) -> str:
        """ Prints current iFDO file """
        return yaml.dump(self.ifdo_checked, default_style=None, default_flow_style=None, allow_unicode=True, width=float("inf"))


    def __getitem__(self, keys):
        """ Returns copy of checked ifdo set or item field value, also considerng default values from header.
            Use keys as e.g. '<item>:<key>:...'. Can be used for header fields as well as item fields.
            Item index can be leglected, in case of video a dict {<image-datatime>:<value>,...} is returned.
            Raises IfdoException if item does not exist. """
        keys = keys.split(':')
        return self.__getFieldValue(self.ifdo_checked,keys)


    def findTmpField(self,keys):
        """ Returns copy of temporary unchecked ifdo set or item field value, also considerng default values from header.
            Use keys as e.g. '<item>:<key>:...'. Can be used for header fields as well as item fields.
            Item index can be leglected, in case of video a dict {<image-datatime>:<value>,...} is returned.
            Raises IfdoException if item does not exist. """
        keys = keys.split(':')
        return self.__getFieldValue(self.ifdo_tmp,keys)
    

    def findTmpField2(self,keys):
        """ Returns copy of temporary unchecked ifdo set or item field value, also considerng default values from header.
            Use keys as e.g. '<item>:<key>:...'. Can be used for header fields as well as item fields.
            Item index can be leglected, in case of video a dict {<image-datatime>:<value>,...} is returned.
            Returns empty string if item does not exist. """
        return iFDO.find_field_str(self.ifdo_tmp,keys)
    

    @staticmethod
    def find_field_str(ifdo:dict,keys):
        """ Returns copy of ifdo set or item field value, also considerng default values from header.
            Use keys as e.g. '<item>:<key>:...'. Can be used for header fields as well as item fields.
            Item index can be leglected, in case of video a dict {<image-datatime>:<value>,...} is returned.
            Returns empty string if item does not exist. """
        keys = keys.split(':')
        try:
            ret = iFDO.__getFieldValue(ifdo,keys)
        except miqtc.IfdoException as ex:
            ret = ""
        return ret


    def setiFDOHeaderFields(self, header: dict):
        """ Deprecated - use set_ifdo_header_fields """
        self.set_ifdo_header_fields(header)


    def set_ifdo_header_fields(self, header: dict):
        """ Clears current header fields und sets provided field values. For updating existing ones use update_ifdo_header_fields() """
        self.ifdo_tmp[self.imageSetHeaderKey] = {}
        if self.imageSetHeaderKey in header:
            header = header[self.imageSetHeaderKey]
        for field in header:
            #if field not in miqtv.ifdo_header_core_fields:
            #    self.prov.log("Caution! Unknown header field \"" + field + "\". Maybe a typo? Otherwise ignore me.")
            self.ifdo_tmp[self.imageSetHeaderKey][field] = header[field]


    def update_ifdo_header_fields(self, header: dict):
        """ Updates existing header fields """
        if self.imageSetHeaderKey in header:
            header = header[self.imageSetHeaderKey]
        log = miqtc.recursivelyUpdateDicts(self.ifdo_tmp[self.imageSetHeaderKey], header)
        self.prov.log(log,dontShow=True)

    def updateiFDOHeaderFields(self, header: dict):
        """ Deprecated - use update_ifdo_header_fields """
        self.update_ifdo_header_fields(header)


    def _try_upgrade_to_ifdo_version_2x(self):
        """ Try to convert fields from iFDO version < 2.0.0 to 2.x """
        read_version_str = "v1.0.0" # did not have the 'image-set-ifdo-version' field yet
        try: 
            read_version_str = self.findTmpField('image-set-ifdo-version')
        except miqtc.IfdoException:
            pass
        read_version = Version(read_version_str)

        if read_version < Version("2.0.0"):
            
            # new URI object fields
            new_uri_fields = ['image-sensor','image-event','image-project','image-context','image-license','image-platform']
            for uri_field in new_uri_fields:
                old_str_val = self.findTmpField2(uri_field)
                if isinstance(old_str_val,str) and old_str_val != "":                    
                    new_obj_val = {'name': old_str_val}
                    is_uri, msg = miqtt.validate_against_schema(old_str_val,{"type": "string","format": "uri"})
                    if is_uri:
                        new_obj_val['uri'] = old_str_val
                    self.ifdo_tmp[self.imageSetHeaderKey][uri_field] = new_obj_val
                    self.prov.log("Auto-upgraded " + uri_field + " from " + old_str_val + " to " + str(new_obj_val))



    def tryAutoSetHeaderFields(self):
        """ Sets certain header fields e.g. from directory if they are not set yet """

        if self.findTmpField2('image-sensor') == "":
            self.ifdo_tmp[self.imageSetHeaderKey]['image-sensor'] = {'name': self.dir.sensor()}
            self.prov.log("'image-sensor'\t empty, parsed from directoy and set to: " + self.ifdo_tmp[self.imageSetHeaderKey]['image-sensor']['name'])

        if self.findTmpField2('image-event') == "":
            self.ifdo_tmp[self.imageSetHeaderKey]['image-event'] = {'name': self.dir.event()}
            self.prov.log("'image-event'\t empty, parsed from directoy and set to: " + self.ifdo_tmp[self.imageSetHeaderKey]['image-event']['name'])

        if self.findTmpField2('image-project') == "":
            self.ifdo_tmp[self.imageSetHeaderKey]['image-project'] =  {'name': self.dir.project()}
            self.prov.log("'image-project'\t empty, parsed from directoy and set to: " + self.ifdo_tmp[self.imageSetHeaderKey]['image-project']['name'])

        if self.findTmpField2('image-platform') == "" and self.dir.gear() != "":
            self.ifdo_tmp[self.imageSetHeaderKey]['image-platform'] = {'name': self.dir.gear()}
            self.prov.log("'image-platform'\t empty, parsed from directoy and set to: " + self.ifdo_tmp[self.imageSetHeaderKey]['image-platform']['name'])

        if not 'image-set-uuid' in self.ifdo_tmp[self.imageSetHeaderKey]:
            self.ifdo_tmp[self.imageSetHeaderKey]['image-set-uuid'] = str(miqtc.uuid4())
        if not 'image-set-handle' in self.ifdo_tmp[self.imageSetHeaderKey]:
            self.ifdo_tmp[self.imageSetHeaderKey]['image-set-handle'] = self.handle_prefix + "/" + self.findTmpField('image-set-uuid')
        if not 'image-set-name' in self.ifdo_tmp[self.imageSetHeaderKey] or self.findTmpField2('image-set-name') == "":
            # construct as <project>_<event>_<sensor>
            project_ = self.findTmpField2("image-project")['name']
            event_ = self.findTmpField2("image-event")['name']
            if event_ == "":
                event_ = self.dir.event()
            sensor_ = self.findTmpField2("image-sensor")['name']
            if sensor_ == "":
                sensor_ = self.dir.sensor()
            self.ifdo_tmp[self.imageSetHeaderKey]['image-set-name'] = iFDO.constructImageSetName(project_,event_,sensor_)

        # set version
        self.ifdo_tmp[self.imageSetHeaderKey]['image-set-ifdo-version'] = miqtv.iFDO_version


    def setHeaderImageLocalPathField(self):
        """ Sets header field 'image-set-local-path' from image dir """
        self.ifdo_tmp[self.imageSetHeaderKey]['image-set-local-path'] = os.path.relpath(self.imagesDir, os.path.dirname(self.getiFDOFileName()))


    def create_fields(self, allow_missing_required=False):
        """ Create and validate current header fields and item fields from intermediate files. Overwrites existing fields. """
        item_data = self._get_item_data_from_intermediate_files()
        return self.createiFDO(self.ifdo_tmp[self.imageSetHeaderKey], item_data.values(), allow_missing_required=allow_missing_required)


    def update_fields(self, header_only:bool=None):
        """ Update and validate current header fields and item fields from intermediate files. """
        if header_only is None:
            header_only = self.ignore_image_files
        if not header_only:
            item_data = self._get_item_data_from_intermediate_files()
            return self.updateiFDO(self.ifdo_tmp[self.imageSetHeaderKey], item_data.values())
        else:
            return self.updateiFDO(self.ifdo_tmp[self.imageSetHeaderKey], [], header_only=True)


    def createCoreFields(self):
        """ DEPRECADET, use create_fields() or update_fields() insted.
        Fills the iFDO core fields from intermediate files. Without them no valid iFDO can be created.
        """
        item_data = self._get_item_data_from_intermediate_files_core()
        # check fields for validity
        # item_data contains field image-filename, which which will not be stored as an item field in iFOD but as the item name itself
        return self.updateiFDO(self.ifdo_tmp[self.imageSetHeaderKey], item_data.values())


    def createCaptureAndContentFields(self):
        """ DEPRECADET, use create_fields() or update_fields() insted.
        Fills the iFDO caputre and content fieds from provided data fields 
        """
        item_data = self._get_item_data_from_intermediate_files_none_core()
        # check fields for validity
        # item_data contains field image-filename, which which will not be stored as an item field in iFOD but as the item name itself
        return self.updateiFDO(self.ifdo_tmp[self.imageSetHeaderKey], item_data.values())

    
    def _get_item_data_from_intermediate_files(self):
        """ Read data from core and none-core intermdeate files, check files exist, add 'image-handle'.
        Returns dict of form {image-file-name:{field:value},...} 
        """
        item_data_core = self._get_item_data_from_intermediate_files_core()
        item_data_none_core = self._get_item_data_from_intermediate_files_none_core()
        #pprint(item_data_none_core)
        #pprint(item_data_core)
        item_data = item_data_core
        log = miqtc.recursivelyUpdateDicts(item_data, item_data_none_core)
        #pprint(item_data)
        self.prov.log(log,dontShow=True)
        return item_data

    def _get_item_data_from_intermediate_files_none_core(self):
        """ Read data from non-core intermdeate files.
        Returns dict of form {image-file-name:{field:value},...} 
        """
        req = self.nonCoreFieldIntermediateItemInfoFiles

        item_data = {}
        if miqtv.getGlobalVerbose():
            print("Parsing intermediate additional data ...")
        for r in req:
            if os.path.exists(r.fileName):
                self.praseItemDataFromFile(item_data,r.fileName,r.separator,r.header, r.datetime_format)
                self.prov.log("Parsed item data from: " + r.fileName)
            else:
                self.prov.log("File does not exists: " + r.fileName)

        # check files exist
        remove = []
        for img in item_data:
            if not img in self._imageNamesImagesDir:
                remove.append(img)
        for img in remove:
            del item_data[img]

        return item_data


    def _get_item_data_from_intermediate_files_core(self):
        """ Read data from core intermdeate files, check files exist, add 'image-handle'.
        Returns dict of form {image-file-name:{field:value},...} 
        """

        # Which files contain the information needed to create the iFDO items core information and which columns shall be used
        req = self.intermediateFilesDef_core

        item_data = {}
        if miqtv.getGlobalVerbose(): 
            print("Parsing intermediate core data ...")
        for r in req:
            file = self.__get_int_file_prefix() + req[r]['suffix']
            if not os.path.exists(file):
                self.prov.log("WARNING! For achieving FAIRness an intermediate image info file is missing: "+ self.__get_int_file_prefix() + req[r]['suffix']+ " run first: " + req[r]['creationFct'])
            else:
                self.parseItemDatafromTabFileData(item_data, file, req[r]['cols'], req[r]['optional'])
                self.prov.log("Parsed item data from: " + file)

        if len(item_data) == 0:
            raise Exception("No iFDO items")

        # check files exist
        remove = []
        for img in item_data:
            if not img in self._imageNamesImagesDir:
                remove.append(img)
        for img in remove:
            del item_data[img]

        # add image-url
        for img in item_data:
            if isinstance(item_data[img],list): # item is already a list (video) but parsed data is not, i.e. parsed data refers to whole video (time independent), i.e. write to first entry
                uuid = findField(item_data[img][0],'image-uuid')
                if uuid == "":
                    pprint(item_data[img][0])
                    raise miqtc.IfdoException("uuid not found (a)")
                item_data[img][0]['image-handle'] = self.image_handle_prefix + '@' + uuid
            else:
                uuid = findField(item_data[img],'image-uuid')
                if uuid == "":
                    raise miqtc.IfdoException("uuid not found (b)")
                item_data[img]['image-handle'] = self.image_handle_prefix + '@' + uuid

        return item_data


    def add_item_info_tab_file(self, fileName: str, separator:str, header:dict, datetime_format = miqtv.date_formats['mariqt']):
        """ Add a column seperated text file to parse item data from by createCaptureAndContentFields(). 
        Columns headers will be set as item field names. Must contain column 'image-filename'.
        """
        if fileName == None or not os.path.exists(fileName):
            raise Exception("File",fileName,"not found")

        for field in header:
            if header[field] not in miqtf.tabFileColumnNames(fileName,col_separator=separator):
                raise Exception("Column", header[field], "not in file", fileName)

        if miqtc.assertSlash(os.path.dirname(fileName)) != miqtc.assertSlash(self.dir.to(self.dir.dt.intermediate)):
            self.prov.log( "Caution! It is recommended to put file in the directory's 'intermediate' folder: " + fileName)
        ncfiif = nonCoreFieldIntermediateItemInfoFile(fileName, separator, header, datetime_format)
        if ncfiif not in self.nonCoreFieldIntermediateItemInfoFiles: 
            self.nonCoreFieldIntermediateItemInfoFiles.append(ncfiif)

    def addItemInfoTabFile(self, fileName: str, separator:str, header:dict, datetime_format = miqtv.date_formats['mariqt']):
        """ Deprecated - use add_item_info_tab_file """
        self.add_item_info_tab_file(fileName,separator,header,datetime_format)

        
    def removeItemInfoTabFile(self, fileName: str, separator:str, header:dict, datetime_format:str):
        """ removes file item from list of files to parse item data from by createCaptureAndContentFields() """
        ncfiif = nonCoreFieldIntermediateItemInfoFile(fileName, separator, header, datetime_format)
        if ncfiif in self.nonCoreFieldIntermediateItemInfoFiles: 
            self.nonCoreFieldIntermediateItemInfoFiles.remove(ncfiif)


    def updateiFDO(self, header: dict, items: list, header_only=False):
        """ Updates the current values iFDO with the provided new values """
        return self.createiFDO(header, items, updateExisting=True, headerOnly=header_only)


    def createiFDO(self, header: dict, items: list, updateExisting=False,headerOnly=False,allow_missing_required=False,validate_single_items=False):
        """ Creates FAIR digital object for the image data itself. This consists of header information and item information.
        updateExisting: if False old values are removed, otherwise they are updated.
        headerOnly: if True items may be empty list.
        allow_missing_required: if True, no exception risen if a required field is missing.  """

        if not updateExisting and len(items) == 0 and not headerOnly:
            raise Exception('No item information given')

        if updateExisting:
            # header
            self.update_ifdo_header_fields(header)
            # items
            # update copy of current items with new items fields
            if not headerOnly:
                itemsDict = miqti.createImageItemsDictFromImageItemsList(items)
                updatedItems_copy = copy.deepcopy(self.ifdo_tmp[self.imageSetItemsKey])
                log = miqtc.recursivelyUpdateDicts(updatedItems_copy, itemsDict)
                self.prov.log(log,dontShow=True)
                items = miqti.createImageItemsListFromImageItemsDict(updatedItems_copy)

        else:
            # overwrite header
            self.set_ifdo_header_fields(header)
            # clear items section
            self.ifdo_tmp[self.imageSetItemsKey] = {}

        # Parse image-abstract and fill its placeholders with information
        try:
            self.ifdo_tmp[self.imageSetHeaderKey]['image-abstract'] = miqts.parseReplaceVal(self.ifdo_tmp[self.imageSetHeaderKey], 'image-abstract')
        except Exception as ex:
            self.prov.log("Could not replace keys in \'image-abstract\': " + str(ex))


        # set version (so it cannot be changed by user)
        self.ifdo_tmp[self.imageSetHeaderKey]['image-set-ifdo-version'] = miqtv.iFDO_version

        # Validate item information
        image_set_items = {}
        if headerOnly:
            self.prov.log("Caution! iFDO created in header_only/ignore_image_file mode. Image items are neither updated nor checked.")
        else:
            invalid_items = 0

            prog = miqtc.PrintKnownProgressMsg("Checking items", len(items),modulo=1)
            for item in items:
                prog.progress()
                # check if all core fields are filled and are filled validly
                try:

                    # check item image exists
                    # if item is a list (video), one would have to check if each entry is valid given the default values in first entry plus given default values in header
                    is_video = True
                    if not isinstance(item,list):
                        item = [item]
                        is_video = False
                    subItemDefault = item[0] 
                    for subItem in item:
                        file_name = subItem['image-filename']
                        if not self.ignore_image_files and file_name not in self._imageNamesImagesDir:
                            raise Exception("Item '" + file_name + "' not found in /raw directory.")

                        if validate_single_items:
                            miqtt.are_valid_ifdo_fields(subItem)
                        else:
                            for field_name,field_val in subItem.items():
                                miqtt.ifdo_field_additional_checks(field_name,field_val)                        

                    image_set_items[subItemDefault['image-filename']] = [] # could make an extra case for images omitting the list
                    for subItem in item:
                        subItemDict = {}
                        for it in subItem:
                            if it != 'image-filename':
                                subItemDict[it] = subItem[it]
                        image_set_items[subItemDefault['image-filename']].append(subItemDict)
                    
                    # if is photo undo list of len 1 to only a dict
                    if not is_video:
                        image_set_items[subItemDefault['image-filename']] = image_set_items[subItemDefault['image-filename']][0]
                
                except miqtc.IfdoException as e:
                    invalid_items += 1
                    self.prov.log("Invalid image item: "+ str(item),dontShow=True)
                    self.prov.log("Exception:\n"+ str(e.args),dontShow=True)
                    raise miqtc.IfdoException("Invalid image item "+ file_name + ":\nException:\n"+ str(e.args)) # otherwise, in case of many images, it may keep running and throwing errors for quit some time
            prog.clear()

            if len(items) != 0 and invalid_items == len(items):
                raise Exception("All items are invalid")
            elif invalid_items > 0:
                self.prov.log("At least " + str(invalid_items) + " items were invalid (of" + str(len(items))+ ")")

        # Validate header information
        try:
            miqtt.are_valid_ifdo_fields(self.ifdo_tmp[self.imageSetHeaderKey])
        except miqtc.IfdoException as ex:
            msg = "Invalid header field: " + str(ex)
            self.prov.log("Exception: " + msg, dontShow=True)
            raise miqtc.IfdoException(msg)

        # put item info into self.ifdo_tmp
        s = miqtc.PrintLoadingMsg("Updating iFDO")
        log = miqtc.recursivelyUpdateDicts(self.ifdo_tmp[self.imageSetItemsKey], image_set_items)
        s.stop()
        self.prov.log(log)

        # set lat lon bounding box
        self._set_lat_lon_bounding_box(self.ifdo_tmp)

        # set representative header fields datetime, lat, lon, alt
        self._set_rep_header_fields_dt_lat_lon_alt(self.ifdo_tmp)

        self._set_image_item_identification_scheme(self.ifdo_tmp)

        # remove emtpy fields
        s = miqtc.PrintLoadingMsg("Removing empty fields")
        self.ifdo_tmp = miqtc.recursivelyRemoveEmptyFields(self.ifdo_tmp)

        if not self.imageSetItemsKey in self.ifdo_tmp:
            self.ifdo_tmp[self.imageSetItemsKey] = []
        # remove fields that contain 'image-datetime' only
        self.removeItemFieldsWithOnlyDateTime()
        s.stop()

        if not self.ignore_image_files:
            self.checkAllItemHashes()

        # check against schema
        valid, msg = miqtt.validate_ifdo(self.ifdo_tmp)
        if not valid and not allow_missing_required:
            self.prov.log("Warning! iFDO no valid yet: " + msg)
            raise miqtc.IfdoException(msg)

        

        # set final one
        self.ifdo_checked = copy.deepcopy(self.ifdo_tmp)
        return self.ifdo_checked


    def _set_image_item_identification_scheme(self,ifdo:dict):
        """ Set image-item-identification-scheme to `image-project_image-event_image-sensor_image-datetime.ext` if empty. """
        if findField(ifdo[self.imageSetHeaderKey],'image-item-identification-scheme') == "":
            ifdo[self.imageSetHeaderKey]['image-item-identification-scheme'] =  'image-project_image-event_image-sensor_image-datetime.ext'


    def _set_rep_header_fields_dt_lat_lon_alt(self,ifdo:dict):
        """ Fill header fields image-datetime and -latitude, -longituede, -altitude-meters, -coordinate-uncertainty-meters, if empty,
        representatively with first items entry and median of all items values, respectively. """

        # 'image-datetime'
        first_image = sorted(ifdo[self.imageSetItemsKey].keys())[0]
        field = 'image-datetime'
        if findField(ifdo[self.imageSetHeaderKey],field) == "":
            try:
                ifdo[self.imageSetHeaderKey][field] = self.__getFieldValue(ifdo,[first_image,field],default_only=True)
                self.prov.log("Set representative header field '" + field + "' to " + str(ifdo[self.imageSetHeaderKey][field]) + " from first image.")
            except miqtc.IfdoException as ex:
                self.prov.log("Could not set representative header field: " + str(ex))
                pass

        # rest
        rep_header_fields_median = ['image-latitude','image-longitude','image-altitude-meters','image-coordinate-uncertainty-meters']
        for field in rep_header_fields_median:
            if findField(ifdo[self.imageSetHeaderKey],field) == "":
                values = []
                for image_name in ifdo[self.imageSetItemsKey].keys():
                    try:
                        item_val = self.__getFieldValue(ifdo,[image_name,field])
                        if isinstance(item_val,dict):
                            values += list(item_val.values())
                        else:
                            values.append(item_val)
                    except miqtc.IfdoException as ex:
                        pass
                values = [i for i in values if i != '']
                if len(values) == 0:
                    self.prov.log("Could not set representative header field, no values found: " + field)
                else:
                    # ignore unknonw, i.e. 0.0, values
                    values = [i for i in values if i != 0.0]
                    if len(values) == 0:
                        values.append(0.0) 
                    ifdo[self.imageSetHeaderKey][field] = statistics.median(values)
                    self.prov.log("Set representative header field '" + field + "' to median: " + str(ifdo[self.imageSetHeaderKey][field]) + ".")


    def _set_lat_lon_bounding_box(self,ifdo:dict):
        """ Set image-set-[min,max]-[latitude,longitude]-degrees """
        lat_min, lat_max, lon_min, lon_max = self._get_lat_lon_bounding_box(ifdo[self.imageSetItemsKey])
        if not None in [lat_min, lat_max, lon_min, lon_max]:
            ifdo[self.imageSetHeaderKey]['image-set-min-latitude-degrees'] = lat_min
            ifdo[self.imageSetHeaderKey]['image-set-max-latitude-degrees'] = lat_max
            ifdo[self.imageSetHeaderKey]['image-set-min-longitude-degrees'] = lon_min
            ifdo[self.imageSetHeaderKey]['image-set-max-longitude-degrees'] = lon_max


    @staticmethod
    def _get_lat_lon_bounding_box(items:dict):
        """ Returns lat_min, lat_max, lon_min, lon_max """
        lat_min, lat_max, lon_min, lon_max = None, None, None, None
        i = 0
        for image, data in items.items():
            # make image entry list (also if its a picture)
            if not isinstance(data, list):
                data = [data]
            
            for timepoint_data in data:
                try:
                    lat = timepoint_data['image-latitude']
                    lon = timepoint_data['image-longitude']
                except KeyError as ex:
                    continue

                if i == 0:
                    lat_min, lat_max = lat, lat
                    lon_min, lon_max = lon, lon
                else:
                    if lat < lat_min:
                        lat_min = lat
                    if lat > lat_max:
                        lat_max = lat
                    if lon < lon_min:
                        lon_min = lon
                    if lon > lon_max:
                        lon_max = lon
                i += 1
        return lat_min, lat_max, lon_min, lon_max


    def removeItemFieldsWithOnlyDateTime(self):
        """ it can happen that an image timestamp does not contain any fields but the timestamp any more. Those are removed here. """ 
        for item in self.ifdo_tmp[self.imageSetItemsKey]:
            if isinstance(self.ifdo_tmp[self.imageSetItemsKey][item],list):

                toBeRemoved = []

                for entry in self.ifdo_tmp[self.imageSetItemsKey][item]:
                    if len(entry) == 1 and 'image-datetime' in entry:
                        toBeRemoved.append(entry)
                for entry in toBeRemoved:
                    self.ifdo_tmp[self.imageSetItemsKey][item].remove(entry) 


    def checkAllItemHashes(self, hard=False, raiseException = True):
        """ 
        Checks if hashes in iFDO match hashes in intermeidate hash file if the latter was changed last after the images has changed.
        Otherwise or if hard==True it redetermines the actuall file's hash and compares the iFDO item's hash with that.
        If hashes do not match a mariqt.core.IfdoException is risen unsless raiseException == False, then a list of lists [<file>,<exception>] is returned.
        """
        hashes = {}
        hashFileModTime = 10e+100
        if os.path.exists(self.get_int_hash_file()):
            hashes = miqtf.tabFileData(self.get_int_hash_file(), [miqtv.col_header['mariqt']['img'], miqtv.col_header['mariqt']['hash']], key_col=miqtv.col_header['mariqt']['img'])
            hashFileModTime = os.path.getmtime(self.get_int_hash_file())

        exceptionList = []

        hashUncheckImagesInRaw = self.imagesInImagesDir()
        prog = miqtc.PrintKnownProgressMsg("Checking item hashes", len(self.ifdo_tmp[self.imageSetItemsKey]))
        for item in self.ifdo_tmp[self.imageSetItemsKey]:
            prog.progress()

            found = False
            for image in hashUncheckImagesInRaw:
                fileName = os.path.basename(image)
                if fileName == item:
                    found = True
                    if isinstance(self.ifdo_tmp[self.imageSetItemsKey][item],list): # in case of video with item as list the first entry holds the default and the hash cannot vary for the same image
                        itemEntry = self.ifdo_tmp[self.imageSetItemsKey][item][0] 
                    else:
                        itemEntry = self.ifdo_tmp[self.imageSetItemsKey][item]

                    imageModTime = os.path.getmtime(image)
                    if not hard and imageModTime < hashFileModTime:
                        if not os.path.basename(image) in hashes:
                            if raiseException:
                                raise miqtc.IfdoException(item, "not found in intermeidate hash file",self.get_int_hash_file()," run create_image_sha256_file() first") 
                            else:
                                exceptionList.append([fileName,"not found in intermeidate hash file " + str(self.get_int_hash_file())])
                        if not itemEntry['image-hash-sha256'] == hashes[os.path.basename(image)]['image-hash-sha256']:
                            if raiseException:
                                raise miqtc.IfdoException(item, "incorrect sha256 hash", itemEntry['image-hash-sha256'],"for file",fileName," run create_image_sha256_file() first")
                            else:
                                exceptionList.append([fileName,"incorrect sha256 hash"])
                    elif not itemEntry['image-hash-sha256'] == miqtc.sha256HashFile(image):
                        if raiseException:
                            raise miqtc.IfdoException(item, "incorrect sha256 hash", itemEntry['image-hash-sha256'],"for file",fileName," run create_image_sha256_file() first")
                        else:
                            exceptionList.append([fileName,"incorrect sha256 hash"])
                    break
            if found:
                del hashUncheckImagesInRaw[image]
            else:
                if raiseException:
                    raise miqtc.IfdoException( "image", item, "not found in directory's raw folder!")
                else:
                    exceptionList.append([fileName,"file not found"])
        prog.clear()
        if not raiseException:
            return exceptionList


    def create_uuid_file(self,clean=True):
        """ Creates in /intermediate a text file containing per image a created uuid (version 4).

        The UUID is only *taken* from the metadata of the images. It does not write UUIDs to the metadata in case some files are missing it.
        But, it creates a CSV file in that case that you can use together with exiftool to add the UUID to your data. Beware! this can destroy your images
        if not done properly! No guarantee is given it will work. Be careful!

        Use clean=False to not check those files again which are already found in intermediate uuid file
        """
        if miqtv.getGlobalVerbose():
            print("Creating UUID file ...")
        self.dir.createTypeFolder([self.dir.dt.intermediate.name])
        uuids = {}
        # Check whether a file with UUIDs exists, then read it
        if not clean and os.path.exists(self.get_int_uuid_file()):
            uuids = miqtf.tabFileData(self.get_int_uuid_file(), [miqtv.col_header['mariqt']['img'], miqtv.col_header['mariqt']['uuid']], key_col=miqtv.col_header['mariqt']['img'])
            
        if os.path.exists(self.imagesDir):

            missing_uuids = {}
            added_uuids = 0

            unknownFiles = []
            for file in self.imagesInImagesDir():
                file_name = os.path.basename(file)
                if file_name not in uuids:
                    unknownFiles.append(file)
                else:
                    uuids[file_name] = uuids[file_name][miqtv.col_header['mariqt']['uuid']]

            unknownFilesUUIDs = miqti.imagesContainValidUUID(unknownFiles)
            for file in unknownFilesUUIDs:
                file_name = os.path.basename(file)
                if not unknownFilesUUIDs[file]['valid']:
                    uuid = miqtc.uuid4()
                    missing_uuids[file] = uuid
                else:
                    uuids[file_name] = unknownFilesUUIDs[file]['uuid']
                    added_uuids += 1

            # If previously unknown UUIDs were found in the file headers, add them to the UUID file
            if added_uuids > 0:
                res = open(self.get_int_uuid_file(), "w")
                res.write(miqtv.col_header['mariqt']['img'] +"\t"+miqtv.col_header['mariqt']['uuid']+"\n")
                files_sorted = list(uuids.keys())
                files_sorted.sort()
                for file in files_sorted:
                    res.write(file+"\t"+str(uuids[file])+"\n")
                res.close()

            if len(missing_uuids) > 0:
                ecsv_path = self.__get_int_file_prefix() + "_exif-add-uuid.csv"
                csv = open(ecsv_path, "w")
                csv.write(miqtv.col_header['exif']['img'] +
                          ","+miqtv.col_header['exif']['uuid']+"\n")
                different_paths = []
                for img in missing_uuids:
                    if os.path.basename(img) not in different_paths:
                        different_paths.append(os.path.basename(img))
                    csv.write(img+","+str(missing_uuids[img])+"\n")
                #return False, "exiftool -csv="+ecsv_path+" "+" ".join(different_paths)
                return False, "Not all images have valid UUIDs. Missing for following files:\n" + '\n'.join(different_paths)
            
            self.__allUUIDsChecked = True
            return True, "All images have a UUID"
        return False, "Path "+self.imagesDir + " not found."


    def createUUIDFile(self,clean=True):
        """ Deprecated - use create_uuid_file """
        return self.create_uuid_file(clean)


    def set_image_set_attitude(self,yaw_frame:float,pitch_frame:float,roll_frame:float,yaw_cam2frame:float,pitch_cam2frame:float,roll_cam2frame:float):
        """ calculates the the cameras absolute attitude and sets it to image set header. All angles are expected in degrees. 
        camera2frame angles: rotation of camera coordinates (x,y,z = top, right, line of sight) with respect to vehicle coordinates (x,y,z = forward,right,down) 
        in accordance with the yaw,pitch,roll rotation order convention:

        1. yaw around z,
        2. pitch around rotated y,
        3. roll around rotated x

        Rotation directions according to \'right-hand rule\'.

        I.e. camera2Frame angles = 0,0,0 camera is facing downward with top side towards vehicle's forward direction' """

        R_frame2ned = miqtg.R_YawPitchRoll(yaw_frame,pitch_frame,roll_frame)
        R_cam2frame = miqtg.R_YawPitchRoll(yaw_cam2frame,pitch_cam2frame,roll_cam2frame)
        R_cam2ned = R_frame2ned.dot(R_cam2frame)
        yaw,pitch,roll = miqtg.yawPitchRoll(R_cam2ned)

        # pose matrix cam2utm
        R_camStd2utm = self.get_R_camStd2utm(R_cam2frame,R_frame2ned)

        """
        x = np.array([1,0,0])
        y = np.array([0,1,0])
        z = np.array([0,0,1])
        print('x',R_camStd2utm.dot(x).round(5))
        print('y',R_camStd2utm.dot(y).round(5))
        print('z',R_camStd2utm.dot(z).round(5))
        """

        headerUpdate = {
            miqtv.col_header['mariqt']['yaw']:yaw,
            miqtv.col_header['mariqt']['pitch']:pitch,
            miqtv.col_header['mariqt']['roll']:roll,
            miqtv.col_header['mariqt']['pose']:{'pose-absolute-orientation-utm-matrix':R_camStd2utm.flatten().tolist()}
        }
        self.update_ifdo_header_fields(headerUpdate)

    def setImageSetAttitude(self,yaw_frame:float,pitch_frame:float,roll_frame:float,yaw_cam2frame:float,pitch_cam2frame:float,roll_cam2frame:float):
        """ Deprecated - use set_image_set_attitude """
        self.set_image_set_attitude(yaw_frame, pitch_frame, roll_frame, yaw_cam2frame, pitch_cam2frame, roll_cam2frame)


    def create_image_attitude_file(self, att_path:str, frame_att_header:dict, camera2Frame_yaw:float,camera2Frame_pitch:float,camera2Frame_roll:float,
                                date_format=miqtv.date_formats['pangaea'], const_values = {}, overwrite=False, col_separator = "\t",
                                att_path_angles_in_rad = False, videoSampleSeconds=1,records2beInverted=[]):
        """ Creates in /intermediate a text file with camera attitude data for each image. All angles are expected in degrees. Use att_path_angles_in_rad if necessary. 
        camera2Frame angles: rotation of camera coordinates (x,y,z = top, right, line of sight) with respect to vehicle coordinates (x,y,z = forward,right,down) 
        in accordance with the yaw,pitch,roll rotation order convention:
        1. yaw around z,
        2. pitch around rotated y,
        3. roll around rotated x

        Rotation directions according to \'right-hand rule\'.

        I.e. camera2Frame angles = 0,0,0 camera is facing downward with top side towards vehicle's forward direction' """

        int_attutude_file = self.__get_int_file_prefix() + '_image-attitude.txt'
        output_header_att = {   miqtv.col_header['mariqt']['img']:  miqtv.col_header['mariqt']['img'],
                                miqtv.col_header['mariqt']['utc']:miqtv.col_header['mariqt']['utc'],
                                miqtv.col_header['mariqt']['yaw']:miqtv.col_header['mariqt']['yaw'],
                                miqtv.col_header['mariqt']['pitch']:miqtv.col_header['mariqt']['pitch'],
                                miqtv.col_header['mariqt']['roll']:miqtv.col_header['mariqt']['roll'],
                            }

        int_pose_file = self.__get_int_file_prefix() + '_image-camera-pose.txt'
        output_header_pose = {  miqtv.col_header['mariqt']['img']:miqtv.col_header['mariqt']['img'],
                                miqtv.col_header['mariqt']['utc']:miqtv.col_header['mariqt']['utc'],
                                miqtv.col_header['mariqt']['pose']:miqtv.col_header['mariqt']['pose'],
                            }

        if os.path.exists(int_attutude_file) and not overwrite:
            self.add_item_info_tab_file(int_attutude_file,"\t",output_header_att)
            extra_msg = ""
            if os.path.exists(int_pose_file):
                self.add_item_info_tab_file(int_pose_file,"\t",output_header_pose)
                extra_msg = ", " + int_pose_file
            return True, "Output file exists: "+int_attutude_file + extra_msg

        if not os.path.exists(att_path):
            return False, "Attitude file not found: "+att_path

        if not os.path.exists(self.imagesDir):
            return False, "Image folder not found: "+ self.imagesDir

        s = miqtc.PrintLoadingMsg("Creating items' attitude data")

        # load frame attitude data from file
        att_data, parseMsg = miqtn.readAllAttitudesFromFilePath(att_path, frame_att_header, date_format,col_separator=col_separator,const_values=const_values,anglesInRad=att_path_angles_in_rad)
        if parseMsg != "":
            self.prov.log(parseMsg,dontShow=True)
            parseMsg = "\n" + parseMsg

        # find for each image the respective navigation data
        s.stop()
        success, image_dts, msg = self.findNavDataForImage(att_data,videoSampleSeconds)
        if not success:
            return False, msg + parseMsg
        s = miqtc.PrintLoadingMsg("Creating items' attitude data")

        # invert values (if needed) before leverarm compensation
        if records2beInverted != []:
            for file in image_dts:
                attitudes = image_dts[file]
                for i in range(len(attitudes)):
                    if 'yaw' in  records2beInverted:
                        attitudes[i].yaw *= -1
                    if 'pitch' in  records2beInverted:
                        attitudes[i].pitch *= -1
                    if 'roll' in  records2beInverted:
                        attitudes[i].roll *= -1


        # add camera2Frame angles
        R_cam2frame = miqtg.R_YawPitchRoll(camera2Frame_yaw,camera2Frame_pitch,camera2Frame_roll)
        R_cam2utm_list = []
        for file in image_dts:
            for timepoint in image_dts[file]:
                attitude = timepoint
                if attitude.yaw is None or attitude.pitch is None or attitude.roll is None:
                    R_cam2utm_list.append("")
                    continue
                R_frame2ned = miqtg.R_YawPitchRoll(attitude.yaw,attitude.pitch,attitude.roll)
                R_cam2ned = R_frame2ned.dot(R_cam2frame)
                yaw,pitch,roll = miqtg.yawPitchRoll(R_cam2ned)
                attitude.yaw = yaw
                attitude.pitch = pitch
                attitude.roll = roll

                R_camStd2utm = self.get_R_camStd2utm(R_cam2frame,R_frame2ned)
                R_cam2utm_list.append(R_camStd2utm.flatten().tolist())

        self.prov.log("applied frame to camera rotation yaw,pitch,roll = " + str(camera2Frame_yaw) + "," + str(camera2Frame_pitch) + "," + str(camera2Frame_roll),dontShow=True)

        if len(image_dts) > 0:

            # Write to navigation txt file
            # header
            res = open(int_attutude_file, "w")
            res.write(miqtv.col_header['mariqt']['img']+"\t"+miqtv.col_header['mariqt']['utc'])
            res.write("\t"+miqtv.col_header['mariqt']['yaw'])
            res.write("\t"+miqtv.col_header['mariqt']['pitch'])
            res.write("\t"+miqtv.col_header['mariqt']['roll'])

            res.write("\n")
            # data lines
            for file in image_dts:
                for timepoint in image_dts[file]:
                    res.write(file+"\t"+timepoint.dateTime().strftime(miqtv.date_formats['mariqt'])) 
                    val = timepoint.yaw
                    res.write("\t"+str(val))
                    val = timepoint.pitch
                    res.write("\t"+str(val))
                    val = timepoint.roll
                    res.write("\t"+str(val))
                    res.write("\n")
            res.close()

            self.prov.addArgument("inputAttitudeFile",att_path,overwrite=True)
            self.prov.log("parsed from inputAttitudeFile: " + str(frame_att_header),dontShow=True)
            self.add_item_info_tab_file(int_attutude_file,"\t",output_header_att)

            # Write to pose txt file
            # header
            res = open(int_pose_file, "w")
            res.write(miqtv.col_header['mariqt']['img']+"\t"+miqtv.col_header['mariqt']['utc'])
            res.write("\t"+miqtv.col_header['mariqt']['pose'])
            res.write("\n")
            # data lines
            i = 0
            for file in image_dts:
                for timepoint in image_dts[file]:
                    if R_cam2utm_list[i] == "":
                        i += 1
                        continue
                    res.write(file+"\t"+timepoint.dateTime().strftime(miqtv.date_formats['mariqt'])) 
                    entry = str({'pose-absolute-orientation-utm-matrix':R_cam2utm_list[i]}).replace('\n','')
                    res.write("\t"+entry)
                    i += 1
                    res.write("\n")
            res.close()
            self.add_item_info_tab_file(int_pose_file,"\t",output_header_pose)
            s.stop()
            return True, "Attitude data created" + parseMsg
        else:
            s.stop()
            return False, "No image attitudes found" + parseMsg
        
        
    def createImageAttitudeFile(self, att_path:str, frame_att_header:dict, camera2Frame_yaw:float,camera2Frame_pitch:float,camera2Frame_roll:float,
                                date_format=miqtv.date_formats['pangaea'], const_values = {}, overwrite=False, col_separator = "\t",
                                att_path_angles_in_rad = False, videoSampleSeconds=1,records2beInverted=[]):
        """ Deprecatde - use create_image_attitude_file """
        return self.create_image_attitude_file(att_path, frame_att_header, camera2Frame_yaw, camera2Frame_pitch, camera2Frame_roll, 
                                               date_format, const_values, overwrite, col_separator, att_path_angles_in_rad, videoSampleSeconds,
                                               records2beInverted)
        

    def get_R_camStd2utm(self,R_cam2frame:np.array,R_frame2ned:np.array):
        """ retrun rotation matrix R tranforming from camStd: (x,y,z = right,buttom,line of sight) to utm (x,y,z = easting,northing,up) """
        R_camiFDO2camStd = miqtg.R_YawPitchRoll(90,0,0) # in iFDO cam: (x,y,z = top,right,line of sight) but for pose the 'standard' camStd: (x,y,z = right,buttom,line of sight) is expected
        R_camStd2frame = R_cam2frame.dot(R_camiFDO2camStd)
        R_camStd2ned = R_frame2ned.dot(R_camStd2frame)
        R_ned2utm = miqtg.R_XYZ(180,0,90) # with utm x,y,z = easting,northing,up
        R_camStd2utm = R_ned2utm.dot(R_camStd2ned).round(5)
        return R_camStd2utm


    def findNavDataForImage(self,data:miqtg.NumDataTimeStamped,videoSampleSeconds=1):
        """ creates a dict (image_dts) with file name as key and a list of data elements as value. 
            In case of photos the list has only a single entry, for videos it has video duration [sec] / videoSampleSeconds entries.
            Returns success, image_dts, msg """

        if videoSampleSeconds <= 0:
            raise Exception("findNavDataForImage: videoSampleSeconds must be greater 0")

        # create sorted time points
        time_points = list(data.keys())
        time_points.sort()
        unmatchedTimePoints = []
        image_dts = {}
        startSearchIndex = 0
        imagesInRaw =  self.imagesInImagesDir()
        imagesInRawSortedList = self.imagesInImagesDirSortedList()
        prog = miqtc.PrintKnownProgressMsg("Interpolating navigation for image", len(imagesInRaw),modulo=1)
        for file in imagesInRawSortedList:
            prog.progress()
            file_name = os.path.basename(file)

            dt_image = miqtc.parseFileDateTimeAsUTC(file_name)
            dt_image_ts = int(dt_image.timestamp() * 1000)

            runTime = imagesInRaw[file][1] # -1 for photos
            # video
            if imagesInRaw[file][2] in miqtv.video_types and runTime <= 0: # ext
                print("Caution! Could not read video run time from file",file) # TODO does this happen? Handle better?

            sampleTimeSecs = 0
            pos_list = []
            go = True
            while go:
                try:                    
                    pos, startSearchIndex = data.interpolateAtTime(dt_image_ts + sampleTimeSecs * 1000,time_points,startSearchIndex)
                    
                    # interpolateAtTime returns None values if time out of range
                    if pos.cotainsNoneValuesInRequiredFields():
                        unmatchedTimePoints.append((dt_image_ts + sampleTimeSecs * 1000)/1000)
                    else:
                        pos_list.append(pos)
                except Exception as e:
                    return False, image_dts, "Could not find image time "+ datetime.datetime.utcfromtimestamp((dt_image_ts + sampleTimeSecs * 1000)/1000).strftime(miqtv.date_formats['mariqt']) +" in "+str(data.len())+" data positions" + str(e.args)
                sampleTimeSecs += videoSampleSeconds
                if sampleTimeSecs > runTime:
                    go = False
            
            image_dts[file_name] = pos_list
        prog.clear()
        returnMsg = ""
        if len(unmatchedTimePoints) != 0:
            unmatchedTimePoints.sort()
            unmatchedTimePoints = [datetime.datetime.utcfromtimestamp(ts).strftime(miqtv.date_formats['mariqt']) for ts in unmatchedTimePoints]
            returnMsg = "Caution! Navigation not found for the following image time points. Double check or provide at least static default navigation in header fields."
            returnMsg += "\n" + "\n".join(unmatchedTimePoints)
        return True, image_dts, returnMsg


    def create_image_navigation_file(self, nav_path: str, nav_header=miqtv.pos_header['pangaea'], date_format=miqtv.date_formats['pangaea'], overwrite=False, col_separator = "\t", videoSampleSeconds=1,
                                    offset_x=0, offset_y=0, offset_z=0,angles_in_rad = False, records2beInverted=[]):
        """ Creates in /intermediate a text file with 4.5D navigation data for each image, i.e. a single row per photo, video duration [sec] / videoSampleSeconds rows per video.
            nav_header must be dict containing the keys 'utc','lat','lon','dep'(or 'alt'), optional: 'hgt','uncert' with the respective column headers as values 
            if one of the vehicle x,y,z offsets [m] is not 0 and nav_header also contains 'yaw','pitch','roll' leverarm offsets are compensated for """
        
        self.dir.createTypeFolder([self.dir.dt.intermediate.name])

        if self.intermediateNavFileExists() and not overwrite:
            return True, "Output file exists: "+self.get_int_nav_file()

        if not os.path.exists(nav_path):
            return False, "Navigation file not found: "+nav_path

        if not os.path.exists(self.imagesDir):
            return False, "Image folder not found: "+ self.imagesDir

        s = miqtc.PrintLoadingMsg("Creating items' navigation data")
        returnMsg = ""
        compensatOffsets = False
        if (offset_x!=0 or offset_y!=0 or offset_z!=0) and 'yaw' in nav_header and 'pitch' in nav_header and 'roll' in nav_header:
            compensatOffsets = True

        # check if for missing fields there are const values in header
        const_values = {}
        for navField in miqtv.pos_header['mariqt']:
            respectiveHeaderField = miqtv.col_header["mariqt"][navField]
            if navField not in nav_header and (respectiveHeaderField in self.ifdo_tmp[self.imageSetHeaderKey] and self.findTmpField2(respectiveHeaderField) != ""): 
                const_values[navField] = self.findTmpField(respectiveHeaderField)

         # handle alt vs dep
        if 'alt' in nav_header and 'dep' in nav_header:
            raise miqtc.IfdoException("'alt' and 'dep' provided. Redundant, alt = - dep. Provided only one of both.")
        
        # Load navigation data (if 'alt' instead of 'dep', its automatically inverted)
        nav_data, parseMsg = miqtn.readAllPositionsFromFilePath(nav_path, nav_header, date_format,col_separator=col_separator,const_values=const_values)
        if parseMsg != "":
            self.prov.log(parseMsg,dontShow=True)
            returnMsg = "\n" + parseMsg

        # find for each image the respective navigation data
        s.stop()
        success, image_dts, msg = self.findNavDataForImage(nav_data,videoSampleSeconds)
        self.prov.log(msg,dontShow=True)
        if msg != "":
            returnMsg += "\n" + msg
        if not success:
            return False, returnMsg
        s = miqtc.PrintLoadingMsg("Creating items' navigation data")

        # invert values (if needed) before leverarm compensation
        if records2beInverted != []:
            for file in image_dts:
                positions = image_dts[file]
                for i in range(len(positions)):
                    if 'lat' in records2beInverted:
                        positions[i].lat *= -1
                    if 'lon' in records2beInverted:
                        positions[i].lon *= -1
                    if ('dep' in records2beInverted and 'dep' in nav_header) or ('alt' in records2beInverted and 'alt' in nav_header):
                        positions[i].dep *= -1
                    if 'hgt' in records2beInverted:
                        positions[i].hgt *= -1


        # compensate leverarm offsets
        if compensatOffsets:

            # load frame attitude data from file
            att_data, parseMsg = miqtn.readAllAttitudesFromFilePath(nav_path, nav_header, date_format,col_separator=col_separator,const_values=const_values,anglesInRad=angles_in_rad)
            if parseMsg != "":
                self.prov.log(parseMsg,dontShow=True)
                returnMsg += "\n" + parseMsg

            if records2beInverted != []:
                for file in image_dts:
                    attitudes = image_dts_att[file]
                    for i in range(len(positions)):
                        if 'yaw' in  records2beInverted:
                            attitudes[i].yaw *= -1
                        if 'pitch' in  records2beInverted:
                            attitudes[i].pitch *= -1
                        if 'roll' in  records2beInverted:
                            attitudes[i].roll *= -1

            # find for each image the respective navigation data
            success, image_dts_att, msg = self.findNavDataForImage(att_data,videoSampleSeconds)
            self.prov.log(msg,dontShow=True)
            if msg != "":
                returnMsg += "\n" + msg
            if not success:
                return False, returnMsg

            # compensate
            for file in image_dts:
                positions = image_dts[file]
                attitudes = image_dts_att[file]
                for i in range(len(positions)):
                    lat = positions[i].lat
                    lon = positions[i].lon
                    dep = positions[i].dep
                    hgt = positions[i].hgt
                    yaw = attitudes[i].yaw
                    pitch = attitudes[i].pitch
                    roll = attitudes[i].roll
                    if yaw is None or pitch is None or roll is None:
                        continue
                    new_lat,new_lon,new_dep,new_hgt = miqtg.addLeverarms2LatLonDepAlt(lat,lon,dep,hgt,offset_x,offset_y,offset_z,yaw,pitch,roll)
                    positions[i].lat = new_lat
                    positions[i].lon = new_lon
                    positions[i].dep = new_dep
                    positions[i].hgt = new_hgt

            self.prov.log("applied lever arm compensation x,y,z = " + str(offset_x) + "," + str(offset_y) + "," + str(offset_z),dontShow=True)

        if len(image_dts) > 0:
            # Check whether depth and height are set
            lat_identical, lon_identical, dep_identical, hgt_identical, dep_not_zero, hgt_not_zero,uncert_not_zero = nav_data.checkPositionsContent()

            # Write to navigation txt file
            # header
            res = open(self.get_int_nav_file(), "w")
            res.write(miqtv.col_header['mariqt']['img']+"\t"+miqtv.col_header['mariqt']['utc'])

            has_alt = True if dep_not_zero and ( 'dep' in nav_header or 'alt' in nav_header ) else False

            if 'lat' in nav_header:
                res.write("\t"+miqtv.col_header['mariqt']['lat'])
            if 'lon' in nav_header:
                res.write("\t"+miqtv.col_header['mariqt']['lon'])
            if has_alt:
                res.write("\t"+miqtv.col_header['mariqt']['alt'])
            if hgt_not_zero and 'hgt' in nav_header:
                res.write("\t"+miqtv.col_header['mariqt']['hgt'])
            if uncert_not_zero and 'uncert' in nav_header:
                res.write("\t"+miqtv.col_header['mariqt']['uncert'])
            res.write("\n")
            # data lines
            for file in image_dts:
                for timepoint in image_dts[file]:
                    res.write(file+"\t"+timepoint.dateTime().strftime(miqtv.date_formats['mariqt'])) 
                    if 'lat' in nav_header:
                        val = timepoint.lat
                        res.write("\t"+str(val))
                    if 'lon' in nav_header:
                        val = timepoint.lon
                        res.write("\t"+str(val))
                    if has_alt:
                        val = timepoint.dep
                        # dep to alt
                        val *= -1
                        res.write("\t"+str(val))
                    if hgt_not_zero and 'hgt' in nav_header:
                        val = timepoint.hgt
                        res.write("\t"+str(val))
                    if uncert_not_zero and 'uncert' in nav_header:
                        val = timepoint.uncert
                        res.write("\t"+str(val))
                    res.write("\n")
            res.close()

            # Write to geojson file
            geojson = {'type': 'FeatureCollection', 'name': self.dir.event()+"_"+self.dir.sensor()+"_image-navigation", 'features': []}
            for file in image_dts:
                # photo
                if len(image_dts[file]) == 1:
                    if dep_not_zero:
                        geometry =  {'type': "Point", 'coordinates': 
                                        [float(image_dts[file][0].lon), float(image_dts[file][0].lat), -1*float(image_dts[file][0].dep)]
                                    }
                    else:
                        geometry =  {'type': "Point", 'coordinates': 
                                        [float(image_dts[file][0].lon), float(image_dts[file][0].lat)]
                                    }
                    if True in [math.isnan(x) for x in geometry['coordinates']]:
                        continue

                # video
                else:
                    if dep_not_zero:
                        geometry =  {'type': "MultiPoint", 'coordinates':
                                        [[float(d.lon), float(d.lat), -1*float(d.dep)] for d in image_dts[file]]
                                    }
                    else:
                        geometry =  {'type': "MultiPoint", 'coordinates':
                                        [[float(d.lon), float(d.lat)] for d in image_dts[file]]
                                    }
                    if True in [math.isnan(x) for x in [item for sublist in geometry['coordinates'] for item in sublist]]:
                        continue

                geojson['features'].append({'type': 'Feature', 'properties': {'id': file}, 'geometry': geometry })
                
            o = open(self.get_int_nav_file().replace(".txt", ".geojson"),
                     "w", errors="ignore", encoding='utf-8')
            json.dump(geojson, o, ensure_ascii=False, indent=4)
            o.close()

            self.prov.addArgument("inputNavigationFile",nav_path,overwrite=True)
            self.prov.log("parsed from inputNavigationFile: " + str(nav_header),dontShow=True)
            s.stop()
            return True, "Navigation data created" + returnMsg
        else:
            s.stop()
            return False, "No image coordinates found" + returnMsg

    def createImageNavigationFile(self, nav_path: str, nav_header=miqtv.pos_header['pangaea'], date_format=miqtv.date_formats['pangaea'], overwrite=False, col_separator = "\t", videoSampleSeconds=1,
                                    offset_x=0, offset_y=0, offset_z=0,angles_in_rad = False, records2beInverted=[]):
        """ Deprecated - use create_image_navigation_file """
        return self.create_image_navigation_file(nav_path, nav_header, date_format, overwrite, col_separator, videoSampleSeconds, offset_x, offset_y, offset_z, angles_in_rad, records2beInverted)


    def create_image_sha256_file(self,reReadAll=True):
        """ Creates in /intermediate a text file containing per image its SHA256 hash.
            If reReadAll is True all images' hashes are determined. Otherwise only for those files
            which are not yet in the intermediate file containing the image hashes  """
        if miqtv.getGlobalVerbose():
            print("Creating intermediate hash file ...")
        self.dir.createTypeFolder([self.dir.dt.intermediate.name])
        hashes = {}
        if os.path.exists(self.get_int_hash_file()):
            hashes = miqtf.tabFileData(self.get_int_hash_file(), [miqtv.col_header['mariqt']['img'], miqtv.col_header['mariqt']['hash']], key_col=miqtv.col_header['mariqt']['img'])
            msg_0 = "Loaded " + str(len(hashes)) + " hahes from " + os.path.basename(self.get_int_hash_file())
            msg_reRedaAll = msg_0 + " - but re-calculating all hashes anyway"
            msg_not_reRedaAll = msg_0 + " - calculating only missing hashes"
            if reReadAll:
                self.prov.log(msg_reRedaAll)
            else:
                self.prov.log(msg_not_reRedaAll)

        imagesInRaw = self.imagesInImagesDir()
        if len(imagesInRaw) > 0:

            added_hashes = 0
            if self.__allUUIDsChecked:
                prog = miqtc.PrintKnownProgressMsg("Checking hashes", len(imagesInRaw),modulo=1)
            else:
                prog = miqtc.PrintKnownProgressMsg("Checking uuids and hashes", len(imagesInRaw),modulo=1)
            for file in imagesInRaw:
                prog.progress()

                if not self.__allUUIDsChecked and not miqti.imageContainsValidUUID(file)[0]:
                    # remove from uuid file
                    if os.path.exists(self.get_int_uuid_file()):
                        res = open(self.get_int_uuid_file(), "r")
                        lines = res.readlines()
                        res.close()
                    else:
                        lines = []
                    i = 0
                    lineNr = i
                    for line in lines:
                        if os.path.basename(file) in line:
                            lineNr = i
                            break
                        i += 1
                    if lineNr != 0:
                        del lines[lineNr]
                        res = open(self.get_int_uuid_file(), "w")
                        res.writelines(lines)
                        res.close()
                    raise Exception( "File " + file + " does not cotain a valid UUID. Run create_uuid_file() first!")

                file_name = os.path.basename(file)
                if not reReadAll and file_name in hashes:
                    hashes[file_name] = hashes[file_name][miqtv.col_header['mariqt']['hash']]
                else:
                    hashes[file_name] = miqtc.sha256HashFile(file)
                    added_hashes += 1
            prog.clear()

            if reReadAll or added_hashes > 0:
                hash_file = open(self.get_int_hash_file(), "w")
                hash_file.write( miqtv.col_header['mariqt']['img']+"\t"+miqtv.col_header['mariqt']['hash']+"\n")
                files_sorted = list(hashes.keys())
                files_sorted.sort()
                for file_name in files_sorted:
                    hash_file.write(file_name+"\t"+hashes[file_name]+"\n")

                hash_file.close()
                return True, "Added "+str(added_hashes)+" hashes to hash file"
            else:
                return True, "All hashes exist"

        else:
            return False, "No images found to hash"
        
    def createImageSHA256File(self,reReadAll=True):
        """ Deprecated - use create_image_sha256_file """
        return self.create_image_sha256_file(reReadAll)


    def create_start_time_file(self):
        """ Creates in /intermediate a text file containing per image its start time parsed from the file name """
        self.dir.createTypeFolder([self.dir.dt.intermediate.name])
        s = miqtc.PrintLoadingMsg("Creating intermediate start time file ")
        imagesInRaw = self.imagesInImagesDirSortedList()
        if len(imagesInRaw) > 0:

            o = open(self.get_int_startTimes_file(), "w")
            o.write(miqtv.col_header['mariqt']['img'] +
                    "\t"+miqtv.col_header['mariqt']['utc']+"\n")

            for file in imagesInRaw:
                file_name = os.path.basename(file)

                dt = miqtc.parseFileDateTimeAsUTC(file_name)
                o.write(file_name+"\t" + dt.strftime(miqtv.date_formats['mariqt'])+"\n")

            o.close()
            s.stop()
            return True, "Created start time file"
        else:
            s.stop()
            return False, "No images found to read start times"
        
    def createStartTimeFile(self):
        """ Deprecated - use create_start_time_file """
        return self.create_start_time_file()


    def createAcquisitionSettingsEXIFFile(self,override=False):
        """ Deprecated. Use create_acquisition_settings_exif_file() instead. """
        return self.create_acquisition_settings_exif_file(override=override)

    def create_acquisition_settings_exif_file(self,override=False):
        """ Creates in /intermediate a text file containing per image a dict of exif tags and their values parsed from the image """

        int_acquisitionSetting_file = self.__get_int_file_prefix() + '_image-acquisition-settings.txt'
        header = {  miqtv.col_header['mariqt']['img']:  miqtv.col_header['mariqt']['img'],
                    miqtv.col_header['mariqt']['acqui']:miqtv.col_header['mariqt']['acqui']}
        if os.path.exists(int_acquisitionSetting_file) and not override:
            self.add_item_info_tab_file(int_acquisitionSetting_file,"\t",header)
            return True, "Result file exists"

        imagesInRaw = self.imagesInImagesDirSortedList()
        if len(imagesInRaw) > 0:

            o = open(int_acquisitionSetting_file, "w")
            o.write(miqtv.col_header['mariqt']['img'] + "\t"+miqtv.col_header['mariqt']['acqui']+"\n")
 
            imagesExifs = miqti.getImagesAllExifValues(imagesInRaw,self.prov)
            for file in imagesExifs:
                file_name = os.path.basename(file)
                o.write(file_name+"\t"+str(imagesExifs[file])+"\n")

            o.close()

            self.add_item_info_tab_file(int_acquisitionSetting_file,"\t",header)
            return True, "Created acquisition settings file"
        else:
            return False, "No images found"


    def imagesInImagesDir(self):
        return copy.deepcopy(self._imagesInImagesDir)

    def imagesInImagesDirSortedList(self):
        return copy.deepcopy(self._imagesInImagesDirSortedList)


    def parseItemDatafromTabFileData(self, items: dict, file: str, cols: list, optional: list = [], datetime_format:str=miqtv.date_formats['mariqt']):
        """ parses data from columns in cols and writes info to items. Column 'image-filename' must be in file and does not need to be passed in cols. 
            File must be tab separated and columns names must equal item field names"""
        tmp_data = miqtf.tabFileData(file, cols+['image-filename']+optional, key_col='image-filename', optional=optional,convert=True)
        self.writeParsedDataToItems(tmp_data,items,self.ifdo_tmp[miqtv.image_set_header_key], datetime_format=datetime_format)


    def praseItemDataFromFile(self,items:dict,file:str,separator:str,header:dict, datetime_format:str=miqtv.date_formats['mariqt']):
        """ parses data from from file to items. header dict must be of structure: {<item-field-name>:<column-name>}
            and must contain entry 'image-filename' """
        if not 'image-filename' in header:
            raise Exception("header does not contain 'image-filename'")
        
        tmp_data = miqtf.tabFileData(file, header,col_separator=separator, key_col='image-filename',convert=True)
        self.writeParsedDataToItems(tmp_data,items,self.ifdo_tmp[miqtv.image_set_header_key], datetime_format=datetime_format)


    def writeParsedDataToItems(self,data:dict,items:dict,header:dict, datetime_format:str=miqtv.date_formats['mariqt']):

        # eval strings as dict or list
        miqtc.recursiveEval(data)

        data = miqtc.recursivelyRemoveEmptyFields(data,content2beRemoved=None)

        # potentailly remove const data from items and put in header
        self.extractConstDataValues(data,header)

        # add 'image-filename' field
        for img, entry in data.items():

            # list
            if isinstance(entry,list):
                for listItem in entry:
                    listItem['image-filename'] = img
                    # covert datetime string
                    if 'image-datetime' in listItem:
                        dt = datetime.datetime.strptime(listItem['image-datetime'], datetime_format)
                        listItem['image-datetime'] = dt.strftime(miqtv.date_formats['mariqt'])
            elif isinstance(entry,dict):
                entry['image-filename'] = img
                # covert datetime string
                if 'image-datetime' in entry:
                    dt = datetime.datetime.strptime(entry['image-datetime'], datetime_format)
                    entry['image-datetime'] = dt.strftime(miqtv.date_formats['mariqt'])
            else:
                raise miqtc.IfdoException("data entries must be dict or list if dicts")

        miqtc.recursivelyUpdateDicts(items,data)


    @staticmethod
    def extractConstDataValues(data:dict,header:dict):
        """ Removes fields that are constant for all entries from data dict and put them in header dict. 
            Each entry of data must be a dict with the same set of keys. """
    
        # skip if there is only one item
        if len(list(data.keys())) == 1:
            return

        fieldsToIgnore = ['image-datetime']
        constData = {}
        firstImage = True
        for image,image_data in data.items():
            
            if not isinstance(image_data,list):
                image_data = [image_data]

            if not firstImage and constData == {}:
                break
            
            firstTimePoint = True
            for image_tp_data in image_data:
                # very first data for comparison
                if firstImage and firstTimePoint:
                    constData = copy.deepcopy(image_tp_data)
                    for field in fieldsToIgnore:
                        if field in constData:
                            del constData[field]
                    firstTimePoint = False
                    continue

                constData = miqtc.findCommonDictElements(image_tp_data,constData)

            firstImage = False

        # TODO check within image times -> to image default. (tricky since we don't have the dafault index here. Only a subset might be update here)
        # check within image items -> header
        headerUpdate = copy.deepcopy(constData)
        headerUpdatedTest = copy.deepcopy(header)
        miqtc.recursivelyUpdateDicts(headerUpdatedTest,headerUpdate)
        updateDiff = DeepDiff(header,headerUpdatedTest)
        # check if headerUpdate would overwrite anything from current header (should not happen), if so dont remove from items
        if not 'values_changed' in updateDiff and not 'type_changes' in updateDiff and not 'dictionary_item_removed' in updateDiff:
            header.clear()
            header.update(headerUpdatedTest)

            # remove const values from data
            miqtc.recursiveMakeNoneDictFieldsEmptyStr(constData)
            for image,image_data in data.items():
                if not isinstance(image_data,list):
                    image_data = [image_data]
                for image_tp_data in image_data:
                    miqtc.recursivelyUpdateDicts(image_tp_data,constData)          

        else:
            pass
            # TODO log?


    @staticmethod
    def get_equipment_handle_url(ifdo:dict, ifdo_field:str, handle_prefix:str, prov:miqtp.Provenance=None ):
        """ Constructs and returns handle url from eqipment id in ifdo_field['name']. Returns "" if fails. Does not check is site is up. 
            handle_prefix prefix must be of form e.g. https://hdl.handle.net/20.500.12085 
        """
        def _log(msg:str):
            if prov is not None:
                prov.log(msg)
            else:
                print(msg)
        image_field = iFDO.find_field_str(ifdo,ifdo_field)
        if image_field == "" or 'name' not in image_field or image_field['name'] == "":
            _log("Error! Can't construct "  + ifdo_field + " uri, name not filled.")
            return ""
        return miqtc.assertSlash(handle_prefix) + miqtequip.equipmentShortName(image_field['name'])


    def set_header_equipment_uri_to_handle_url(self,ifdo_field:str, override:bool = False, ignore_offline:bool = False):
        """ Constructs equipment handle url from ifdo_field['name'] and write it to ifdo_field['uri'].
        Params:
            override: if False set only if uri is empty or does not exist.
            ignore_offline: write to ifdo_field['uri'] even if constructed url is not reachable. """
        if not override and self.findTmpField2(ifdo_field+':uri') != "":
            self.prov.log("Caution! " + ifdo_field + ":uri already exists and is not overridden: " + self.findTmpField2(ifdo_field+ ':uri'))
            return
        
        eqip_url = self.get_equipment_handle_url(self.ifdo_tmp, ifdo_field, self.handle_prefix, self.prov)
        try:
            ret = requests.head(eqip_url + '?noredirect', timeout=5) # seems not work without ?noredirect
            if ret.status_code != 200:
                raise Exception()
        except Exception:
            if not ignore_offline:
                self.prov.log("Error! " + ifdo_field + ":uri ignored, not reachable: " + eqip_url)
                return
            else:
                self.prov.log("Caution! " + ifdo_field + ":uri set but not reachable " + eqip_url)

        self.ifdo_tmp[self.imageSetHeaderKey][ifdo_field]['uri'] = eqip_url
        self.prov.log(ifdo_field + ":uri set to " + eqip_url)
        

    @staticmethod
    def get_header_equipment_uri_to_equipment_git_url(ifdo:dict, ifdo_field:str, prov:miqtp.Provenance=None):
        """ DEPRECATED: Rather use get_equipment_handle_url() instead.
        Constructs and returns equipment url from ifdo_field['name']. Returns "" if fails. Does not check is site is up. """
        warnings.warn('This method is deprecated. Rather use get_equipment_handle_url() instead.', DeprecationWarning, stacklevel=2)
        def _log(msg:str):
            if prov is not None:
                prov.log(msg)
            else:
                print(msg)

        image_field = iFDO.find_field_str(ifdo,ifdo_field)
        if image_field == "" or 'name' not in image_field or image_field['name'] == "":
            _log("Error! Can't construct "  + ifdo_field + " uri, name not filled.")
            return ""

        eqip_url = miqtequip.equipment_url(image_field['name'])
        return eqip_url
    

    def set_header_equipment_uri_to_equipment_git_url(self,ifdo_field:str, override:bool = False, ignore_offline:bool = False):
        """ DEPRECATED: Rather use set_header_equipment_uri_to_handle_url() instead.
        Constructs equipment url from ifdo_field['name'] and write it to ifdo_field['uri'].
        Params:
            override: if False set only if uri is empty or does not exist.
            ignore_offline: write to ifdo_field['uri'] even if constructed url is not reachable. """
        warnings.warn('This method is deprecated. Rather use set_header_equipment_uri_to_handle_url() instead.', DeprecationWarning, stacklevel=2)
        if not override and self.findTmpField2(ifdo_field+':uri') != "":
            self.prov.log("Caution! " + ifdo_field + ":uri already exists and is not overridden: " + self.findTmpField2(ifdo_field+ ':uri'))
            return
        
        eqip_url = self.get_header_equipment_uri_to_equipment_git_url(self.ifdo_tmp,ifdo_field,self.prov)
        try:
            ret = requests.head(eqip_url, timeout=5)
            if ret.status_code != 200:
                raise Exception()
        except Exception:
            if not ignore_offline:
                self.prov.log("Error! " + ifdo_field + ":uri ignored, not reachable: " + eqip_url)
                return
            else:
                self.prov.log("Caution! " + ifdo_field + ":uri set but not reachable " + eqip_url)

        self.ifdo_tmp[self.imageSetHeaderKey][ifdo_field]['uri'] = eqip_url
        self.prov.log(ifdo_field + ":uri set to " + eqip_url)


    @staticmethod
    def get_header_image_project_uri_to_osis_expedition_url(ifdo:dict,prov:miqtp.Provenance=None):
        """ Returns header image-project uri as osis expedition url parsed from image-project['name']."""

        def _log(msg:str):
            if prov is not None:
                prov.log(msg)
            else:
                print(msg)

        image_project = iFDO.find_field_str(ifdo,'image-project')
        if image_project == "" or 'name' not in image_project or image_project['name'] == "":
            _log("Error! Can't construct image-project uri, image-project not filled.")
            return ""
        
        # get expedition id
        try:
            expedition_id = miqtosis.get_expedition_id_from_label(image_project['name'])
        except ValueError:
            _log("Error! Can't get osis expedition id from image-project " + str(image_project))
            return ""

        expedition_url = miqtosis.get_expedition_url(expedition_id)
        return expedition_url


    def set_header_image_project_uri_to_osis_expedition_url(self,override:bool = False):
        """ Sets header image-project uri to osis expedition url parsed from image-project['name'].
        Params:
            override: if False set only if uri is empty or does not exist. """

        if not override and self.findTmpField2('image-project:uri') != "":
            self.prov.log("Caution! image-project:uri already exists and is not overridden: " + self.findTmpField2('image-project:uri'))
            return

        expedition_url = self.get_header_image_project_uri_to_osis_expedition_url(self.ifdo_tmp,self.prov)
        self.ifdo_tmp[self.imageSetHeaderKey]['image-project']['uri'] = expedition_url
        try:
            ret = requests.head(expedition_url)
            if ret.status_code != 200:
                raise Exception()
        except Exception:
            self.prov.log("Caution! image-project:uri set but not reachable " + expedition_url)
        self.prov.log("image-project:uri set to " + expedition_url)


    @staticmethod
    def get_header_image_event_uri_to_osis_event_url(ifdo:dict,prov:miqtp.Provenance=None):
        """ Returns header image-event uri as osis event url parsed from image-project and image-event['name'] or 
        image-event['uri'] if it refers to osis. Returns empty string if fails. """

        def _log(msg:str):
            if prov is not None:
                prov.log(msg)
            else:
                print(msg)

        image_project = iFDO.find_field_str(ifdo, 'image-project')
        if image_project == "" or 'name' not in image_project or image_project['name'] == "":
            _log("Error! Can't construct image-event uri, image-project not filled.")
            return ""

        # get expedition id
        ## try parse expedition id from project osis uri
        if 'uri' in image_project and image_project['uri'] != "":
            expedition_id = miqtosis.get_expedition_id_from_url(image_project['uri'])
        # get expedition id from osis api by expedition name
        else:
            try:
                expedition_id = miqtosis.get_expedition_id_from_label(image_project['name'])
            except ValueError:
                _log("Error! Can't get osis expedition id from image-project " + str(image_project))
                return ""

        # try parse event id
        event_name = iFDO.find_field_str(ifdo, 'image-event:name')
        if event_name == "":
            _log("Error! Can't construct image-event uri, image-event:name not filled.")
            return ""

        osis_url = iFDO.get_osis_event_url(expedition_id, event_name)

        if osis_url == "":
            _log("Error! Can't construct image-event uri from expedition_id and event_name: " + str(expedition_id) + ", " + event_name)
            return ""

        return osis_url


    def set_header_image_event_uri_to_osis_event_url(self,override:bool = False):
        """ Sets header image-event uri to osis event url parsed from image-project and image-event['name'] or 
        image-event['uri'] if it refers to osis.
        Params:
            override: if False set only if uri is empty or does not exist. """

        if not override and self.findTmpField2('image-event:uri') != "":
            self.prov.log("Caution! image-event:uri already exists and is not overridden: " + self.findTmpField2('image-event:uri'))
            return

        osis_url = self.get_header_image_event_uri_to_osis_event_url(self.ifdo_tmp,self.prov)
        if osis_url == "":
            return
        self.ifdo_tmp[self.imageSetHeaderKey]['image-event']['uri'] = osis_url
        try:
            ret = requests.head(osis_url)
            if ret.status_code != 200:
                raise Exception()
        except Exception:
            self.prov.log("Caution! image-event:uri set but not reachable " + osis_url)
        self.prov.log("image-event:uri set to " + osis_url)


    @staticmethod
    def get_osis_event_url(expedition_id:int, event_name:str):
        """ Returns osis event url if osis event id can be successfully retrieved from event_name.
        Returns "" if not successsful. """
        event_url = ""
        event_ids = miqtosis.get_expedition_event_ids(expedition_id)

        event_name_options = [event_name]
        event_name_options.append(event_name)
        # e.g. M182_040-1_XOFOS
        name_split = event_name.split('_')
        if len(name_split) >= 2:
            event_name_options.append(name_split[1])
        # e.g. MSM96_003_AUV-01
        if len(name_split) >= 3:
            ext_split = name_split[2].split('-')
            if len(ext_split) == 2:
                event_name_options.append(name_split[1] + '-' + ext_split[1])
        event_name_options_0strip = []
        for name in event_name_options:
            dash_split = name.split('-')
            event_name_options_0strip.append('-'.join([e.lstrip('0') for e in dash_split]))
        event_name_options += event_name_options_0strip
        for event_name in event_name_options:
            if event_name in event_ids:
                event_url = miqtosis.get_event_url(expedition_id,event_ids[event_name])
                break
        
        return event_url


    @staticmethod
    def get_license_uri(licence_name:str):
        """ Tries to guess licence url from license name and returns it. Returns "" if fails. """
        licenses_dict = {
            "ccby": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "cc0": "https://creativecommons.org/publicdomain/zero/1.0/legalcode"
        }
        cleand_license = licence_name.strip().lower().replace('-', '')
        if cleand_license in licenses_dict:
            return licenses_dict[cleand_license]
        else:
            return ""


    @staticmethod
    def get_license_uri_to_license(ifdo:dict):
        """ Returns header image-license uri guessed from license name. Returns empty string if fails. """
        image_license = iFDO.find_field_str(ifdo, 'image-license')
        if isinstance(image_license, dict):
            return iFDO.get_license_uri(image_license['name'])
        else:
            return iFDO.get_license_uri(image_license)


    def set_license_uri_from_license_name(self, override:bool = False):
        """ Sets header image-license uri to url guessed from image-license.
        Params:
            override: if False set only if uri is empty or does not exist. """
        
        if not override and self.findTmpField2('image-license:uri') != "":
            self.prov.log("Caution! image-license:uri already exists and is not overridden: " + self.findTmpField2('image-license:uri'))
            return
        
        license_url = self.get_license_uri_to_license(self.ifdo_tmp)
        if license_url == "":
            self.prov.log("Warning! Can't guess image-license:uri from name")
            return
        self.ifdo_tmp[self.imageSetHeaderKey]['image-license']['uri'] = license_url
        try:
            ret = requests.head(license_url)
            if ret.status_code != 200:
                raise Exception()
        except Exception:
            self.prov.log("Caution! image-license:uri set but not reachable " + license_url)
        self.prov.log("image-license:uri set to " + license_url)


    def intermediateNavFileExists(self):
        if os.path.exists(self.get_int_nav_file()):
            return True
        else:
            return False


    def headerFieldFilled(self,field:str):
        if self.findTmpField2(field) == "":
            return False
        return True

    def convertToDefaultDateTimeFormat(self,ifdo):
        """ Checks if all items' 'image-datetime' fields match default datetime format or a custom one defined in 'image-datetime-format'
            and converts to default format. Throws exception if datetime cannot be parsed """
        customDateTimeFormatFound = False
        headerCustomDateTimeFormat = findField(ifdo[self.imageSetHeaderKey],'image-datetime-format')
        if headerCustomDateTimeFormat != "":
            ifdo[self.imageSetHeaderKey]['image-datetime-format'] = "" # remove custom format # TODO why not keep?
            customDateTimeFormatFound = True
        prog = miqtc.PrintKnownProgressMsg("Checking datetime formats", len(ifdo[self.imageSetItemsKey]),modulo=1)
        for file,item in ifdo[self.imageSetItemsKey].items():
            prog.progress()
            if not isinstance(item,list):
                    item = [item]
            subItemDefault = item[0]
            itemCustomDateTimeFormat = ""
            if 'image-datetime-format' in subItemDefault:
                itemCustomDateTimeFormat = subItemDefault['image-datetime-format']
                subItemDefault['image-datetime-format'] = "" # remove custom format # TODO why not keep?
                customDateTimeFormatFound = True
            for subItem in item:
                try:
                    format = miqtv.date_formats['mariqt']
                    datetime.datetime.strptime(subItem['image-datetime'],format)
                except:
                    try:
                        format = headerCustomDateTimeFormat
                        dt = datetime.datetime.strptime(subItem['image-datetime'],format)
                        subItem['image-datetime'] = datetime.datetime.strftime(dt,miqtv.date_formats['mariqt'])
                    except:
                        try:
                            format = itemCustomDateTimeFormat
                            dt = datetime.datetime.strptime(subItem['image-datetime'],format)
                            subItem['image-datetime'] = datetime.datetime.strftime(dt,miqtv.date_formats['mariqt'])
                        except:
                            prog.clear()
                            raise miqtc.IfdoException('Invalid datetime value',subItem['image-datetime'], "does not match format default or custom format")
        if customDateTimeFormatFound:
            self.prov.log("Custom datetime formats found. They will be replaced by the default format.")   
        prog.clear()    


    def __initIntermediateFiles(self):
        self.intermediateFilesDef_core = {
            'hashes': {
                'creationFct': 'create_image_sha256_file()',
                'suffix': '_image-hashes.txt',
                'cols': [miqtv.col_header['mariqt']['hash']],
                'optional': []},
            'uuids': {
                'creationFct': 'create_uuid_file()',
                'suffix': '_image-uuids.txt',
                'cols': [miqtv.col_header['mariqt']['uuid']],
                'optional': []},
            'datetime': {
                'creationFct': 'create_start_time_file()',
                'suffix': '_image-start-times.txt',
                'cols': [miqtv.col_header['mariqt']['utc']],
                'optional': []},
            'navigation': {
                'creationFct': 'create_image_navigation_file()',
                'suffix': '_image-navigation.txt',
                'cols': [miqtv.col_header['mariqt']['utc']],
                'optional': [miqtv.col_header['mariqt']['lon'], miqtv.col_header['mariqt']['lat'], miqtv.col_header['mariqt']['alt'], miqtv.col_header['mariqt']['hgt'], miqtv.col_header['mariqt']['uncert']]},
        }

        self.nonCoreFieldIntermediateItemInfoFiles = []

    def __get_int_file_prefix(self):
        """ depends on 'image-event' and 'image-sensor' so it can change during upate """
        return os.path.join(self.dir.to(self.dir.dt.intermediate), self.findTmpField('image-set-name'))

    def get_int_hash_file(self):
        return self.__get_int_file_prefix() + self.intermediateFilesDef_core['hashes']['suffix']

    def get_int_uuid_file(self):
        return self.__get_int_file_prefix() + self.intermediateFilesDef_core['uuids']['suffix']

    def get_int_startTimes_file(self):
        return self.__get_int_file_prefix() + self.intermediateFilesDef_core['datetime']['suffix']

    def get_int_nav_file(self):
        return self.__get_int_file_prefix() + self.intermediateFilesDef_core['navigation']['suffix']

