"""Uses a Flask provided mechanism to handle errors in the an application.
When an error is detected we return a custom error templates. """

from flask import render_template
from app import app, db

@app.errorhandler(401)
def page_not_found_error(error):
    """Declares custom error handler through errorhandler decorator for when
    Unauthorized access error is thrown. Returns 401 error template and error code.
    args:
        error: Flask error object.
    """
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found_error(error):
    """Declares custom error handler through errorhandler decorator for when
    page not found error is thrown. Returns 404 error template and error code.
    args:
        error: Flask error object.
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Declares custom error handler through errorhandler decorator for when
    server error is thrown. Rollsback any changes to the database in case of error.
    Returns 500 error template and error code.
    args:
        error: Flask error object.
    """
    db.session.rollback()
    return render_template('500.html'), 500
