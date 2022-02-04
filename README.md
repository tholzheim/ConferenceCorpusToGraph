![Build](https://github.com/tholzheim/ConferenceCorpusToGraph/actions/workflows/Build/badge.svg)
# ConferenceCorpusToGraph

Provides a mapping from the entites in [ConferenceCorpus](https://github.com/WolfgangFahl/ConferenceCorpus) to a graph.
The projects goal is to only test out different mapping strategies and graph databases.

Current mapping status:
* neo4j
  * datasources: ConfRef, dblp
  * enties: Event, EventSeries(only implicit)
  
## neo4j
 
 Start the database with `docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --env=NEO4J_AUTH=none neo4j`
