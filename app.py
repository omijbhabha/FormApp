# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # Add this for flash messages
db = SQLAlchemy(app)

# Database models
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fields = db.Column(db.Text, nullable=False)  # Store fields as JSON string

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'), nullable=False)
    answers = db.Column(db.Text, nullable=False)  # Store answers as JSON string

# Initialize the database
with app.app_context():
    db.create_all()

# Add json.loads to the Jinja environment
app.jinja_env.globals.update(json_loads=json.loads)

# Index page
@app.route('/')
def index():
    forms = Form.query.all()
    return render_template('index.html', forms=forms)

# Create a form page
@app.route('/create_form', methods=['GET', 'POST'])
def create_form():
    if request.method == 'POST':
        form_name = request.form['form_name']
        fields = []
        for key, value in request.form.items():
            if key.startswith('field_name'):
                field_number = key.split('_')[-1]
                field_name = value
                field_type = request.form[f'field_type_{field_number}']
                fields.append({'name': field_name, 'type': field_type})
        form = Form(name=form_name, fields=json.dumps(fields))
        db.session.add(form)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_form.html')

# Form filling page
@app.route('/fill_form/<int:form_id>', methods=['GET', 'POST'])
def fill_form(form_id):
    form = Form.query.get_or_404(form_id)
    fields = json.loads(form.fields)
    if request.method == 'POST':
        response = {'form_id': form_id, 'answers': {}}
        for field in fields:
            response['answers'][field['name']] = request.form.get(field['name'])
        db_response = Response(form_id=form_id, answers=json.dumps(response['answers']))
        db.session.add(db_response)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('fill_form.html', form=form, fields=fields)

# View responses page
@app.route('/view_responses/<int:form_id>')
def view_responses(form_id):
    form = Form.query.get_or_404(form_id)
    form_responses = Response.query.filter_by(form_id=form_id).all()
    return render_template('view_responses.html', form=form, responses=form_responses)

# Delete form route
@app.route('/delete_form/<int:form_id>', methods=['POST'])
def delete_form(form_id):
    form = Form.query.get_or_404(form_id)
    responses = Response.query.filter_by(form_id=form_id).all()
    
    # Delete associated responses
    for response in responses:
        db.session.delete(response)
    
    # Delete the form
    db.session.delete(form)
    db.session.commit()
    
    flash('Form and associated responses deleted successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)