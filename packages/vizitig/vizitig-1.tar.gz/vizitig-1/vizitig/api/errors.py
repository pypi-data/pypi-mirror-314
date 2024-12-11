from fastapi import HTTPException

from vizitig import version as viz_version
from vizitig.errors import NoGraphException as InfoNoGraphException


class NoGraphException(InfoNoGraphException, HTTPException):
    def __init__(self, **kwargs):
        detail = kwargs.pop("detail", "")
        super().__init__(detail=f'No Graph "{detail}"', **kwargs)


class NotFoundException(HTTPException):
    _object = "Something"

    def __init__(self, **kwargs):
        detail = kwargs.pop("detail", "")
        super().__init__(detail=f'{self._object} not found: "{detail}"', **kwargs)


class NodeNotFoundException(NotFoundException):
    _object = "Node"


class MetaDataNotFoundException(NotFoundException):
    _object = "Metadata key"


class NoPathFoundException(NotFoundException):
    _object = "No path found"


class UnknownFormat(NotFoundException):
    _object = "Format not found"


class ExportError(NotFoundException):
    _object = "Error during export"


class ReservedKeysException(HTTPException):
    def __init__(self, **kwargs):
        detail = kwargs.pop("detail", "")
        super().__init__(detail=f'Reserved keys "{detail}"', **kwargs)


class InvalidKmerSize(HTTPException):
    def __init__(self, **kwargs):
        seq = kwargs.pop("seq", "")
        k = kwargs.pop("k", "")
        detail = f"{seq} ({len(seq)}!={k})" if seq and k else ""
        super().__init__(detail=f'Invalid Kmersize: "{detail}"', **kwargs)


class QueryError(HTTPException):
    _object = "Error while parsing"


class GraphNameAlreayTaken(HTTPException):
    def __init__(self, **kwargs):
        name = kwargs.pop("name")
        super().__init__(detail=f"Graph name {name} already taken", status_code=400)


class NoEmptyGraphNameAllowed(HTTPException):
    _object = "No empty graph name allowed"


class UnsupportedExtension(HTTPException):
    def __init__(self, **kwargs):
        ext = kwargs.pop("extension")
        super().__init__(detail=f"Unsupported extension {ext}", status_code=400)


class IncompatibleViziGraph(HTTPException):
    def __init__(self, **kwargs):
        version = kwargs.pop("version")
        super().__init__(
            detail=f"Incompatible vizitig version ({version} vs {viz_version})",
        )
