class APIError(Exception):
    def __init__(self, message=None, data=None):
        if message is None:
            message = getattr(self, 'default_message', "API Error")
        if data:
            message += ' : ' + str(data)
        super().__init__(message)


class InvalidToken(APIError):
    default_message = 'API Request Error - Invalid Token'


class InvalidMethod(APIError):
    default_message = 'API Request Error - Invalid Method'


class InvalidModelId(APIError):
    default_message = 'API Request Error - Invalid Model ID'


class InvalidPluginPathError(APIError):
    default_message = 'API Request Error - Invalid Plugin Path'


class InvalidInvalidData(APIError):
    default_message = 'API Request Error: Invalid Data - Parameters must satisfy Min < Max and Min ≤ Base ≤ Max.'


class InvalidModelPath(APIError):
    default_message = 'API Request Error - Invalid Model Path'


class InvalidItemId(APIError):
    default_message = 'API Request Error - Invalid Item ID'


class InvalidItemPath(APIError):
    default_message = 'API Request Error - Invalid Item Path'


class InvalidMotionPath(APIError):
    default_message = 'API Request Error - Invalid Motion Path'


class InvalidExpressionPath(APIError):
    default_message = 'API Request Error - Invalid Expression Path'


class InvalidSceneId(APIError):
    default_message = 'API Request Error - Invalid Scene ID'


class ErrorManager:
    
    def __init__(self, error_type, request, response):
        self.error_type = error_type
        self.exception = ValueError
        self.data = response
        self.request = request
        self.manage_error()
    
    def manage_error(self):
        values = self.request.get('Data')

        if self.error_type == 'InvalidMethod':
            raise InvalidMethod(data=self.request.get('Method'))
        elif self.error_type == 'InvalidToken':
            raise InvalidToken()
        elif self.error_type == 'InvalidModelId':
            raise InvalidModelId(data=values.get('ModelId'))
        elif self.error_type == 'InvalidPluginPathError':
            raise InvalidPluginPathError(data=values.get('PluginPath'))
        elif self.error_type == 'InvalidData':
            raise InvalidInvalidData()
        elif self.error_type == 'InvalidModelPath':
            raise InvalidModelPath(data=self.data.get('ModelPath'))
        elif self.error_type == 'InvalidItemId':
            raise InvalidItemId(data=values.get('ItemId'))
        elif self.error_type == 'InvalidExpressionPath':
            raise InvalidExpressionPath(data=values.get('ExpressionPath'))
        elif self.error_type == 'InvalidMotionPath':
            raise InvalidMotionPath(data=self.data.get('MotionPath'))
        elif self.error_type == 'InvalidItemPath':
            raise InvalidItemPath(data=values.get('ItemPath'))
        elif self.error_type == 'InvalidSceneId':
            raise InvalidSceneId(data=values.get('SceneId'))
        else:
            raise APIError(data=self.data)
