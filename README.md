# balerion
###### Firstly run Neo4j on localhost

docker build -t balerion .

docker run -p 5000:5000 --net=host balerion
