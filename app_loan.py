from flask import Flask, render_template, request, abort, send_from_directory, url_for, redirect
from sklearn.preprocessing import Normalizer
import pandas as pd
import numpy as np
import joblib
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def form():
    return render_template('form.html') 

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    if request.method == "GET":
        return redirect(url_for('form'))
    elif request.method == "POST":
        name = str(request.form['Name'])
        job = str(request.form['Job'])
        income = int(request.form['AppIn'])
        co_income = int(request.form['CoIn'])
        total = int(income + co_income)
        loan = int(request.form['LoAm'])
        term = int(request.form['Term'])
        gender = int(request.form['inlineRadioOptions1'])
        depent = int(request.form['inlineRadioOptions2'])
        marriage = int(request.form['inlineRadioOptions3'])
        edu = int(request.form['inlineRadioOptions4'])
        credit = int(request.form['inlineRadioOptions5'])
        area = int(request.form['inlineRadioOptions6'])

        std = np.array([loan, term, total])
        std = np.reshape(std, (1,-1))
        transform = fit_norm.transform(std)
        print(transform)
        total_new = transform[0][2]
        loan_new = transform[0][0]
        term_new =  transform[0][1]

        x = np.array([loan_new, term_new, total_new, marriage, depent, edu, credit, area])
        x = np.reshape(x, (1,-1))
       
        pred = model.predict(x)
        pred_proba = model.predict_proba(x)
        prediksi = pred[0]
        prediksi_proba = pred_proba[0]

        if prediksi == 1:
            status = 'Approved'
        else:
            status = 'Not Approved'

        if gender == 0:
            sex = 'Female'
        else:
            sex = 'Male'

        if marriage == 0:
            nikah = 'No'
        else:
            nikah = 'Yes'
        
        if edu == 0:
            pend = 'Graduate'
        else:
            pend = 'Non Graduate'
        
        if credit == 0:
            kredit = 'Never'
        else:
            kredit = 'Yes'

        if area == 0:
            lahan = 'Rural'
        elif area == 1:
            lahan = 'Semi-Urban'
        else:
            lahan = 'Urban'

        labels = ['Not Approved', 'Approved']

        plt.figure(figsize=(5,5))
        plt.title('Loan Egibility Percentage')
        plt.pie(x= prediksi_proba, explode=[0.05,0.05], 
            labels=labels, autopct='%1.1f%%', shadow=True)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png', transparent=True)
        plt.close()
        img.seek(0)
        pict_url = base64.b64encode(img.getvalue()).decode()
        pict = f'data:image/png;base64,{pict_url}'

        take_result = {'nama': name, 'pekerjaan': job, 'sex': sex, 
                        'keluarga': depent, 'nikah': nikah, 'pendidikan': pend,
                        'kredit': kredit, 'lahan': lahan, 'pendapatan': total, 
                        'pinjaman': loan, 'jangka': term, 'prediksi': status}
        
        return render_template('result.html', data = take_result, gambar = pict)
    else:
        return redirect(url_for('form'))

@app.route('/filetemp/<path:path>')                           
def filetemp(path):
    return send_from_directory('./templates/image', path)

if __name__ == '__main__':
    model = joblib.load('rfc_model')
    fit_norm = joblib.load('fit_norm')
    app.run(debug=True, port=3000)
