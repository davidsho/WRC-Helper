import requests

class Helper:
    '''
    Class containing helper functions for WRC RESTful API

    ...

    Attributes
    ----------
    season_url : str
        API URL for the active season
    results_api : str
        Results API URL for a given event

    '''

    def __init__(self):
        '''
        Parameters
        ----------
        season_url : str
            API URL for the active season
        results_api : str
            Results API URL for a given event        
        '''
        self.season_url = "https://api.wrc.com/contel-page/83388/calendar/active-season/"
        self.results_api = 'https://api.wrc.com/results-api'

    def getActiveSeason(self, all=False):
        '''Gets JSON from active season API.

        If all argument isn't passed, automatically returns just rally events items.

        Parameters
        ----------
        all : bool, optional
            Whether entire JSON is returned or not (default is False)

        Returns
        -------
        list
            a list of the events in the current calendar
        '''
        r = requests.get(self.season_url).json()
        if all:
            return r
        else:
            return r['rallyEvents']['items']
        
    def getEventIds(self, season):
        '''Gets list of IDs from a season
        
        Parameters
        ----------
        season : list
            List of events in a season
        
        Returns
        -------
        list
            List of event IDs
        '''
        return [ev['id'] for ev in season]
        
    def getEventIdFromName(self, season, eventName):
        '''Gets the ID of an event from its name.

        Parameters
        ----------
        season : list
            List of events in season
        eventName : str
            Name of the event to match

        Returns
        -------
        int
            event ID as an integer
        None
            if no event is found
        '''        
        e = [ev['id'] for ev in list(filter(lambda event: eventName.lower() in event['name'].lower(), season))]
        if len(e) > 0:
            return e[0]
        else:
            return None

    def getItinerary(self, eventId):
        '''Gets itinerary of an event.

        Parameters
        ----------
        eventId : int
            The ID of the event to get the itinerary of

        Returns
        -------
        list
            a list of dictionaries of itinerary legs
        '''
        link = self.results_api + '/rally-event/' + str(eventId) + '/itinerary'
        r = requests.get(link).json()
        return r['itineraryLegs']

    def getSections(self, itinerary):
        '''Gets a list of itinerary sections from itinerary.

        Parameters
        ----------
        itinerary : list
            a list of itinerary leg dictionaries

        Returns
        -------
        list
            a list of dictionaries of itinerary sections
        '''
        return [i['itinerarySections'] for i in itinerary]

    def getControls(self, sections):
        '''Gets a list of controls from itinerary sections.

        Parameters
        ----------
        sections : list
            a list of itinerary sections

        Returns
        -------
        list
            a list of dictionaries of itinerary controls
        '''
        controls = []
        for section in sections:
            for c in section:
                for control in c['controls']:
                    control['itinerarySectionId'] = c['itinerarySectionId']
                    controls.append(control)
        return controls

    def getStages(self, sections):
        '''Gets a list of itinerary stages from itinerary.

        Parameters
        ----------
        sections : list
            a list of itinerary sections

        Returns
        -------
        list
            a list of dictionaries of itinerary stages
        '''
        stages = []
        for section in sections:
            for s in section:
                for stage in s['stages']:
                    stage['itinerarySectionId'] = s['itinerarySectionId']
                    stages.append(stage)
        return stages    

    def getStageList(self, stages):
        '''Gets a list of itinerary stage IDs.

        Parameters
        ----------
        stages : list
            a list of itinerary stage dictionaries

        Returns
        -------
        list
            a list of stage IDs
        '''
        return [s['stageId'] for s in stages]

    def getStagesLookup(self, stages):
        '''Gets a list of stage dictionaries with code and ID.

        Parameters
        ----------
        stages : list
            a list of itinerary stage dictionaries

        Returns
        -------
        list
            a list of dictionaries of itinerary stages with code and ID
        '''
        return [{"code": s['code'], "stageId": s['stageId']} for s in stages]

    def getStageId(self, stages, sname, typ='code'):
        '''Gets a list of itinerary sections from itinerary.

        Parameters
        ----------
        stages : list
            a list of itinerary stage dictionaries
        sname : str
            either stage name or code
        typ : str, optional
            'code' or 'name', default 'code'

        Returns
        -------
        int
            stage ID integer
        None
            if no stage is found
        '''
        if typ == 'code':
            sId = [s['stageId'] for s in stages if s[typ] == sname]
            if len(sId) > 0:
                return sId[0]
            else:
                return None
        else:
            sId = [s['stageId'] for s in stages if sname.lower() in s[typ].lower()]
            if len(sId) > 0:
                return sId[0]
            else:
                return None

    def getStageInfo(self, stages, sid, typ='stageId', clean=True):
        '''Gets stage name and distance.

        Parameters
        ----------
        stages : list
            a list of itinerary stage dictionaries
        sid : int
            the stage ID
        clean : bool, optional
            whether stage name should be cleaned, default True

        Returns
        -------
        dictionary
            a dictionary containing stage name and distance
        '''
        stage = [s for s in stages if s[typ] == sid]
        if len(stage) < 0:
            return None
        stage = stage[0]
        if clean:
            return {"name": stage["name"].replace(" (Live TV)", ""), "distance": stage["distance"]}
        else:
            return {"name": stage["name"], "distance": stage["distance"]}

    def getStartListId(self, itinerary, itinerarySectionId):
        '''Gets start list ID from section ID.

        Parameters
        ----------
        itinerary : list
            a list of itinerary leg dictionaries
        itinerarySectionId : int
            the section ID

        Returns
        -------
        int
            start list ID
        None
            if no section is found
        '''
        sections = self.getSections(itinerary)
        itineraryLegId = None
        for section in sections:
            for s in section:
                if s['itinerarySectionId'] == itinerarySectionId:
                    itineraryLegId = s['itineraryLegId']
        if not itineraryLegId:
            return None
        return next((item["startListId"] for item in itinerary if item['itineraryLegId'] == itineraryLegId), None)

    def getStartList(self, eventId, startListId):
        '''Gets start list from event and start list ID.

        Parameters
        ----------
        eventId : int
            the event ID
        startListId : int
            the start list ID

        Returns
        -------
        list
            a list of starters in start order
        '''
        startListURL = self.results_api + '/rally-event/' + str(eventId) + '/start-list-external/' + str(startListId)
        r = requests.get(startListURL).json()
        startList = r['startListItems']
        return sorted(startList, key=lambda d: d['order'])

    def getRallyEntries(self, eventId):
        '''Get the entries from a rally event.

        Parameters
        ----------
        eventId : int
            the event ID

        Returns
        -------
        list
            a list of car entries for an event
        '''
        carsURL = self.results_api + "/rally-event/" + str(eventId) + "/cars"
        return requests.get(carsURL).json()
    
    def getEntryById(self, entries, entryId):
        '''Gets entry by ID.

        Parameters
        ----------
        entries : list
            a list of event entries
        entryId : int
            the event entry ID

        Returns
        -------
        dictionary
            the event found
        None
            if no event found
        '''
        return next((e for e in entries if e['entryId'] == entryId), None)

    def getDrivers(self, entries):
        '''Gets just drivers from entries.

        Parameters
        ----------
        entries : list
            a list of event entries

        Returns
        -------
        list
            a list of drivers from entries
        '''
        return [e['driver'] for e in entries]

    def getCoDrivers(self, entries):
        '''Gets just codrivers from entries.

        Parameters
        ----------
        entries : list
            a list of event entries

        Returns
        -------
        list
            a list of codrivers from entries
        '''
        return [e['codriver'] for e in entries]

    def getPersonId(self, persons, sname, typ='fullName'):
        '''Gets just codrivers from entries.

        Parameters
        ----------
        persons : list
            a list of persons
        sname : str
            the person code or name
        typ : str, optional
            'code' or 'fullName', default 'fullName'

        Returns
        -------
        int
            the person ID
        None
            if no person found
        '''
        if typ == 'code':
            return next((person['personId'] for person in persons if person[typ] == sname), None)
        else:
            return next((person['personId'] for person in persons if sname.lower() in person[typ].lower()), None)
        
    def getCarDataFromEntry(self, entry):
        '''Get core car data from an entry

        Parameters
        ----------
        entry : dictionary
            full entry dictionary

        Returns
        -------
        dictionary
            core info from entry dictionary
        '''
        keys = ['entryId','driverId','codriverId','manufacturerId','vehicleModel','eligibility']
        newEntry = {key: entry[key] for key in keys}
        newEntry['classname'] = entry['eventClasses'][0]['name']
        newEntry['manufacturer'] = entry['manufacturer']['name']
        newEntry['entrantname'] = entry['entrant']['name']
        newEntry['groupname'] = entry['group']['name']
        newEntry['drivername'] = entry['driver']['abbvName']
        newEntry['driverfullname'] = entry['driver']['fullName']
        newEntry['codrivername'] = entry['codriver']['abbvName']
        newEntry['codriverfullname'] = entry['codriver']['fullName']
        newEntry['code'] = entry['driver']['code']
        return newEntry

    def getCarData(self, entries):
        '''Gets car data from all entries.

        Parameters
        ----------
        entries : list
            a list of event entries

        Returns
        -------
        list
            a list of core car data from all entries
        '''
        dataList = []
        for entry in entries:
            newEntry = self.getCarDataFromEntry(entry)
            dataList.append(newEntry)
        return dataList

    def getPenalties(self, eventId):
        '''Gets penalties from event.

        Parameters
        ----------
        eventId : int
            the event ID

        Returns
        -------
        list
            a list of penalties from event
        '''
        penaltiesURL = self.results_api + "/rally-event/" + str(eventId) + "/penalties"
        return requests.get(penaltiesURL).json()

    def getRetirements(self, eventId):
        '''Gets retirements from event.

        Parameters
        ----------
        eventId : int
            the event ID

        Returns
        -------
        list
            a list of retirements from event
        '''
        retirementsURL = self.results_api + "/rally-event/" + str(eventId) + "/retirements"
        return requests.get(retirementsURL).json()

    def getResult(self, eventId):
        '''Gets result from event.

        Parameters
        ----------
        eventId : int
            the event ID

        Returns
        -------
        list
            a list of finishing order from event
        '''
        resultURL = self.results_api + "/rally-event/" + str(eventId) + "/result"
        return requests.get(resultURL).json()

    def getStageWinners(self, eventId):
        '''Gets stage winners from event.

        Parameters
        ----------
        eventId : int
            the event ID

        Returns
        -------
        list
            a list of individual stage winners from event
        '''
        stageWinnersURL = self.results_api + "/rally-event/" + str(eventId) + "/stage-winners"
        return requests.get(stageWinnersURL).json()

    def getOverallResult(self, eventId, stageId):
        '''Gets overall results from event stage.

        Parameters
        ----------
        eventId : int
            the event ID
        stageId : int
            the stage ID

        Returns
        -------
        list
            a list of positions from event stage
        '''
        overallURL = self.results_api + "/rally-event/" + str(eventId) + "/stage-result/stage-external/" + str(stageId)
        overall = requests.get(overallURL).json()
        overall = [dict(pos, **{'stageId':stageId}) for pos in overall]
        return overall

    def getMultipleOverall(self, eventId, stageList):
        '''Gets overall results from multiple event stages.

        Parameters
        ----------
        eventId : int
            the event ID
        stageList : list
            list of stage IDs

        Returns
        -------
        list
            a list of positions from multiple event stages
        '''
        resultList = [self.getOverallResult(eventId, stage) for stage in stageList]
        final = []
        for res in resultList:
            for pos in res:
                final.append(pos)
        return final

    def getStageTimes(self, eventId, stageId):
        '''Gets times from event stage.

        Parameters
        ----------
        eventId : int
            the event ID
        stageId : int
            the stage ID

        Returns
        -------
        list
            a list of stage times
        '''
        stageTimesURL = self.results_api + "/rally-event/" + str(eventId) + "/stage-times/stage-external/" + str(stageId)
        return requests.get(stageTimesURL).json()

    def getMultipleStageTimes(self, eventId, stageList):
        '''Gets times from multiple event stages.

        Parameters
        ----------
        eventId : int
            the event ID
        stageList : list
            list of stage IDs

        Returns
        -------
        list
            a list of times from multiple event stages
        '''
        resultList = [self.getStageTimes(eventId, stage) for stage in stageList]
        final = []
        for res in resultList:
            for pos in res:
                final.append(pos)
        return final

    def getMultiStageTimesWide(self, multiStageTimes):
        '''Gets stage times by entry and stage IDs.

        Parameters
        ----------
        multiStageTimes : list
            list of times from event stages

        Returns
        -------
        list
            a list of dictionaries containing entry IDs and stage ID times
        '''
        entries = []
        for stage in multiStageTimes:
            if stage['entryId'] not in entries:
                entries.append(stage['entryId'])
        final = []
        for entry in entries:
            newEntry = {"entryId": entry}
            for stage in multiStageTimes:
                if stage["entryId"] == entry:
                    if stage['elapsedDurationMs']:
                        newEntry[stage['stageId']] = stage['elapsedDurationMs'] / 1000
                    else:
                        newEntry[stage['stageId']] = 0
            final.append(newEntry)
        return final

    def getMultiStagePositionsWide(self, multiStagePositions):
        '''Gets stage positions by entry and stage IDs.

        Parameters
        ----------
        multiStagePositions : list
            list of positions from event stages

        Returns
        -------
        list
            a list of dictionaries containing entry IDs and stage ID positions
        '''
        entries = []
        for stage in multiStagePositions:
            if stage['entryId'] not in entries:
                entries.append(stage['entryId'])
        final = []
        for entry in entries:
            newEntry = {"entryId": entry}
            for stage in multiStagePositions:
                if stage["entryId"] == entry:
                    newEntry[stage['stageId']] = stage['position']
            final.append(newEntry)
        return final

    def getMultiStageGenericWide(self, multiStageTimes, stageKey):
        '''Gets stage times by entry and stage IDs.

        Parameters
        ----------
        multiStageTimes : list
            list of times from event stages
        stageKey : str
            the key for which to show for each stage

        Returns
        -------
        list
            a list of dictionaries containing entry IDs and stage ID by provided key
        '''
        entries = []
        for stage in multiStageTimes:
            if stage['entryId'] not in entries:
                entries.append(stage['entryId'])
        final = []
        for entry in entries:
            newEntry = {"entryId": entry}
            for stage in multiStageTimes:
                if stage["entryId"] == entry:
                    if stageKey == 'elapsedDurationMs':
                        if stage[stageKey]:
                            newEntry[stage['stageId']] = stage['elapsedDurationMs'] / 1000
                        else:
                            newEntry[stage['stageId']] = 0
                    else:
                        newEntry[stage['stageId']] = stage[stageKey]
            final.append(newEntry)
        return final

    def getSplits(self, eventId, stageId):
        '''Gets splits by event and stage IDs.

        Parameters
        ----------
        eventId : int
            the event ID
        stageId : int
            the stage ID

        Returns
        -------
        dictionary
            a dictionary containing splits
        '''
        splitsURL = self.results_api + '/rally-event/' + str(eventId) + '/split-times/stage-external/' + str(stageId)
        return requests.get(splitsURL).json()

    def getDriverSplits(self, splits):
        '''Gets splits for each driver.

        Parameters
        ----------
        splits : dictionary
            dictionary containing split info

        Returns
        -------
        list
            a list of split times containing driver info and split time info
        '''
        driverSplits = []
        for entry in splits['entrySplitPointTimes']:
            for split in entry['splitPointTimes']:
                split['elapsedDurationS'] = split['elapsedDurationMs'] / 1000
                split.pop('elapsedDurationMs')
                driverSplits.append(split)
        return driverSplits

    def getDriverSplitsWide(self, splits):
        '''Gets splits for each driver.

        Parameters
        ----------
        splits : dictionary
            dictionary containing split info

        Returns
        -------
        list
            a list of split times containing driver info and times for each split
        '''
        entries = []
        for entry in splits['entrySplitPointTimes']:
            newEntry = {"entryId": entry['entryId']}
            for split in entry['splitPointTimes']:
                newEntry[split['splitPointId']] = split["elapsedDurationMs"] / 1000
            entries.append(newEntry)
        return entries

    def getMultiSplitTimes(self, eventId, stageList):
        '''Gets splits for multiple stages.

        Parameters
        ----------
        eventId : int
            the event ID
        stageList : list
            list of stage IDs

        Returns
        -------
        list
            a list of split times for multiple stages
        '''
        final = []
        for stage in stageList:
            splits = self.getSplits(eventId, stage)
            splits = self.getDriverSplits(splits)
            for split in splits:
                final.append(split)
        return final