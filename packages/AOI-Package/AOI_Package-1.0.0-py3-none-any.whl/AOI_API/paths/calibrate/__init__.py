# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from AOI_API.paths.calibrate import Api

from AOI_API.paths import PathValues

path = PathValues.CALIBRATE