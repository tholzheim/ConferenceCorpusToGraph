import unittest
from unittest import TestCase
from py2neo import Graph
from ccgraphmapper.cc2neo4j import ConfRef, DblpEvent


class TestCc2neo4j(TestCase):
    """
    tests cc2neo4j graph mappers
    """

    def test_buildingNeo4jGraph(self):
        """
        tests building the graph by adding entities and relations of different data sources
        """
        graph = Graph("bolt://localhost:7687", auth=("", ""))
        confRef2Graph = ConfRef(graph=graph)
        confRef2Graph.addAllEvents(limit=250)
        confRef2Graph.addSeriesRelation()
        confRef2Graph.addLocationRelation()
        confRef2Graph.addDblpSeriesRelation()

        dblp2Graph = DblpEvent(graph=graph)
        dblp2Graph.addAllEvents(limit=250)
        dblp2Graph.addLocationRelation()
        print(dblp2Graph.addSeriesRelation().stats())


if __name__ == '__main__':
    unittest.main()
