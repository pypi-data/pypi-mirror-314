import logging
import random
import sys

def handleExit():
    """
    Handles exit scenarios for both Jupyter notebooks and normal Python scripts.
    """
    try:
        # Check if the environment is a Jupyter notebook
        get_ipython
        # Use IPython's exit function for notebooks
        from IPython.display import display, Javascript
        display(Javascript('IPython.notebook.kernel.execute("exit()")'))
        # Raise an exception to stop the current cell execution
        raise SystemExit("Exiting the notebook cell.")      
        quit()
    except NameError:
        import sys
        sys.exit()

def createLogger(log_level = None, name = None, mode = 'a', log_format = None, is_consoleLogger = False, filename = None):
    """
    Creates a logger object with the specified parameters.
    Parameters:
        log_level: The level of logging to be used. Defaults to logging.INFO
        name: The name of the logger. Defaults to a random number between 1 and 100
        mode: The mode of the file handler. Defaults to 'a'
        log_format: The format of the log message. Defaults to "%(asctime)s -%(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        is_consoleLogger: Whether to log to the console. Defaults to False
        filename: The filename to be used for the file handler. Defaults to None
    """
    if log_level is None:
        log_level = logging.INFO
    if log_format is None:
        log_format = "%(asctime)s -%(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    if is_consoleLogger is False:
        if name is None:
            name = "logger"+str(random.randint(1,100))
    else:
        if name is None:
            name = __name__
    logger = logging.getLogger(name)
    if is_consoleLogger is True:
        file_handler = logging.StreamHandler()
    else:
        if filename is None:
            filename = sys.executable.rstrip(".py")+".log"
        file_handler = logging.FileHandler(filename=filename, mode=mode)
    file_handler.setLevel(log_level)
    formater = logging.Formatter(log_format)
    file_handler.setFormatter(formater)
    logger.addHandler(file_handler)
    logger.setLevel(log_level)
    return logger