import io
from contextlib import redirect_stdout
from typing import Callable

from alive_progress import alive_it
from lodstorage.lod import LOD
from py2neo import Graph
from corpus.datasources.download import Download
from corpus.event import EventStorage, Event
from corpus.lookup import CorpusLookup, CorpusLookupConfigure

class GraphMapper(object):
	"""
	Mapping functions to map records e.g. of events to a graph
	interface class
	"""
	SOURCE_ID=NotImplemented
	EVENT_LABEL=NotImplemented

	def __init__(self, graph:Graph, debug:bool=False):
		self.graph=graph
		self.debug=debug

	def runQuery(self,query, *args, **kwargs):
		"""
		executes query and returns the result
		if debug is True print stats
		"""
		qres = self.graph.run(query, *args, **kwargs)
		if self.debug:
			print(qres.stats())
		return qres

	def addEvent(self, event:Event):
		"""
		Add Event to the graph
		"""
		return NotImplemented

	def addAllEvents(self, limit:int=None):
		"""
		Adds all events to the graph

		Args:
			limit(int): limit the number of events added to the graph i.e. for debug/testing purposes
		"""
		events = self.getEvents()
		if limit is not None:
			print(f"Limited events to {limit} of {len(events)}")
			events=events[:limit]
		total = len(events)
		for event in alive_it(events):
			qres = self.addEvent(event)


	def getEvents(self):
		corpus = CorpusLookup(configure=CorpusLookupConfigure.configureCorpusLookup)
		output=self.captureOutput(corpus.load, forceUpdate=False) # reduces debug output
		if self.debug:
			print(output)
		datasource = corpus.getDataSource(self.SOURCE_ID)
		events = datasource.eventManager.getList()
		return events

	def addLocationRelation(self):
		"""
		Adds the location relation to the event
		currently only city
		"""
		query=f"""
		MATCH (e:Event:{self.EVENT_LABEL})
		WHERE e.cityWikidataid IS NOT NULL
		MERGE (c:City {{wikidataid:e.cityWikidataid}})
		MERGE (e)-[:CITY]->(c)
		"""
		qres = self.runQuery(query)
		return qres

	@staticmethod
	def captureOutput(fn: Callable, *args, **kwargs) -> str:
		"""
        Captures stdout put of the given function

        Args:
            fn(callable): function to call
        Returns:
            str
        """
		f = io.StringIO()
		with redirect_stdout(f):
			fn(*args, **kwargs)
		f.seek(0)
		output = f.read()
		return output



