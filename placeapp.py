from flask import Flask, request, render_template
import pickle
import numpy as np

placeapp = Flask(__name__, template_folder='template')
model = pickle.load(open('op.pkl', 'rb'))
salary = pickle.load(open('salary.pkl', 'rb'))


@placeapp.route('/')
def home():
    return render_template('home.html')


@placeapp.route('/', methods=['POST'])
def predict():
    '''
        For rendering results in HTML GUI
    '''
    # features = [x for x in request.form.values()]
    features = []
    for i in request.form.values():
        if i == 'Male' or i == 'Female':
            if i == 'Male':
                i = 0
            else:
                i = 1
        if i == 'Science' or i == 'Commerce' or i == 'Arts':
            if i == 'Science':
                i = 0
            elif i == 'Commerce':
                i = 1
            else:
                i = 2
        if i == 'Science and Technology' or i == 'Commerce and Management' or i == 'Architecture and Others':
            if i == 'Science and Technology':
                i = 0
            if i == 'Commerce and Management':
                i = 1
            if i == 'Architecture and Others':
                i = 2
        if i == 'Yes' or i == 'No':
            if i == 'Yes':
                i = 1
            else:
                i = 0
        try:
            # if isinstance(float(i),float):
            if type(float(i)) == float:
                i = float(i) / 100
        except ValueError:
            continue
        features.append(i)

    final_features = [np.array(features, dtype='f')]
    predictions = model.predict(final_features)
    sal = salary.predict(final_features)
    if predictions == [1]:
        output = sal[0] * 4
        output = int(output)
        return render_template(
            'home.html',
            prediction_text='''With this track record, YOU WILL BE PLACED!
        And if you work hard you will have a chance of getting a package of {}.00 ₹ per annum '''
            .format(output))
    else:
        output = sal[0] * 1.25
        output = int(output)
        return render_template(
            'home.html',
            prediction_text='''With this track record, you will NOT be PLACED!
        And if you work hard and try... you will have a chance of getting a package of {}.00 ₹ per annum '''
            .format(output))


if __name__ == "__main__":
    placeapp.run(debug=True)
# html khol okar