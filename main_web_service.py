from solver import *
from flask import Flask, request
from werkzeug.exceptions import BadRequest
import os

app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def main():

    # If the user sends a GET request we'll give them some guidance.
    if request.method == 'GET':
        return "Please use a post request with data sent as either form data or JSON. " \
               "For an html page or script to do so please see: "

    # Get the body of the POST.
    list_in, hw = get_post_body()

    # Run the solver on the input.
    sol = run_solver_on_list(list_in, hw)

    # Format the output as a string and add whitespace.
    string_out = format_as_string(sol)

    # Return / display our solution.
    return string_out


def get_post_body():
    # Get the body of the POST.
    try:
        # This section handles input from an html form.
        list_in = [(float(request.form['corner11']), float(request.form['corner12'])),
                   (float(request.form['corner21']), float(request.form['corner22'])),
                   (float(request.form['corner31']), float(request.form['corner32'])),
                   (float(request.form['corner41']), float(request.form['corner42']))]

        # Get (if it exists) the height/width values. We use a separate try/except because we want to just set
        # hw to None if it doesn't exist or let the user know if it's a decimal
        try:
            hw = (int(request.form['height']), int(request.form['width']))
        except ValueError as e:
            hw = None

    except BadRequest as e:

        # If the data wasn't formatted from an html form then we'll try and read it in JSON.
        try:
            data_in = request.get_json(force=True)
            list_in = [(data_in.get('corner11'), data_in.get('corner12')),
                       (data_in.get('corner21'), data_in.get('corner22')),
                       (data_in.get('corner31'), data_in.get('corner32')),
                       (data_in.get('corner41'), data_in.get('corner42'))]
            # Get (if it exists) the height/width values.
            hw = (data_in.get('height'), data_in.get('width'))

            # If they don't exist then set hw to None
            if hw[0] is None or hw[1] is None:
                hw=None

        except BadRequest as e:
            # If there is still an issue than we will add some context and send it to the user.
            raise BadRequest("Error 400 Bad Request. Data should be sent as either form data or JSON. " + str(e))

    except ValueError as e:
        raise BadRequest("Invalid Corner Input. Are all of the corner fields filled in with valid options? ")

    return list_in, hw


def run_solver_on_list(list_in, hw):
    # Run the solver on the input.
    try:
        if hw is None:
            sol = solver(list_in)
            print("hw is none")
        else:
            sol = solver(list_in, hw)
            print("hw is not none")
    # If the is an issue than display it to the user.
    except (TypeError, ValueError) as e:
        raise BadRequest("Error 400: Bad Request. Problem Parsing corners input: " + str(e))

    return sol


def format_as_string(sol):
    # Format the output as a string and add whitespace.
    string_out = "solution = [<br/>"
    for x in sol:
        string_out += "&emsp;&emsp;" + str(x) + ",<br/>"
    # Make sure there isn't a comma at the end of the last row.
    string_out = string_out[:-6]
    string_out += "<br/>&emsp;]"

    return string_out


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
