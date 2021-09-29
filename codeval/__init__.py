import pkgutil
import keyword
import time


def process(code, fname, kwargs=None, output=None, max_time=0):
    """Evaluate a code snippet given a specific entry-point function to call, keywords-arguments,
     expected output and max time execution

    Parameters:
        - code: string, the code to evaluate

        - fname: string, the name of the entry point function.
        Example: 'my_func'

        - kwargs: dict, the keyword-arguments to test the entry-point function

        - output: object, this is the expected output.

        - max_time: float or int, this is the max time of execution allowed
        for the execution of the code in fractional seconds.
        Defaults to 0, i.e. no max time.

    Returns: Nothing !

    Exceptions:
        - raises IdentifierError if fname or kwargs keys aren't identifiers
        - raises CodevalCodeError when there is an error in the code
        - raises CodevalFunctionError while running the entry-point function
        - raises CodevalOutputError when the expected output isn't returned
        by the entry-point function
        - raises CodevalMaxTimeError when the entry-point function takes longer
        to run than expected
    """
    if not valid_identifier(fname):
        raise IdentifierError("Function name '{}' isn't a valid identifier".format(fname))
    if not kwargs:
        kwargs = ""
    else:
        cache = []
        for key, val in kwargs.items():
            if not valid_identifier(key):
                raise IdentifierError("Argument name '{}' isn't a valid identifier".format(key))
            cache.append("{}={}".format(key, repr(val)))
        kwargs = ", ".join(cache)
    exec_template = pkgutil.get_data("codeval", "exec_template.txt")
    exec_template = exec_template.decode("utf-8")
    exec_text = exec_template.format(code=code, fname=fname, kwargs=kwargs,
                                     output=repr(output), max_time=max_time)
    error_classes = {"CodevalFunctionError": CodevalFunctionError,
                     "CodevalOutputError": CodevalOutputError,
                     "CodevalMaxTimeError": CodevalMaxTimeError}
    try:
        exec(exec_text, error_classes)
    except CodevalFunctionError as e:
        raise e
    except CodevalOutputError as e:
        raise e
    except CodevalMaxTimeError as e:
        raise e
    except Exception as e:
        raise CodevalCodeError(e) from e


def valid_identifier(identifier):
    """Returns True if identifier is valid, else returns False"""
    if not isinstance(identifier, str):
        return False
    if not identifier.isidentifier():
        return False
    if keyword.iskeyword(identifier):
        return False
    return True


class Error(Exception):
    pass


class IdentifierError(Error):
    pass


class CodevalCodeError(Error):
    pass


class CodevalFunctionError(Error):
    pass


class CodevalOutputError(Error):
    pass


class CodevalMaxTimeError(Error):
    pass
