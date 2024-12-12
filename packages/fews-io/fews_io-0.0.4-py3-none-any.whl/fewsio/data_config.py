import logging
import os
import xml.etree.ElementTree as ET  # noqa: N817
from abc import ABC, abstractmethod

from .common import NAMESPACES, ParameterId, TimeseriesId

ns = NAMESPACES

logger = logging.getLogger("fews-io")


class DataConfigBase(ABC):
    @abstractmethod
    def timeseries_id_to_string_id(self, timeseries_id: TimeseriesId) -> str:
        """
        Map a TimeseriesId object to its corresponding string identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def string_id_to_timeseries_id(self, timeseries_string_id: str) -> TimeseriesId:
        """
        Map a string identifier to its corresponding TimeseriesId object.
        """
        raise NotImplementedError

    @abstractmethod
    def parameter_id_to_string_id(self, parameter_id: ParameterId) -> str:
        """
        Map a ParameterId object to its corresponding string identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def string_id_to_parameter_id(self, parameter_string_id: str) -> ParameterId:
        """
        Map a string identifier to its corresponding ParameterId object.
        """
        raise NotImplementedError


class XMLDataConfig(DataConfigBase):
    """
    Used to map PI-XML timeseries and parameters to string identifiers.
    """

    def __init__(self, path):
        """
        Parse data config file

        :param path: Path to data config .xml file.
        """
        self.__variable_map = {}
        self.__location_parameter_ids = {}
        self.__parameter_map = {}
        self.__model_parameter_ids = {}

        try:
            tree = ET.parse(path)
            root = tree.getroot()

            timeseriess1 = root.findall("./*/fews:timeSeries", ns)
            timeseriess2 = root.findall("./fews:timeSeries", ns)
            timeseriess1.extend(timeseriess2)

            for timeseries in timeseriess1:
                pi_timeseries = timeseries.find("fews:PITimeSeries", ns)
                if pi_timeseries is not None:
                    internal_id = timeseries.get("id")
                    external_id = TimeseriesId.from_xml_element(pi_timeseries, "fews")

                    if internal_id in self.__location_parameter_ids:
                        message = (
                            "Found more than one external timeseries "
                            "mapped to internal id {} in {}."
                        ).format(internal_id, path)
                        logger.error(message)
                        raise Exception(message)
                    elif external_id in self.__variable_map:
                        message = (
                            "Found more than one internal timeseries "
                            "mapped to external id {} in {}."
                        ).format(external_id, path)
                        logger.error(message)
                        raise Exception(message)
                    else:
                        self.__location_parameter_ids[internal_id] = TimeseriesId.from_xml_element(
                            pi_timeseries, "fews"
                        )
                        self.__variable_map[external_id] = internal_id

            for k in ["import", "export"]:
                res = root.find("./fews:%s/fews:PITimeSeriesFile/fews:timeSeriesFile" % k, ns)
                if res is not None:
                    setattr(self, "basename_%s" % k, os.path.splitext(res.text)[0])

            parameters = root.findall("./fews:parameter", ns)
            if parameters is not None:
                for parameter in parameters:
                    pi_parameter = parameter.find("fews:PIParameter", ns)
                    if pi_parameter is not None:
                        internal_id = parameter.get("id")
                        external_id = ParameterId.from_xml_element(pi_parameter, "fews")

                        if internal_id in self.__model_parameter_ids:
                            message = (
                                "Found more than one external parameter mapped "
                                "to internal id {} in {}."
                            ).format(internal_id, path)
                            logger.error(message)
                            raise Exception(message)
                        if external_id in self.__parameter_map:
                            message = (
                                "Found more than one interal parameter mapped to external "
                                "modelId {}, locationId {}, parameterId {} in {}."
                            ).format(
                                external_id.model_id,
                                external_id.location_id,
                                external_id.parameter_id,
                                path,
                            )
                            logger.error(message)
                            raise Exception(message)
                        else:
                            self.__model_parameter_ids[internal_id] = ParameterId.from_xml_element(
                                pi_parameter, "fews"
                            )
                            self.__parameter_map[external_id] = internal_id

        except IOError:
            logger.error('Data config file "{}" could not be found.'.format(path))
            raise

    def timeseries_id_to_string_id(self, timeseries_id: TimeseriesId) -> str:
        """
        Map a TimeseriesId object to its corresponding string identifier.
        """
        return self.__variable_map[timeseries_id]

    def string_id_to_timeseries_id(self, timeseries_string_id: str) -> TimeseriesId:
        """
        Map a string identifier to its corresponding TimeseriesId object.
        """
        return self.__location_parameter_ids[timeseries_string_id]

    def parameter_id_to_string_id(self, parameter_id: ParameterId) -> str:
        """
        Map a ParameterId object to its corresponding string identifier.
        """
        return self.__parameter_map[parameter_id]

    def string_id_to_parameter_id(self, parameter_string_id: str) -> ParameterId:
        """
        Map a string identifier to its corresponding ParameterId object.
        """
        return self.__model_parameter_ids[parameter_string_id]
