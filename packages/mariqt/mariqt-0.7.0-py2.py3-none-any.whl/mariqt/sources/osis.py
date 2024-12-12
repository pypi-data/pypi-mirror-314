""" This file contains functionality to handle OSIS urls. """

import mariqt.variables as miqtv
import mariqt.core as miqtc
import requests
import json


def get_expedition_event_ids(expedition_id:int):
    """ returns dict {event_name: event_id} """
    ret = {}
    try:
        res = requests.get(miqtv.apis['osis_underway'] + 'expeditions/' + str(expedition_id) + '/events', timeout=5)
    except requests.exceptions.ConnectionError:
        res = False

    if not res:
        return ret
    
    events = json.loads(res.text)
    for event in events:
        # get event name sometimes only one of 'name' or 'optional_label' is filled, other 'null'
        #print("event",event)
        event_name = event['name']
        if event_name is not None:
            try:
                event_name = event_name.split('_')[1]
            except IndexError:
                #raise miqtc.IfdoException("Can't parse event part from event_name: " + event_name)
                event_name = event['optional_label']
        else:
            event_name = event['optional_label']

        ret[event_name] = event['id']

    return ret


def get_expedition_ids():
    """ 
    returns dict {cruise_name: cruise_id} of all expeditions. 
    RATHER use get_expedition_id_from_label() if you look for a single
    expeditions id - much faster
    """
    ret = {}
    try:
        res = requests.get(miqtv.apis['osis_underway'] + 'expeditions', timeout=5)
    except requests.exceptions.ConnectionError:
        res = False    

    if not res:
        return ret
    
    nr_pages = json.loads(res.text)['meta']['total_pages']
    cruises = []
    for i in range(1, nr_pages + 1):
        res = requests.get(miqtv.apis['osis_underway'] + 'expeditions', params={'page':i}, timeout=5)
        cruises += json.loads(res.text)['data']

    for cruise in cruises:
        ret[cruise['name']] = cruise['id']

    return ret


def get_expedition_id_from_label(label:str):
    """ 
    queries osis for the expedition label and returns its id if exact match was found, 
    otherwise raise ValueError.
    """
    expeditions = get_expeditions_from_label(label)
    if len(expeditions) != 1:
        raise ValueError("No exact match found for label: " + label)
    else:
        return expeditions[0]['id']


def get_expeditions_from_label(label:str):
    """ queries osis for the expedition label and return list of matches """
    ret = {}
    try:
        res = requests.get(miqtv.apis['osis_underway'] + 'expeditions',
                           params={'filter':str({'name':label}).replace('\'','"')}, timeout=5)
    except requests.exceptions.ConnectionError:
        res = False    

    if not res:
        return ret
    
    ret = json.loads(res.text)['data']
    return ret


def get_event_url(expedition_id:int,event_id:int):
    """ returns url to osis event """
    return miqtv.apis['osis_app'] + "expeditions/" + str(expedition_id) + "/events/" + str(event_id)


def get_expedition_url(expedition_id:int):
    """ returns url to osis expedition """
    return miqtv.apis['osis_app'] + "expeditions/" + str(expedition_id)


def get_expedition_id_from_url(osis_url:str):
    """ returns parsed expedition from url as int. Returns -1 if not successful """
    # e.g. https://osis.geomar.de/app/expeditions/359211/events/1781066
    exp_id = -1
    url_split = osis_url.split("/")
    try:
        exp_id = int(url_split[url_split.index('expeditions') + 1])
    except (ValueError, IndexError):
        pass
    return exp_id