# encoding=utf-8
import pickle
import logging
import pandas as pd
import joblib
from flask import request, jsonify, Flask
import datetime
logging.basicConfig(level=logging.DEBUG, filename="app_zillow.log"
                    , filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_model2():
    model = None
    try:
        with open('zillow_random_forest_model_joblib.pkl', 'rb') as file:
            model = joblib.load(file)
    except:
        logging.error("Erreur lors de l'ouverture du fichier")
    finally:
        return model


def load_model():
    return joblib.load("zillow_random_forest_model_joblib_version_2.3.pkl")


class ZillowPredictionApi:
    def __init__(self):
        self.columns = ['longitude', 'yearBuilt', 'latitude', 'bathrooms', 'bedrooms',
                        'propertyAge', 'bedroom_bathroom_ratio', 'livingArea_m2',
                        'value_per_m2', 'homeType_encoded', 'city_encoded', 'zipcode_encoded']
        self.data = self.load_data("zillow_dataset.xlsx")
        self.model = load_model()

    def setup_routes(self, data: dict):
        data_copy = data.copy()  # Copie du dictionnaire reçu en paramètre
        homeType = self.get_home_type()  # On récupère toute les homeType dans la DataSet
        city = self.get_cities()  # On récupère toute les city de la DataSet
        zipcode = self.get_zipcode()  # On récupère tout les zipcode de la DataSet

        homeType_encoded = self.get_home_type_encoded()  # On récupère toute les homeType dans la DataSet
        city_encoded = self.get_cities_encoded()  # On récupère toute les city de la DataSet
        zipcode_encoded = self.get_zipcode_encoded()  # On récupère tout les zipcode de la DataSet

        #        items : list = data_copy.values() # On récupère les valeurs envoyer par l'utilisateur
        #       columns = data_copy.keys()   # on récupère les clés de chacune de ces valeurs
        #      l = data['homeType']
        pos_homeType = -1
        pos_city = -1
        pos_zipcode = -1

        try:
            # On récupère la position de chaque variable catégoricielle dans la liste items
            pos_homeType = homeType.index(data_copy['homeType'])
            pos_city = city.index(data_copy['city'])
            pos_zipcode = zipcode.index(float(data_copy['zipcode']))
        except:
            logging.error("Erreur lors de la récupération des données dans le dataset")

        data_copy['city_encoded'] = city_encoded[pos_city]
        data_copy['homeType_encoded'] = homeType_encoded[pos_homeType]
        data_copy['zipcode_encoded'] = zipcode_encoded[pos_zipcode]
        data_copy['value_per_m2'] = float(3023.920162751529)
        data_copy['longitude'] = float(data_copy.get('longitude'))
        data_copy['yearBuilt'] = int(data_copy.get('yearBuilt'))
        data_copy['bedrooms'] = int(data_copy.get('bedrooms'))
        data_copy['propertyAge'] = int(datetime.datetime.now().year) - int(data_copy.get('yearBuilt'))
        data_copy['bedroom_bathroom_ratio'] = float(data_copy.get('bedrooms')) / float(data_copy.get('bathrooms'))
        data_copy['longitude'] = float(data_copy.get('longitude'))
        data_copy['latitude'] = float(data_copy.get('latitude'))
        data_copy['bathrooms'] = float(data_copy.get('bathrooms'))
        data_copy['livingArea_m2'] = float(data_copy.get('livingArea_m2'))

        data_copy.__delitem__('city')
        data_copy.__delitem__('homeType')
        data_copy.__delitem__('zipcode')

        value = []
        for keys in self.columns:
            value.append(data_copy[keys])

        final_data = pd.DataFrame([value], columns=list(self.columns))
        predict = self.model.predict(final_data)
        print(final_data)
        print(type(final_data))
        print("********************************************************************")
        print(self.columns)
        print(value)
        print(predict)
        print(type(predict))
        return {'predict': predict.tolist()}

    def load_data(self, path):
        data = None
        try:
            data = pd.read_excel(path)
        except:
            logging.error("Erreur lors de l'ouverture du DataSet")
        finally:
            return data

    def get_home_type(self):
        hometype = self.data['homeType'].unique()
        return list(hometype)

    def get_home_type_encoded(self):
        hometype = self.data['homeType_encoded'].unique()
        return list(hometype)

    def get_cities(self):
        city = self.data['city'].unique()
        return list(city)

    def get_cities_encoded(self):
        city = self.data['city_encoded'].unique()
        return list(city)

    def get_zipcode(self):
        zipcode = self.data['zipcode'].unique()
        return list(zipcode)

    def get_zipcode_encoded(self):
        zipcode = self.data['zipcode_encoded'].unique()
        return list(zipcode)
