import os


def is_none_decorator(argument):
    def real_decorator(function):
        def wrapper(self, *args, **kwargs):
            if getattr(self, argument, None) is None:
                return 'Trade data is not loaded.'
            return function(self, *args, **kwargs)
        return wrapper
    return real_decorator


def get_csv_files(dir):
    """
    Find all .cvs files in given dir and 
    return full path list of files
    """
    csv_files = []
    for file in os.listdir(dir):
        if file.lower().endswith(".csv"):
            csv_files.append(os.path.join(dir, file))
    print("Trade CSV files found: {}.".format(', '.join(csv_files)))
    return csv_files
