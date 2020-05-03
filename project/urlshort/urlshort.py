from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint,get_flashed_messages
import json
import os.path
from werkzeug.utils import secure_filename
import pymysql
from urlshort.demodb import Database

bp = Blueprint('urlshort',__name__)
print("trying")

urls = {}
db=Database("url_short");
db.create_table();


@bp.route('/')
def home():

    return render_template('home.html', codes=session.keys())

@bp.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        
        db=Database("url_short")
        value=db.insert_data(request.form['url'],request.form["code"],"url")
        print(value)
        if value=="fail":
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))
@bp.route('/your-file', methods=['GET','POST'])
def your_file():
    if request.method == 'POST':
        db=Database("url_short")
        f = request.files['file']
        curdest=os.getcwd()
        full_path = curdest+'/urlshort/static/user_files/' + request.form['code'] + secure_filename(f.filename)
        full_name = request.form['code'] + secure_filename(f.filename)
        value=db.insert_data(full_name,request.form["code"],"file")
        if value=="fail":
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))
        f.save(full_path)
        
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home'))
@bp.route('/<string:code>')
def redirect_to_url(code):
    db=Database("url_short")
    result=db.findrow(code)
    if result==None:
        flash('That short name does not exit. Please enter right value.')
        return redirect(url_for('urlshort.home'))
    elif result["dtype"]=="url":
        return redirect(result["website"])
    elif result["dtype"]=="file":
        return redirect(url_for('static', filename='user_files/' + result["website"]))
        
    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@bp.route('/api')
def session_api():
    return jsonify(list(session.keys()))
