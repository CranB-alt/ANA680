from flask import Flask, render_template, request
import numpy as np
import pickle
import os

app = Flask(__name__)

#Model and features
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
features = pickle.load(open(os.path.join(BASE_DIR, "features.pkl"), "rb"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", predict="", values={})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        #User input
        values = {
            "bare_nuclei": request.form.get("bare_nuclei", ""),
            "uniformity_cell_shape": request.form.get("uniformity_cell_shape", ""),
            "uniformity_cell_size": request.form.get("uniformity_cell_size", ""),
            "bland_chromatin": request.form.get("bland_chromatin", "")
        }


        if "" in values.values():
            return render_template("index.html", predict="", values=values)


        X = np.array([[float(values[f]) for f in features]])

        #Prediction
        pred = model.predict(X)[0]
        label = "Malignant" if pred == 1 else "Benign"

        return render_template("index.html", predict=label, values=values)

    except Exception as e:
        return render_template("index.html", predict=f"Error: {e}", values={})

if __name__ == "__main__":
    app.run(debug=True)
