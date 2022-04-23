import requests
import numpy as np


# You can use this script one of two ways. Firstly, you can run it and input the values.
# Secondly you can comment out line 18 and edit the 2d array defined on lines 8 - 12 and the tuple on line 15.

def main():
    # Setup default corners.
    corner_points = [
        (1, 1),  # (x, y)
        (3, 1),  # (x, y)
        (1, 3),  # (x, y)
        (3, 3)]  # (x, y)

    # Setup default height/width that matches our default corners.
    # If you want to just ignore height/width you can set them to 0.
    height_width = (3, 3)  # (height, width)

    # If you want to just edit the script and not use the command line comment out the next line:
    corner_points, height_width = get_user_input()

    # Setup dictionary for use in our POST request.
    dict_to_send = {'corner11': corner_points[0][0], 'corner12': corner_points[0][1],
                    'corner21': corner_points[1][0], 'corner22': corner_points[1][1],
                    'corner31': corner_points[2][0], 'corner32': corner_points[2][1],
                    'corner41': corner_points[3][0], 'corner42': corner_points[3][1]}

    # We'll check if our height/width is valid input. If not it will just get ignored
    # If the height/width isn't a number the try/except block will make sure it's ignored.
    # If the height/width isn't greater than 0 the if block will make sure it's ignored.
    # Those last two would also be handled server side if they slipped through somehow.
    # If the height/width is a decimal the server will make sure it's ignored.
    # If its valid but doesn't match the corner values than the server will reply telling us so.
    try:
        if height_width[0] > 0 and height_width[1] > 0:
            dict_to_send.update({'height': height_width[0]})
            dict_to_send.update({'width': height_width[1]})
    except TypeError:
        pass

    # Send the POST and get the response.
    response = requests.post('http://127.0.0.1:5000/', json=dict_to_send)

    # Our response has html formatting. Let's replace it to make it readable in the script output.
    response = de_html(response.text)

    # Print our result
    print(response)


# Our response has html formatting. Let's replace it to make it readable in the script output.
def de_html(text):
    text = text.replace('<br/>', '\n')
    text = text.replace('&emsp;', '\t')
    return text


# This functions gets user input
def get_user_input():
    # We will use a try/except block to catch any issues with user input and prompt them again recursively.
    try:
        # Prompt and get user input.
        string_in = input("Please enter your values (including Words like corner, width, and height) like so "
                          "(I suggest copy, pasting, and replacing within parentheses):"
                          "\nCorner1: (x,y) Corner2: (x,y) Corner3: (x,y) Corner4: (x,y) Height/Width: (h, w)\n"
                          "Height/Width values are optional and can be set to 0 if you want to not use them.")

        # Adding a space before user input allows for correct processing of input in case the user cuts
        # off the first part of their input.
        string_in = " " + string_in

        # Define an empty list we'll add to later.
        corners = []

        # Split the list and remove the first useless part.
        temp_list = string_in.split('(')
        temp_list = temp_list[1:]

        # Split items in the list and keep only useful parts.
        for x in range(len(temp_list)):
            temp_list[x] = temp_list[x].split(")")[0]

        # Extract the numerical values for the corners from the list.
        for x in range(len(temp_list) - 1):
            tuple_string_list = temp_list[x].split(",")
            corners.append((float(tuple_string_list[0]), float(tuple_string_list[1])))

        # Finally pull out the height/width.
        tuple_string_list = temp_list[-1].split(",")
        height = float(tuple_string_list[0])
        width = float(tuple_string_list[1])

        # Convert the list to a numpy array for easy shape checking.
        # If the shape is incorrect raise an exception.
        n_corner_array = np.asarray(corners)
        if n_corner_array.shape != (4, 2):
            raise ValueError("Incorrect amount of values entered!")

    except (IndexError, ValueError) as e:
        # If an exception has been raised then give the user some hints and another chance using recursion.
        print("Something went wrong: " + str(e) + "Ensure that you have numeric values at the right places."
                                                  "Your input should be something like: \"Corner1: (1,1) Corner2: "
                                                  "(1,3) Corner3: (3,1) Corner4: (3,3) Height/Width: (3, 3)\""
                                                  "\nPlease try again!")
        corners, (height, width) = get_user_input()

    # Return our values.
    return corners, (height, width)


# Main method to run the script
if __name__ == '__main__':
    main()
