from datetime import datetime
from typing import Optional, Set

from oslc4py_domains_auto.oslc_constants import NS_FIT, NS_OSLC_AUTO, VERIFIT_UNIVERSAL_ANALYSIS
from rdflib import DCTERMS, FOAF
from oslc4py_client.Link import Link
from oslc4py_client.OSLCResource import OSLCResource
from oslc4py_client.annotation_types.Occurs import Occurs
from oslc4py_client.annotation_types.ValueType import ValueType
from oslc4py_client.decorators import oslc_name, oslc_namespace, oslc_occurs, oslc_property_definition, oslc_range, oslc_read_only, oslc_resource_shape, oslc_value_type

@oslc_namespace(VERIFIT_UNIVERSAL_ANALYSIS)
@oslc_name("SUT")
@oslc_resource_shape(describes=VERIFIT_UNIVERSAL_ANALYSIS["SUT"], title="SUT Resource Shape")
class SUT(OSLCResource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._launch_command = None
        self._build_command = None
        self._title = None
        self._description = None
        self._created = None
        self._modified = None
        self._identifier = None
        self._sut_directory_path= None
        self._creator = set()
        self._compiled = None
        self._produced_by_automation_request = None
        
    @property
    @oslc_name("launchCommand")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["launchCommand"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def launch_command(self):
        return self._launch_command

    @launch_command.setter
    def launch_command(self, value):
        self._launch_command = value
        
    @property
    @oslc_name("buildCommand")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["buildCommand"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def build_command(self) -> Optional[str]:
        return self._build_command

    @build_command.setter
    def build_command(self, value: str):
        self._build_command = value

    @property
    @oslc_name("title")
    @oslc_property_definition(DCTERMS["title"])
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def title(self) -> Optional[str]:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    @oslc_name("description")
    @oslc_property_definition(DCTERMS["description"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    @oslc_name("created")
    @oslc_property_definition(DCTERMS["created"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.DATETIME)
    @oslc_read_only(False)
    def created(self) -> Optional[datetime]:
        return self._created

    @created.setter
    def created(self, value: datetime):
        self._created = value

    @property
    @oslc_name("modified")
    @oslc_property_definition(DCTERMS["modified"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.DATETIME)
    @oslc_read_only(False)
    def modified(self) -> Optional[datetime]:
        return self._modified

    @modified.setter
    def modified(self, value: datetime):
        self._modified = value

    @property
    @oslc_name("identifier")
    @oslc_property_definition(DCTERMS["identifier"])
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.STRING)
    @oslc_read_only(False)
    def identifier(self) -> Optional[str]:
        return self._identifier

    @identifier.setter
    def identifier(self, value: str):
        self._identifier = value

    @property
    @oslc_name("SUTdirectoryPath")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["SUTdirectoryPath"])
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.XMLLITERAL)
    @oslc_read_only(False)
    def sut_directory_path(self) -> Optional[str]:
        return self._sut_directory_path

    @sut_directory_path.setter
    def sut_directory_path(self, value: str):
        self._sut_directory_path = value

    @property
    @oslc_name("creator")
    @oslc_property_definition(DCTERMS["creator"])
    @oslc_occurs(Occurs.ZERO_OR_MANY)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(FOAF["Person"])
    @oslc_read_only(False)
    def creator(self) -> Set[Link]:
        return self._creator

    def add_creator(self, creator: Link):
        self._creator.add(creator)

    @property
    @oslc_name("compiled")
    @oslc_property_definition(VERIFIT_UNIVERSAL_ANALYSIS["compiled"])
    @oslc_occurs(Occurs.EXACTLY_ONE)
    @oslc_value_type(ValueType.BOOLEAN)
    @oslc_read_only(False)
    def compiled(self) -> Optional[bool]:
        return self._compiled

    @compiled.setter
    def compiled(self, value: bool):
        self._compiled = value

    @property
    @oslc_name("producedByAutomationRequest")
    @oslc_property_definition(NS_OSLC_AUTO["producedByAutomationRequest"])
    @oslc_occurs(Occurs.ZERO_OR_ONE)
    @oslc_value_type(ValueType.RESOURCE)
    @oslc_range(NS_OSLC_AUTO["AutomationRequest"])
    @oslc_read_only(False)
    def produced_by_automation_request(self) -> Optional[Link]:
        return self._produced_by_automation_request

    @produced_by_automation_request.setter
    def produced_by_automation_request(self, value: Link):
        self._produced_by_automation_request = value

    def __str__(self) -> str:
        return f"{{a Local SUT Resource}} - update SUT.__str__() to present resource as desired. {self.about}"