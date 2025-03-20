def response(status: int, message: str, data: any = None) -> dict:
    """
    Create a response
    :param status: The status code
    :param data: The data
    :param message: The message
    :return: The response
    """
    return {
        "status": status,
        "data": data,
        "message": message,
    }
