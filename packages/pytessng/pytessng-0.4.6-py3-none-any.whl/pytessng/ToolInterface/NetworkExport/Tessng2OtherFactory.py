from .tessng2opendrive.Tessng2Opendrive import Tessng2Opendrive
from .tessng2shape.Tessng2Shape import Tessng2Shape
from .tessng2geojson.Tessng2Geojson import Tessng2Geojson
from .tessng2unity.Tessng2Unity import Tessng2Unity
from .tessng2json.Tessng2Json import Tessng2Json


class Tessng2OtherFactory:  # file_path: str, proj_string: str
    mode_mapping = {
        "opendrive": Tessng2Opendrive,
        "shape": Tessng2Shape,
        "geojson": Tessng2Geojson,
        "unity": Tessng2Unity,
        "json": Tessng2Json,
    }

    @classmethod
    def build(cls, netiface, mode: str, params: dict) -> None:
        if mode in cls.mode_mapping:
            model = cls.mode_mapping[mode](netiface)
            model.load_data(params)
        else:
            raise Exception("No This Export Mode!")
