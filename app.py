from website import create_app, db
#from flask import render_template

app = create_app()
db.create_all(app=create_app())


"""@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return render_template("500.html"), 500"""

if __name__ == "__main__" :

    app.run(debug=True)
