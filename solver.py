import numpy as np


# We shouldn't need height and width to be passed in so we'll make it an optional parameter.
def solver(corners_in, height_width=-1):
    # Convert into a numpy array. This gives us flexibility because np.array will accept almost anything and turn
    # it into an a numpy array.
    corners_unsorted = np.array(corners_in)

    # Sort the array.
    corners = sort_array(corners_unsorted)

    # Verify shape of array
    check_array_shape(corners)

    # Assign each corner to a named variable for readability.
    bottom_left = corners[0]
    top_left = corners[1]
    bottom_right = corners[2]
    top_right = corners[3]

    # Verify that the corners form a valid square
    check_corners(bottom_left, top_left, bottom_right, top_right)

    # Calculate height and width, ensure given height and width match and perform various checks to ensure
    # we get valid results.
    height, width = get_valid_height_width(bottom_left, top_left, bottom_right, top_right, height_width)

    # Calculate our solution.
    solution = calc_solution(bottom_left, top_left, bottom_right, top_right, height, width)

    # Return our solution as a List.
    return np.ndarray.tolist(solution)


def sort_array(corners_unsorted):
    # Sort the array. Catch any errors and add some context.
    try:
        # Using lexsort allows us more precise control over our sort. This way we can sort by the x value first
        # and the y value second. It returns indices of corners_unsorted in a sorted order.
        ind = np.lexsort((corners_unsorted[:, 1], corners_unsorted[:, 0]))
        # Lets create a new list and use a for loop to append the values from corners_unsorted in the right order
        corners_temp_list = []
        for x in ind:
            corners_temp_list.append(corners_unsorted[x])
        # Finally lets convert it into a numpy array
        corners = np.array(corners_temp_list)
    # Catch any errors and add a little context.
    except TypeError as e:
        raise TypeError("There was an issue sorting the corners array in Pixel Coordinate Solver Function: " + str(e))

    return corners


def check_array_shape(corners):
    # If the shape of the resulting array is wrong then raise a type Exception
    if corners.shape != (4, 2):
        raise ValueError(
            "The shape of the corners array in the Pixel Coordinate Solver Function is :" + str(corners.shape) +
            " when it should be (4, 2).")


def check_corners(bottom_left, top_left, bottom_right, top_right):
    # Validate that the corners form a valid, un-rotated rectangle.
    valid = True

    if top_left[0] != bottom_left[0]:
        valid = False

    if top_right[0] != bottom_right[0]:
        valid = False

    if top_left[1] != top_right[1]:
        valid = False

    if bottom_left[1] != bottom_right[1]:
        valid = False

    if valid is False:
        raise ValueError("Invalid rectangle corners entered into the Pixel Coordinate Solver function.")


def get_valid_height_width(bottom_left, top_left, bottom_right, top_right, height_width):
    # Let's calculate the height and width from the corners.
    width = top_right[0] - top_left[0] + 1
    height = top_left[1] - bottom_left[1] + 1

    # Check to make sure that the given corners allow for a integer width / height.
    if (width - int(width)) != 0 or (height - int(height)) != 0:
        raise ValueError("The corners passed into Pixel Coordinate Solver Function don't allow for a "
                         "valid number of pixels between them. Make sure the given corners allows for "
                         "integer width / height.")

    # We'll cast our results to int because if they were calculated from floats than they will still be floats.
    # We need them as ints for later use in the range function.
    width = int(width)
    height = int(height)

    # We'll ensure that the height and width calculated are valid. If they aren't this means the corners
    # are invalid.
    if width < 1:
        raise ValueError("The Width calculated from the corners array passed into Pixel Coordinate Solver "
                         "Function is invalid. This means the corners are invalid.")

    if height < 1:
        raise ValueError("The Height calculated from the corners array passed into Pixel Coordinate Solver "
                         "Function is invalid. This means the corners are invalid.")

    # If the caller passed in a value of height and width then lets make sure it matches with what we calculated.
    # If they don't pass in a value then we will ignore it.
    if height_width != -1:
        # We'll use a try block in case a valid Tuple with at least two wasn't passed in.
        # We won't worry about if more than two were passed in. If the first two values aren't valid
        # we'll handle that later.
        try:
            height_extracted = height_width[0]
            width_extracted = height_width[1]

            # If they pass in a decimal height / width we will ignore it and use our calculated values.
            if (height_extracted - int(height_extracted)) != 0 or (width_extracted - int(width_extracted)) != 0:
                height_extracted = height
                width_extracted = width

        except TypeError:
            raise TypeError("Height and width passed into Pixel Coordinate Solver Function is not a valid Tuple.")

        # If there is a mismatch in the calculated width/height and the given width/height let's raise an
        # exception so that the caller knows something has gone wrong.
        raise_value_error = False
        error_to_raise_height = ""
        error_to_raise_width = ""
        if height != height_extracted:
            raise_value_error = True
            error_to_raise_height = "The Height passed in does not match the corner values passed in. "

        if width != width_extracted:
            raise_value_error = True
            error_to_raise_width = "The Width passed in does not match the corner values passed in."

        if raise_value_error:
            raise ValueError(
                "Errors Found in Pixel Coordinate Solver Function: " + error_to_raise_height +
                error_to_raise_width)

    return height, width


def calc_solution(bottom_left, top_left, bottom_right, top_right, height, width):
    # Now that we're sure of our inputs lets calculate the output array.
    # We'll create an empty array to hold our solution.
    solution = np.empty((height, width, 2))
    # We'll calculate a starting x coordinate that we can add onto.
    start_x = bottom_left[0]

    # On the theoretical computer screen we are calculating pixel coordinates for, the position represented
    # by y gets larger as you "ascend." However, in our numpy array y gets smaller as you "ascend" and larger
    # as you "descend." Because of this we will start at the maximum of y and decrement it as we "descend" down
    # our numpy array.
    start_y = top_left[1]

    # One for loop to iterate over the width.
    for y in range(height):
        # One for loop to iterate over the height.
        for x in range(width):
            solution[y][x][0] = start_x + x
            solution[y][x][1] = start_y - y

    return solution
