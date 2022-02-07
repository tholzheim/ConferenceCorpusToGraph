[![Github Actions Build](https://github.com/tholzheim/ConferenceCorpusToGraph/workflows/Build/badge.svg?branch=master)](https://github.com/tholzheim/ConferenceCorpusToGraph/actions?query=workflow%3ABuild+branch%3Amaster)
[![GitHub issues](https://img.shields.io/github/issues/tholzheim/ConferenceCorpusToGraph.svg)](https://github.com/tholzheim/ConferenceCorpusToGraph/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/tholzheim/ConferenceCorpusToGraph.svg)](https://github.com/tholzheim/ConferenceCorpusToGraph/issues/?q=is%3Aissue+is%3Aclosed)
# ConferenceCorpusToGraph

Provides a mapping from the entites in [ConferenceCorpus](https://github.com/WolfgangFahl/ConferenceCorpus) to a graph.
The projects goal is to only test out different mapping strategies and graph databases.

Current mapping status:
* neo4j
  * datasources: ConfRef, dblp
  * enties: Event, EventSeries(only implicit)
  
## neo4j
 
 Start the database with `docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --env=NEO4J_AUTH=none neo4j`
