# model_predict.py
import joblib

class ModelPredict:
    def __init__(self):
        self.__nb_model = joblib.load("model_ml/naive_bayes_model.pkl")
        self.__svm_model = joblib.load("model_ml/SVM_model.pkl")
        self.__vectorizer = joblib.load("model_ml/vectorizer.pkl")

    def __vectorize(self, text):
        return self.__vectorizer.transform([text])

    def __label(self, pred):
        return "POSITIF" if pred[0] == 1 else "NEGATIF"

    def predict_nb(self, text):
        vec = self.__vectorize(text)
        return self.__label(self.__nb_model.predict(vec))

    def predict_svm(self, text):
        vec = self.__vectorize(text)
        return self.__label(self.__svm_model.predict(vec))
