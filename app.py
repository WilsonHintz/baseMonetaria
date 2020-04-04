from flask import Flask, Markup, render_template
import pandas as pd
import csv

app = Flask(__name__)

# df = pd.read_csv('output.csv')
# labels = df['fecha'].to_numpy()
# values = df['Base_Monetaria_Total'].to_numpy()
#datas = df.to_dict()
datas={}
# with open('/static/output.csv') as fin:
#     reader=csv.reader(fin, delimiter=';', skipinitialspace=True)
#     for row in reader:
#         datas[row[0]]=row[1]
# print(datas)

# @app.route('/bar')
# def bar():
#     bar_labels = labels
#     bar_values = values
#     return render_template('bar_chart.html', title='Base Monetaria en PESOS', max=2513096, labels=bar_labels,
#                            values=bar_values)


# @app.route('/line')
# def line():
#     line_labels=labels
#     line_values=values
#     return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=2513096, labels=line_labels, values=line_values)

@app.route('/pie')
def pie():
    pie_datas = datas
    return render_template('spline.html', title='Bitcoin Monthly Price in USD', max=17000, datas=pie_datas)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
