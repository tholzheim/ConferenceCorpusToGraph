import unittest
from py2neo import Graph
from ccgraphmapper.cc2neo4j import ConfRef, DblpEvent
from tests.basetest import Basetest


class TestCc2neo4j(Basetest):
    """
    tests cc2neo4j graph mappers
    """

    def test_buildingNeo4jGraph(self):
        """
        tests building the graph by adding entities and relations of different data sources
        """
        debug=True
        graph = Graph("bolt://localhost:7687", auth=("", ""))
        confRef2Graph = ConfRef(graph=graph)
        confRef2Graph.addAllEvents(limit=1000)
        confRef2Graph.debug=debug # Show stats of added relations
        confRef2Graph.addSeriesRelation()
        confRef2Graph.addLocationRelation()
        confRef2Graph.addDblpSeriesRelation()

        dblp2Graph = DblpEvent(graph=graph)
        dblp2Graph.addAllEvents(limit=1000)
        dblp2Graph.debug = debug  # Show stats of added relations
        dblp2Graph.addLocationRelation()
        dblp2Graph.addSeriesRelation()


if __name__ == '__main__':
    unittest.main()
