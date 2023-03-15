from flask import render_template, request, redirect, session, url_for, flash, send_file
from main import app, db
from flask_login import login_user, login_required, logout_user, current_user
from main.helper import predict
from main.models import User, MedicalTestResult
from main.forms import LoginForm, RegistrationForm
from datetime import datetime
import os
import numpy as np
from PIL import Image
import tensorflow as tf
import traceback


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/download')
@login_required
def download():
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
        return send_file(db_path, as_attachment=True)
    except Exception as e:
        return str(e)
    
@app.route('/download-page')
@login_required
def download_page():
    return render_template("download.html")
    
@app.route("/diabetes", methods=['GET', 'POST'])
@login_required
def diabetesPage():
    return render_template('diabetes.html')

@app.route("/cancer", methods=['GET', 'POST'])
@login_required
def cancerPage():
    return render_template('breast_cancer.html')

@app.route("/heart", methods=['GET', 'POST'])
@login_required
def heartPage():
    return render_template('heart.html')

@app.route("/kidney", methods=['GET', 'POST'])
@login_required
def kidneyPage():
    return render_template('kidney.html')

@app.route("/liver", methods=['GET', 'POST'])
@login_required
def liverPage():
    return render_template('liver.html')

@app.route("/malaria", methods=['GET', 'POST'])
@login_required
def malariaPage():
    return render_template('malaria.html')

@app.route("/pneumonia", methods=['GET', 'POST'])
@login_required
def pneumoniaPage():
    return render_template('pneumonia.html')

@app.route("/predict", methods = ['POST', 'GET'])
@login_required
def predictPage():
    try:
        if request.method == 'POST':
            to_predict_dict = request.form.to_dict()

            for key, value in to_predict_dict.items():
                try:
                    to_predict_dict[key] = int(value)
                except ValueError:
                    to_predict_dict[key] = float(value)

            to_predict_list = list(map(float, list(to_predict_dict.values())))
            test_type, pred = predict(to_predict_list, to_predict_dict)
            test_result = "positive" if pred == 1 else "negative"
            medical_test_result = MedicalTestResult(user_id=current_user.id, test_type=test_type, result=test_result)
            db.session.add(medical_test_result)
            db.session.commit()

    except Exception as e:
        print(traceback.format_exc())
        message = "Please enter valid data"
        return render_template("home.html", message=message)

    return render_template('predict.html', pred=pred)

@app.route("/malariapredict", methods = ['POST', 'GET'])
@login_required
def malariapredictPage():
    pred = None
    if request.method == 'POST':
        try:
            file = request.files['image']
            img = Image.open(file)
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            img.save(f"main/uploads/{file.filename}")
            img_path = os.path.join(os.path.dirname(__file__), 'uploads', file.filename)
            model_path = os.path.join(os.path.dirname(__file__), 'ml_models', "malaria.h5")
            os.path.isfile(img_path)
            img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
            img = tf.keras.utils.img_to_array(img)
            img = np.expand_dims(img, axis=0)

            model = tf.keras.models.load_model(model_path)
            pred = np.argmax(model.predict(img))
            test_result = "positive" if pred == 1 else "negative"
            test_type = "malaria"
            medical_test_result = MedicalTestResult(user_id=current_user.id, test_type=test_type, result=test_result)
            db.session.add(medical_test_result)
            db.session.commit()
        except Exception as e:
            print(traceback.format_exc())
            message = "Please upload an image"
            return render_template('malaria.html', message=message)
    return render_template('malaria_predict.html', pred=pred)

@app.route("/pneumoniapredict", methods = ['POST', 'GET'])
@login_required
def pneumoniapredictPage():
    pred = None
    if request.method == 'POST':
        try:
            file = request.files['image']
            img = Image.open(request.files['image']).convert('L')
            if not os.path.exists('uploads'):
                os.makedirs('uploads')
            img.save(f"main/uploads/{file.filename}")
            img_path = os.path.join(os.path.dirname(__file__), 'uploads', file.filename)
            model_path = os.path.join(os.path.dirname(__file__), 'ml_models', "pneumonia.h5")
            os.path.isfile(img_path)
            img = tf.keras.utils.load_img(img_path, target_size=(180, 180))
            img = tf.keras.utils.img_to_array(img)
            img = np.expand_dims(img, axis=0)

            model = tf.keras.models.load_model(model_path)
            pred = np.argmax(model.predict(img))
            test_result = "positive" if pred == 1 else "negative"
            test_type = "pneumonia"
            medical_test_result = MedicalTestResult(user_id=current_user.id, test_type=test_type, result=test_result)
            db.session.add(medical_test_result)
            db.session.commit()
        except Exception as e:
            print(traceback.format_exc())
            message = "Please upload an image"
            return render_template('pneumonia.html', message=message)
    return render_template('pneumonia_predict.html', pred=pred)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    session.pop('_flashes', None)
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering " + form.name.data + ". Please login.")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    session.pop('_flashes', None)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get("next")
                if next == None or not not next[0] == "/":
                    next = url_for("home")
                flash("Login Successful")
                return redirect(next)

            else:
                flash("Password is incorrect.")

        else:
            flash("Account does not exist. Pleae register first!")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))