import pyrebase
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import pdb
import collections
# importing the firebase auth cridentials
from firebase import firebaseConfig as firebaseConfig

app = Flask(__name__)

app.secret_key = "super secret key"
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
# insilized the database
db = firebase.database()


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


@app.route("/delete", methods=['POST'])
def delete():
    try:
        name = request.form['remove']
        # name = request.form.get['remove']
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
    ref = db.child("ToDo").get()
    values = ref.val()
    listing = convert(values)

    items = listing.keys()
    list_val = listing.values()
    # pdb.set_trace()
    return render_template('todo.html', list_val=list_val)


if __name__ == '__main__':
    app.run(debug=True)
