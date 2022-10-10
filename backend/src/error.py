'''
File containing error codes and exceptions raised
'''
from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    '''
    Error code 400 for an AccessError
    '''
    code = 400
    message = 'No message specified'

class InputError(HTTPException):
    '''
    Error code 400 for an InputError
    '''
    code = 400
    message = 'No message specified'
