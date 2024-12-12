def equipmentOwner(eqid):
	"""Returns the owner part of an equipment id (everything until the first underscore)"""
	return eqid[0:eqid.find("_")]

def equipmentType(eqid):
	"""Returns the type part of an equipment id (between the first underscore and the first dash)"""
	return eqid[eqid.find("_")+1:eqid.find("-")]

def equipmentShortName(eqid):
	"""Returns the unique short version of the id (owner_type-index)"""
	tmp = eqid.split("_")
	return tmp[0]+"_"+tmp[1]

def equipment_url(eqid):
	""" returns constructed equipment git url to https://dm.pages.geomar.de/equipment/...
	Reachability of url should be checked. """

	#e.g.: https://dm.pages.geomar.de/equipment/equipment/GMR/PFM/GMR_PFM-38_OFOS_XOFOS-Frame/
	url = 'https://dm.pages.geomar.de/equipment/equipment/' + equipmentOwner(eqid) + '/' + equipmentType(eqid) + '/' + eqid + '/'
	return url