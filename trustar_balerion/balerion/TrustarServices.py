from TrustarQueries import QueriesRepository
import datetime
import json
import math
import pandas as pd

COUNT = "NUMBER"
VALUE = "VALUE"

# Mapping from barncat indicator labels to TruSTAR indicator labels
MAPPING = {"md5": "MD5",
           "Campaign": "CAMPAIGN",
           "sha1": "SHA1",
           "sha256": "SHA256",
           "ip-dst": "IP",
           "Domain": "URL",
           "rat_name": "MALWARE",
           "imphash": "IMPHASH_MD5",
           "section_.BSS": "BSS_MD5",
           "section_DATA": "DATA_MD5",
           "section_.IDATA": "IDATA_MD5",
           "section_.ITEXT": "ITEXT_MD5",
           "section_.RDATA": "RDATA_MD5",
           "section_.RELOC": "RELOC_MD5",
           "section_.RSRC": "RSRC_MD5",
           "section_.TEXT": "TEXT_MD5",
           "section_.TLS": "TLS_MD5",
           "section_CODE": "CODE_MD5",
           "Mutex": "MUTEX"}


class Classifier(object):
    """
    This class contains the tools to classify into a classification indicator given an input indicator
    """

    def __init__(self, **kwargs):
        self.type = ""
        for key, value in kwargs.iteritems():
            if key == 'type':
                self.type = value
            elif key == 'connection':
                self.queries_repository = QueriesRepository(value)

    def get_records_number(self):
        """
        Method returning the total number of records in the graph DB.
        :return: integer
        """

        result = self.queries_repository.query_records_number()
        return result[0][COUNT]

    def get_class_values(self, input_value, class_type):
        """
        Method to determine the list of classification indicator values associated with
        a given input indicator value.
        :param input_value: value of the input indicator
        :param class_type: type of the classification indicator
        :return: list of classification indicator values
        """

        result_query = self.queries_repository.query_class_values(input_value,
                                                                  class_type)

        result = []
        for row in result_query:
            result.append(row[VALUE])
        return result

    def get_class_distribution(self, class_type):
        """
        Method to get the distribution of classification indicator values.
        :param class_type: classification indicator type
        :return: dict with a classification indicator value as key and an integer as value
        """

        result = {}
        result_query = self.queries_repository.query_class_frequencies(class_type)
        for row in result_query:
                result[row[VALUE]] = row[COUNT]
        return result

    def get_indicator_frequency(self, input_value):
        """
        Method to get the frequency of occurrence of an input indicator value.
        :param input_value: input indicator value
        :return: integer
        """

        result = self.queries_repository.query_indicator_frequency(input_value)
        return result[0][COUNT]

    def get_indicator_class_frequency(self, input_value, class_values):
        """
        This method gets the frequency of co-occurrence of an input indicator value w.r.t. a list of classification
        indicator values.
        :param input_value: input indicator value
        :param class_values: list of classification indicator values
        :return: dict with a classification indicator value as key and an integer as value
        """
        result = {}
        for class_value in class_values:
            result_query = self.queries_repository.query_indicator_class_frequency(input_value, class_value)
            if result_query[0][COUNT] != 0:
                result[class_value] = result_query[0][COUNT]
        return result

    @staticmethod
    def get_probabilities(n_x_y):
        """
        This method computes probabilities for the Bayes equation with a prior obtained from the real data.
        The only required input is the frequency of co-occurrence of input indicator x with classification indicator y.
        :param n_x_y: frequency of co-occurrence of x and y
        :return: dict with a classification indicator value as key and a float as value (probabilities in %)
        """

        summation = sum(n_x_y.values())
        result = {}
        for class_value in n_x_y:
            result[class_value] = float(n_x_y[class_value])/float(summation)*100
        return result

    @staticmethod
    def get_uniform_odds(n_x_y, n_y):
        """
        This method computes probabilities for the Bayes equation that assumes that the prior probabilities of the
        classification indicators are uniform. The required inputs are the frequency of co-occurrence of input indicator
        x with classification indicator y, and the frequency of occurrence of classification indicator y.
        :param n_x_y: frequency of co-occurrence of x and y
        :param n_y: frequency of occurrence of y
        :return: dict with a classification indicator value as key and a float as value (probabilities in %)
        """

        ratio = {}
        for class_value in n_x_y:
            ratio[class_value] = float(n_x_y[class_value])/float(n_y[class_value])

        result = {}
        summation = sum(ratio.values())
        for class_value in ratio:
            result[class_value] = float(ratio[class_value])/float(summation)*100
        return result


class Persist(object):
    """
    This class is used to store data to a Neo4j database
    """

    def __init__(self, **kwargs):
        self.type = ""
        for key, value in kwargs.iteritems():
            if key == 'type':
                self.type = value
            elif key == 'connection':
                self.queries_repository = QueriesRepository(value)

    @staticmethod
    def process_file(source_file):
            df = pd.read_csv(source_file)
            return df

    def store_file(self, record):
        """
        Method that takes a pandas data frame and stores it in the graph DB.
        :param record: a pandas data frame
        """

        json_in_comment = record.comment == 'JSON config'
        json_config = {}

        if True in json_in_comment.values:
            try:
                json_config = json.loads(record[record.comment == 'JSON config']['value'].values[0]
                                         .encode('ascii', 'ignore'))
            except:
                pass

            if 'Date' in json_config:
                time = json_config['Date'].split(" ")[0].split("-")
                timestamp = '{0:f}'.format((datetime.datetime(int(time[0]), int(time[1]), int(time[2][0:2])) -
                                            datetime.datetime(1970, 1, 1)).total_seconds()*1000)
            else:
                timestamp = '{0:f}'.format((datetime.datetime(2016, 8, 12) -
                                            datetime.datetime(1970, 1, 1)).total_seconds()*1000)
            doc_id = str(record.event_id.values[0])

            if 'Campaign' in json_config:
                title = json_config['Campaign'].encode('ascii', 'ignore') + " " + doc_id
            else:
                title = 'NO_CAMPAIGN' + " " + doc_id

            for key in MAPPING:
                if key in json_config:
                    indicator_value = json_config[key]
                    indicator_type = MAPPING[key]
                    self.queries_repository.store_object(doc_id,
                                                         title,
                                                         str(int(math.floor(float(timestamp)))),
                                                         indicator_type,
                                                         indicator_value)
