from . import _VDAPIService, _VDDuplicateableResponse, V1API

class _ClearLineDealAPI(_VDAPIService):

    __API_FACTORY__ = staticmethod(V1API)
    __RESPONSE_OBJECT__ = _VDDuplicateableResponse
    __API__ = 'clearline_deals'
