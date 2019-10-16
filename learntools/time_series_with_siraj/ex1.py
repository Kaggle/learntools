import numpy as np
from numpy import newaxis
import matplotlib.pyplot as plt

from learntools.core import *

def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')

    #Pad the list of predictions to shift it in the graph to it's correct start
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Predicted Path')
        plt.legend()
    plt.show()


def predict_sequences_multiple(model, data, window_size, prediction_len):
    #Predict sequence of 50 steps before shifting prediction run forward by 50 steps
    prediction_seqs = []
    for i in range(len(data) // prediction_len):
        curr_frame = data[i*prediction_len]
        predicted = []
        for j in range(prediction_len):
            predicted.append(model.predict(curr_frame[newaxis,:,:])[0,0])
            curr_frame = curr_frame[1:]
            curr_frame = np.insert(curr_frame, [window_size-1], predicted[-1], axis=0)
        prediction_seqs.append(predicted)
    return prediction_seqs

class PlotSirajStockModel(CodingProblem):
    # test are on train_X and val_y. If these are right, others will be right too.
    _vars = ["siraj_model", "X_test", "y_test"]
    _hint = ("")
    _solution = CS("""
    """)

    def check(self, siraj_model, X_test, y_test):
        print("Predicted path at various points in time for siraj_model")
        siraj_predictions = predict_sequences_multiple(siraj_model, X_test, 50, 50)
        plot_results_multiple(siraj_predictions, y_test, 50)

class PlotMyStockModel(CodingProblem):
    # test are on train_X and val_y. If these are right, others will be right too.
    _vars = ["my_model", "X_test", "y_test"]
    _hint = ("")
    _solution = CS("""
    """)

    def check(self, my_model, X_test, y_test):
        print("Predicted path at various points in time for my_model")
        my_predictions = predict_sequences_multiple(my_model, X_test, 50, 50)
        plot_results_multiple(my_predictions, y_test, 50)

qvars = bind_exercises(globals(), [
    PlotSirajStockModel,
    PlotMyStockModel
    ],
    var_format='step_{n}',
    )
__all__ = list(qvars)