class ConfRef(GraphMapper):
	"""
	Maps confref data to graph data
	"""
	SOURCE_ID="confref"
	EVENT_LABEL="ConfRef"

	@staticmethod
	def getSamples() -> dict:
		samples=[{'acronym': 'BTW',
				'country': 'Germany', 
				'city': 'Dresden', 
				'year': 2021, 
				'startDate': '2021-01-01', 
				'endDate': '2021-01-01', 
				'submissionExtended': 0, 
				'keywords': '', 
				'ranks': '',
				'area': 'Computer Science',
				'dblpSeriesId': 'conf/btw',
				'seriesId': 'btw',
				'seriesTitle': 'Datenbanksysteme für Business, Technologie und Web Datenbanksysteme in Büro, Technik und Wissenschaft',
				'eventId': 'btw2021',
				'url': 'http://portal.confref.org/list/btw2021',
				'title': 'Datenbanksysteme für Business, Technologie und Web Datenbanksysteme in Büro, Technik und Wissenschaft',
				'source': 'confref',
				'location': 'Dresden, Germany',
				'cityWikidataid': 'Q1731',
				'region': 'Saxony',
				'regionIso': 'DE-SN',
				'regionWikidataid': 'Q1202',
				'countryIso': 'DE',
				'countryWikidataid': 'Q183'}
				 ]
		return samples

	def addEvent(self, event:Event):
		query="""
		MERGE (e:Event:ConfRef {eventId:$event.eventId})
		ON CREATE SET e = $event
		ON MATCH SET e += $event
		"""
		records=event.__dict__
		params={"event":records}
		qres = self.runQuery(query, params)
		return qres

	def addAllRelations(self):
		self.addLocationRelation()
		self.addSeriesRelation()
		self.addDblpSeriesRelation()

	def addSeriesRelation(self):
		"""
		Adds the series relation to the event
		"""
		query="""
		MATCH (e:Event:ConfRef)
		WHERE e.seriesId IS NOT NULL
		MERGE (s:EventSeries:ConfRef {eventSeriesId:e.seriesId})
		MERGE (e)-[:IN_EVENT_SERIES]->(s)
		"""
		qres = self.runQuery(query)
		return qres

	def addDblpSeriesRelation(self):
		"""
		Adds the series relation to the event
		Note: the series relation should be added first
		"""
		query="""
		MATCH (e:Event:ConfRef)
		WHERE e.dblpSeriesId IS NOT NULL
		MATCH (e)-[:IN_EVENT_SERIES]->(s:EventSeries:ConfRef)
		MERGE (sd:EventSeries:DBLP {eventSeriesId:e.dblpSeriesId})
		MERGE (s)-[r:MAYBE_SAME_AS]-(sd)
		ON CREATE SET r.definedBy = [e.eventId]
		ON MATCH SET r.definedBy = r.definedBy + e.eventId
		"""
		qres = self.runQuery(query)
		return qres


class DblpEvent(GraphMapper):
	"""
	Maps dblp event data to graph data
	"""
	SOURCE_ID = "dblp"
	EVENT_LABEL="DBLP"

	@staticmethod
	def getSamples():
		samples=[
			{
				"acronym": "WEBIST 2019",
				"booktitle": "WEBIST",
				"city": "Vienna",
				"cityWikidataid": "Q1741",
				"country": "Austria",
				"countryIso": "AT",
				"countryWikidataid": "Q40",
				"doi": None,
				"ee": None,
				"endDate": None,
				"eventId": "conf/webist/2019",
				"isbn": "978-989-758-386-5",
				"location": "Vienna, Austria",
				"mdate": "2019-10-17",
				"publicationSeries": None,
				"region": "Vienna",
				"regionIso": "AT-9",
				"regionWikidataid": "Q1741",
				"series": "webist",
				"source": "dblp",
				"startDate": None,
				"title": "Proceedings of the 15th International Conference on Web Information Systems and Technologies, WEBIST 2019, Vienna, Austria, September 18-20, 2019.",
				"url": "https://dblp.org/db/conf/webist/webist2019.html",
				"year": 2019
			}
		]
		return samples

	def addEvent(self, event:Event):
		query="""
		MERGE (e:Event:DBLP {eventId:$event.eventId})
		ON CREATE SET e = $event
		ON MATCH SET e += $event
		"""
		records=event.__dict__
		params={"event":records}
		qres = self.runQuery(query, params)
		return qres

	def addSeriesRelation(self):
		"""
		Adds the series relation to the event
		"""
		query="""
		MATCH (e:Event:DBLP)
		WHERE e.series IS NOT NULL
		MERGE (s:EventSeries:DBLP {eventSeriesId:"conf/" + e.series})
		MERGE (e)-[:IN_EVENT_SERIES]->(s)
		"""
		qres = self.runQuery(query)
		return qres


if __name__ == '__main__':
	graph = Graph("bolt://localhost:7687", auth=("", ""))
	confRef2Graph = ConfRef(graph=graph)
	#confRef2Graph.addAllEvents(limit=100)
	#confRef2Graph.addSeriesRelation()
	#confRef2Graph.addLocationRelation()
	#confRef2Graph.addDblpSeriesRelation()

	dblp2Graph = DblpEvent(graph=graph)
	dblp2Graph.addAllEvents(limit=100)
	#dblp2Graph.addLocationRelation()
	#dblp2Graph.addSeriesRelation()