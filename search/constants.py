"""This file is for contstants in order to easy access to them and change """
GITHUB_API = 'https://api.github.com/search/repositories?q='
BITBUCKET_API = ''
LOG_FILE = 'loggingfile.log'

class GlobalVariable():
    """This class is for global variables in order to easy access to them and change """
    def __init__(self):
        self.__current_data = []
        self.__host_name = ''

    def get_current_data(self):
        """This method is for getting current data """
        return self.__current_data

    def set_current_data(self, current_data):
        """This method is for setting current data """
        self.__current_data = current_data

    def get_host_name(self):
        """This method is for getting host name """
        return self.__host_name

    def set_host_name(self, host_name):
        """This method is for getting host name """
        self.__host_name = host_name
