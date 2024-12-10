from pydantic import BaseModel


class ImageConfiguration(BaseModel):
    """
     Image configuration
    :param bytes image: Image binary data
    :param str image_content_type: Image content type
    """

    image: bytes
    image_content_type: str
