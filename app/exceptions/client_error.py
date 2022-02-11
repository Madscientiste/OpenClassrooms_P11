from werkzeug.exceptions import HTTPException


class ClientError(HTTPException):
    code = 400

    def __init__(self, description=None, response=None, template=None, template_kwargs=None):
        self.response = response
        self.description = description
        self.template = template
        self.template_kwargs = template_kwargs or {}
