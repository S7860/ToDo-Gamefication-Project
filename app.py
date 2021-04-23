from firebase import firebaseConfig as firebaseConfig
import pyrebase  # inisilizing the firebase
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import collections  # for creating a dictionary
import pdb  # debugging
from smsNotification import client
import time

# importing the firebase auth cridentials

app = Flask(__name__)

app.secret_key = "super secret key"
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
# insilized the database
db = firebase.database()


def database():
    ref = db.child("ToDo").get()
    values = ref.val()
    listing = convert(values)
    return listing


@app.route("/sms", methods=['POST'])
def sms():
    if request.method == 'POST':
        tel = request.form['phone']
        # progress_bar = request.form['number']

        task_list = database()
        items = task_list.values()

        # pdb.set_trace()

        # if tel.encode("utf-8"):
        #     time.sleep(3600)
        #     client.messages.create(from_="+15623726595",
        #                            body="Don't want to miss out on the Fun!!...Please Continue to Do Your Tasks ",
        #                            to=tel)

        #     return redirect(url_for('homePage'))

    # Keeps sending message at 30 min,  1 hour, then 2 hours later...
    # Check if task for that day is all completed before sending the 4th sms message.


@app.route("/change_progress", methods=['POST'])
def change_progress():
    try:
        if request.method == 'POST':
            progress = request.form['number']

            # pdb.set_trace()
            print("progress rate", progress)

            return redirect(url_for('homePage'))
    except Exception as e:
        flash(e)
        return render_template('todo.html')


@app.route("/delete", methods=['POST'])
def delete():
    try:
        name = request.form['remove']
        # pdb.set_trace()

        if request.method == 'POST':
            name_exist = db.child("TODO").get()
            dct = convert(name_exist.val())

            if name.encode("utf-8"):
                db.child("ToDo").child(name).remove()
                # this allows it to return back to homepage once user inputs.
                return redirect(url_for('homePage'))
        return redirect(url_for('homePage'))
    except Exception as e:
        flash(e)
        return render_template('todo.html')


@app.route("/insert", methods=['POST'])
def insert():
    try:
        task = request.form['addTask']
        date = request.form['date_input']
        # pdb.set_trace()
        if request.method == 'POST':
            name_exist = db.child("TODO").get()
            name = name_exist.val()
            dct = convert(name)

            if task.encode("utf-8") and date.encode("utf-8"):
                data = {"list": task, "due": date}
                db.child("ToDo").child(task).set(data)
                # this allows it to return back to homepage once user inputs.
                return redirect(url_for('homePage'))
        else:
            return render_template('todo.html')
    except Exception as e:
        flash(e)
        return render_template('todo.html')


@app.route("/")
def homePage():
    # ref = db.child("ToDo").get()
    # values = ref.val()
    # listing = convert(values)
    todo = database()
    # items = listing.keys()
    list_val = todo.values()
    # pdb.set_trace()

    return render_template('todo.html', list_val=list_val)

# This creates a dictionary of the inerted items via input


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


if __name__ == '__main__':

    app.run(debug=True)
