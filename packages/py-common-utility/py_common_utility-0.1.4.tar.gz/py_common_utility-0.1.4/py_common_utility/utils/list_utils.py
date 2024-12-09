def is_list_of_type(obj, row_type):
    # First check if the object is a list
    if isinstance(obj, list):
        # Check if all items in the list are integers
        return all(isinstance(item, row_type) for item in obj)
    return False
