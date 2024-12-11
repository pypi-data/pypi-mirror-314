import typing_extensions

from AOI_API.paths import PathValues
from AOI_API.apis.paths.calibrate import Calibrate
from AOI_API.apis.paths.scan_board import ScanBoard

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.CALIBRATE: Calibrate,
        PathValues.SCAN_BOARD: ScanBoard,
    }
)

path_to_api = PathToApi(
    {
        PathValues.CALIBRATE: Calibrate,
        PathValues.SCAN_BOARD: ScanBoard,
    }
)
