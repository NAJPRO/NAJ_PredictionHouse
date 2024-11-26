# encoding=utf-8
import logging

import joblib
import pandas as pd

logging.basicConfig(level=logging.DEBUG, filename="app_zillow.log"
                    , filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_model():
    model = None
    try:
        model = joblib.load("model/zillow_prediction_linearRegressor.pkl")
    except:
        logging.error("Erreur lors du chargement du model")
    finally:
        return model


def load_data(path):
    data = None
    try:
        data = pd.read_excel(path)
    except:
        logging.error("Erreur lors de l'ouverture du DataSet")
    finally:
        return data


class ZillowPredictionApi:
    def __init__(self):
        self.columns = ['yearBuilt', 'livingArea', 'bathrooms', 'bedrooms', 'homeType_encoded',
                        'city_encoded', 'streetAddress_encoded', 'county_encoded']
        self.data = load_data("model/finalZillowDataSet.xlsx")
        self.model = load_model()

    def setup_routes(self, data: dict):
        print(type(self.model))
        data_copy = data.copy()  # Copie du dictionnaire reçu en paramètre

        homeType = self.get_home_type()  # On récupère toute les homeType dans la DataSet
        homeType_encoded = self.get_home_type_encoded()  # On récupère toute les homeType dans la DataSet

        city = self.get_city()  # On récupère toute les city de la DataSet
        city_encoded = self.get_city_encoded()  # On récupère toute les city de la DataSet

        streetAddress = self.get_streetAddress()  # On récupère toute les adresse de la DataSet
        streetAddress_encoded = self.get_streetAddress_encoded()

        county = self.get_county()  # On récupère tout les Comptés de la DataSet
        county_encoded = self.get_county_encoded()
        #        items : list = data_copy.values() # On récupère les valeurs envoyer par l'utilisateur
        #       columns = data_copy.keys()   # on récupère les clés de chacune de ces valeurs
        #      l = data['homeType']
        pos_homeType = -1
        pos_city = -1
        pos_streetAddress = -1
        pos_county = -1

        try:
            # On récupère la position de chaque variable catégoricielle dans la liste items
            pos_homeType = homeType.index(data_copy['homeType'])
            pos_city = city.index(data_copy['city'])
            pos_county = county.index(data_copy['county'])
            pos_streetAddress = streetAddress.index(data_copy.get('streetAddress'))


        except:
            logging.error("Erreur lors de la récupération des données envoyé par l'utilisateur")

        data_copy['city_encoded'] = city_encoded[pos_city]
        data_copy['homeType_encoded'] = homeType_encoded[pos_homeType]
        data_copy['county_encoded'] = county_encoded[pos_county]
        data_copy['streetAddress_encoded'] = streetAddress_encoded[pos_streetAddress]

        data_copy['yearBuilt'] = float(data_copy.get('yearBuilt'))
        data_copy['bedrooms'] = float(data_copy.get('bedrooms'))
        data_copy['bathrooms'] = float(data_copy.get('bathrooms'))
        data_copy['livingArea'] = float(data_copy.get('livingArea'))

        data_copy.__delitem__('city')
        data_copy.__delitem__('homeType')
        data_copy.__delitem__('county')
        data_copy.__delitem__('streetAddress')

        value = []
        for keys in self.columns:
            value.append(data_copy[keys])

        final_data = pd.DataFrame([value], columns=list(self.columns))
        predict = self.model.predict(final_data)
        return {'predict': predict.tolist()}

    def get_home_type(self):
        hometype = self.data['homeType'].unique()
        return list(hometype)

    def get_home_type_encoded(self):
        hometype = self.data['homeType_encoded'].unique()
        return list(hometype)

    def get_streetAddress(self):
        streetAddress = self.data['streetAddress'].unique()
        return list(streetAddress)

    def get_streetAddress_encoded(self):
        streetAddress = self.data['streetAddress_encoded'].unique()
        return list(streetAddress)

    def get_city(self):
        city = self.data['city'].unique()
        return list(city)

    def get_city_encoded(self):
        city = self.data['city_encoded'].unique()
        return list(city)

    def get_county(self):
        county = self.data['county'].unique()
        return list(county)

    def get_county_encoded(self):
        county = self.data['county_encoded'].unique()
        return list(county)
