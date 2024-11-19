import numpy as np
from flask import Flask, request, jsonify
from flask import render_template, session, redirect
from flask_bootstrap import Bootstrap
from ZillowPredictionApi import ZillowPredictionApi as Zillow

app = Flask(__name__)
app.secret_key = "571cb9c35d0d6bf3da64d288e54c24bffdd91eebd8af087ce69355dcb2a6aaf0"
Bootstrap(app)

data_test = Zillow()


@app.route('/app')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'Hello world'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.route('/back')
def back():
    return redirect(request.referrer)


@app.route('/predict', methods=['GET'])
def get_prediction_info():
    cities = data_test.get_city()
    homeType = data_test.get_home_type()
    county = data_test.get_county()
    streetAddress = data_test.get_streetAddress()

    return render_template('form_model_test.html', cities=cities, homeType=homeType, streetAddress=streetAddress, county=county)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Reception les données au format JSON
    t = data_test.setup_routes(data)
    return jsonify(t)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
