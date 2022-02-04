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
        graph = Graph("bolt://localhost:7687", auth=("", ""))
        confRef2Graph = ConfRef(graph=graph)
        confRef2Graph.addAllEvents(limit=1000)
        print(confRef2Graph.addSeriesRelation().stats())
        print(confRef2Graph.addLocationRelation().stats())
        print(confRef2Graph.addDblpSeriesRelation().stats())

        dblp2Graph = DblpEvent(graph=graph)
        dblp2Graph.addAllEvents(limit=1000)
        print(dblp2Graph.addLocationRelation().stats())
        print(dblp2Graph.addSeriesRelation().stats())


if __name__ == '__main__':
    unittest.main()
