from typing import List

from pydantic import BaseModel


class FileSpecificFields(BaseModel):
    """
    Specific fields for file
    :param List[str] Names: File names
    :param str Sha256: SHA-256 hash
    :param str Sha1: SHA-1 hash
    :param str Md5: MD5 hash
    :param str Sha512: SHA-512
    :param str Tlsh: TLSH hash
    :param str Ssdeep: SSDeep hash
    :param str Imphash: ImpHash
    :param int SizeInBytes: File size in bytes
    """
    Names: List[str] = None
    Sha256: str = ''
    Sha1: str = ''
    Md5: str = ''
    Sha512: str = ''
    Tlsh: str = ''
    Ssdeep: str = ''
    Imphash: str = ''
    SizeInBytes: int = None
