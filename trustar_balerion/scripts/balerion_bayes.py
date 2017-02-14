#!/usr/bin/env python

"""
Script that takes an input indicator value and a classification indicator type and computes the probabilities of
the classification indicator values
"""

import argparse
import json

from trustar_balerion.balerion import Classifier
from trustar_balerion.balerion import Neo4jConnection
import os


# tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'application_properties.ini')
neo4j_connection = Neo4jConnection(config_file='trustar_balerion/scripts/application_properties.ini')


def query_barncat(input_indicator, class_type):
    classifier = Classifier(connection=neo4j_connection)
    class_values = classifier.get_class_values(input_indicator, class_type.upper())

    x = input_indicator

    print '#################################\n'
    print 'Computing probabilities of ' + class_type + ' {} for indicator {}.\n'.format(class_values, x)

    print '#################################\n'
    n_x = classifier.get_indicator_frequency(x)
    print 'Frequency of occurrence of indicator {}: {}.\n'.format(x, n_x)

    print '#################################\n'
    print 'Frequency of co-occurrence of ' + class_type + ' {} with indicator {}:\n'.format(class_values, x)
    n_x_y = classifier.get_indicator_class_frequency(x, class_values)
    print json.dumps(n_x_y, indent=2)

    print '#################################\n'
    print 'Compute probability (%) of ' + class_type + ' {} given indicator {} for a non-uniform prior:\n'.format(
            class_values, x)
    p_n_i = classifier.get_probabilities(n_x_y)
    print json.dumps(p_n_i, indent=2)
    return p_n_i


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=('Query barncat data using an input indicator and returns '
                                                  'probabilities of different RAT-families/Campaigns\n'
                                                  'Example:\n\n'
                                                  'python balerion_bayes.py -i f34d5f2d4577ed6d9ceec516c1f5a744 '
                                                  '-c malware'))
    parser.add_argument('-i', '--indicator', required=True, dest='indicator', help='input indicator')
    parser.add_argument('-c', '--class', required=True, dest='class_type', help='class indicator')

    # Indicator
    args = parser.parse_args()
    indicator = args.indicator
    class_type = args.class_type

    query_barncat(indicator, class_type)


if __name__ == '__main__':
    main()
