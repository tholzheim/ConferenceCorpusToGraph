from distutils.core import setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='cc2graph',
      version='0.0.1',
      description='ConferenceCorpus to neo4j mapper',
      author='tholzheim',
      author_email='tim.holzheim@rwth-aachen.de',
      packages=['ccgraphmapper'],
      install_requires=requirements,
     )