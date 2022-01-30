from tensorflow import keras
import numpy as np

"""
predict and parse output of dnn model.

input data is a len = 10 + 1 list or array of states 
string (like "00", "01", ..)
"""

# Encode measurements outcomes
def parse_input(data):
    out_data = []
    stati = ["00", "01", "10","11"]
    for me in data[0].split(" ")[::-1]:
        out_data.append(stati.index(str(me)))
   return out_data

# Predict sample
def dnn_predict(model, sample):
    pred = model.predict(sample)
    cat_pred = np.zeros_like(pred)
    for n,p in enumerate(pred):
        cat_pred[n,:] = [round(i) for i in p]
    return cat_pred

if __name__ == '__main__':
    model = keras.models.load_model("dnn_predictor.krs")
    dnn_predict(model, [0,0,0,0,0,0,1,0,0,0])
