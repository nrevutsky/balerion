from flask import Flask
from flask import render_template
from flask import request

from trustar_balerion.scripts.balerion_bayes import query_barncat

app = Flask(__name__)
INDEX_TEMPLATE = 'index.html'


@app.route('/')
def main_page_view():
    return render_template(INDEX_TEMPLATE)


@app.route('/', methods=['POST'])
def result_view():
    indicator = request.form['ioc']
    if not indicator:
        result = {'error': 'This field is required'}
    elif indicator.find(',') != -1:
        result = {'error': 'Please, input only one value'}
    else:
        classification = request.form['classification']
        result = query_barncat(indicator, classification)
        if result:
            for key, value in result.iteritems():
                if value:
                    result[key] = float("{0:.4f}".format(value))
        else:
            result = {'no_result': 'Results: This IoC does not exist in the Barncat Intelligence Database.'
                                   ' Please try another IoC.'}
    return render_template(INDEX_TEMPLATE, data=result)


if __name__ == '__main__':
    app.run()
