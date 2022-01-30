from tensorflow import keras

"""
predict and parse output of dnn model.

input data is a len = 10 list or array
"""

def dnn_predict(model, sample):
    pred = model.predict(sample)
    cat_pred = np.zeros_like(pred)
    for n,p in enumerate(pred):
        cat_pred[n,:] = [round(i) for i in p]
    return cat_pred

if __name__ == '__main__':
    model = keras.models.load_model("dnn_predictor.krs")
    dnn_predict(model, [0,0,0,0,0,0,1,0,0,0])