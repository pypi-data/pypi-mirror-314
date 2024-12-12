import xml.etree.ElementTree as ET  # noqa: N817
from dataclasses import dataclass
from typing import Iterable


ns = NAMESPACES = {
    "fews": "http://www.wldelft.nl/fews",
    "pi": "http://www.wldelft.nl/fews/PI",
}


@dataclass(frozen=True)
class ParameterId:
    model_id: str
    location_id: str
    parameter_id: str

    @classmethod
    def from_xml_element(cls, el: ET.Element, namespace) -> "ParameterId":
        model_id = el.find(namespace + ":modelId", ns).text
        location_id = el.find(namespace + ":locationId", ns).text
        parameter_id = el.find(namespace + ":parameterId", ns).text

        return cls(
            model_id=(model_id if model_id is not None else ""),
            location_id=(location_id if location_id is not None else ""),
            parameter_id=(parameter_id if parameter_id is not None else ""),
        )


@dataclass(frozen=True)
class TimeseriesId:
    location_id: str
    parameter_id: str
    qualifier_ids: frozenset = frozenset()

    def __init__(self, location_id: str, parameter_id: str, *qualifier_ids: Iterable[str]):
        object.__setattr__(self, "location_id", location_id)
        object.__setattr__(self, "parameter_id", parameter_id)
        object.__setattr__(self, "qualifier_ids", frozenset(qualifier_ids))

    @classmethod
    def from_xml_element(cls, el: ET.Element, namespace: str) -> "TimeseriesId":
        location_id = el.find(namespace + ":locationId", ns).text
        parameter_id = el.find(namespace + ":parameterId", ns).text

        qualifiers = el.findall(namespace + ":qualifierId", ns)
        qualifier_ids = []
        for qualifier in qualifiers:
            qualifier_ids.append(qualifier.text)

        return cls(location_id, parameter_id, *qualifier_ids)
