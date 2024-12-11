import typing_extensions

from AOI_API.apis.tags import TagValues
from AOI_API.apis.tags.aoi_api import AOIApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.AOI: AOIApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.AOI: AOIApi,
    }
)
