from flask import render_template


def feedback_errors(name, message):
    if len(name) > 100:
        return render_template('error.html', error='The name is too long')
    if len(message) > 5000:
        return render_template('error.html', error='The message is too long')
