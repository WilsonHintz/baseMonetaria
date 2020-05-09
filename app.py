from flask import Flask, render_template, request, jsonify
from helpers import bcraImporter
import json
app = Flask(__name__)

datas={}

@app.route('/pie')
def pie():
    pie_datas = datas
    return render_template('spline.html', title='Bitcoin Monthly Price in USD', max=17000, datas=pie_datas)


@app.route('/import', methods=['GET'])
def execImport():
    result = bcraImporter.importBase(request.args.get('fecha'))
    content = json.loads(result.content)

    print(request.args.get('fecha'))
    #resp = jsonify("result")
    #resp.status_code = 200
    return content


@app.route('/getCsv')
def downloadCsv():
    result = bcraImporter.getCsv()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
