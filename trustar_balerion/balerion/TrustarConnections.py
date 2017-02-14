import ConfigParser
from py2neo import Graph, authenticate


class Neo4jConnection(object):
    """
    Main class to connect to Neo4j DB
    The properties are stored in a .ini file
    """

    def __init__(self, config_file="application_properties.ini"):
        config = ConfigParser.ConfigParser()
        config.read(config_file)

        databases = config.sections()
        neo4j = databases[0]
        host_port_user_password_path = config.options(neo4j)
        host_port = host_port_user_password_path[0]
        user = host_port_user_password_path[1]
        password = host_port_user_password_path[2]
        path = host_port_user_password_path[3]
        host_port_value = config.get(neo4j, host_port)
        user_value = config.get(neo4j, user)
        password_value = config.get(neo4j, password)
        path_value = config.get(neo4j, path)
        authenticate(host_port_value, user_value, password_value)

        self.graph = Graph(path_value)
        self.cypher = self.graph.cypher
