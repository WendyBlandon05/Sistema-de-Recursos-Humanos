class ResponseData:
    def __init__(self, Success, Status, Message, Record=None):
        self.Success = Success
        self.Status = Status
        self.Message = Message
        self.Record = Record

    def toResponse(self):
        # Convierte los atributos de la instancia en un diccionario
        return self.__dict__
