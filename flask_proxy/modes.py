from enum import Enum


class VCRMode(Enum):
    playback = "none"
    record = "all"
    off = None

    @classmethod
    def value_of(cls, mode):
        mode = str(mode).lower()
        e = dict(cls.__members__).get(mode)
        if e is None:
            raise ValueError("Invalid VCR mode. Use one of: {}".format(list(cls.__members__.keys())))
        return e