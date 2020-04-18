# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
from swagger_server import util
from models.ontology_term import OntologyTerm
from models.template_column import TemplateColumn


class Template(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name: str=None, type_template: str=None, descriptiopn: str=None, columns: List[TemplateColumn]=None):  # noqa: E501
        """Template - a model defined in Swagger

        :param name: The name of this Template.  # noqa: E501
        :type name: str
        :param type_template: The type_template of this Template.  # noqa: E501
        :type type_template: str
        :param descriptiopn: The descriptiopn of this Template.  # noqa: E501
        :type descriptiopn: str
        :param columns: The columns of this Template.  # noqa: E501
        :type columns: List[TemplateColumn]
        """
        self.swagger_types = {
            'name': str,
            'type_template': str,
            'descriptiopn': str,
            'columns': List[TemplateColumn]
        }

        self.attribute_map = {
            'name': 'name',
            'type_template': 'typeTemplate',
            'descriptiopn': 'descriptiopn',
            'columns': 'columns'
        }

        self._name = name
        self._type_template = type_template
        self._descriptiopn = descriptiopn
        self._columns = columns

    @classmethod
    def from_dict(cls, dikt) -> 'Template':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Template of this Template.  # noqa: E501
        :rtype: Template
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Template.

        Name of the template  # noqa: E501

        :return: The name of this Template.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Template.

        Name of the template  # noqa: E501

        :param name: The name of this Template.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type_template(self) -> str:
        """Gets the type_template of this Template.

        Type of the Template Sample or Data template  # noqa: E501

        :return: The type_template of this Template.
        :rtype: str
        """
        return self._type_template

    @type_template.setter
    def type_template(self, type_template: str):
        """Sets the type_template of this Template.

        Type of the Template Sample or Data template  # noqa: E501

        :param type_template: The type_template of this Template.
        :type type_template: str
        """
        allowed_values = ["Data", "Sample"]  # noqa: E501
        if type_template not in allowed_values:
            raise ValueError(
                "Invalid value for `type_template` ({0}), must be one of {1}"
                .format(type_template, allowed_values)
            )

        self._type_template = type_template

    @property
    def descriptiopn(self) -> str:
        """Gets the descriptiopn of this Template.

        Description of the template  # noqa: E501

        :return: The descriptiopn of this Template.
        :rtype: str
        """
        return self._descriptiopn

    @descriptiopn.setter
    def descriptiopn(self, descriptiopn: str):
        """Sets the descriptiopn of this Template.

        Description of the template  # noqa: E501

        :param descriptiopn: The descriptiopn of this Template.
        :type descriptiopn: str
        """

        self._descriptiopn = descriptiopn

    @property
    def columns(self) -> List[TemplateColumn]:
        """Gets the columns of this Template.


        :return: The columns of this Template.
        :rtype: List[TemplateColumn]
        """
        return self._columns

    @columns.setter
    def columns(self, columns: List[TemplateColumn]):
        """Sets the columns of this Template.


        :param columns: The columns of this Template.
        :type columns: List[TemplateColumn]
        """

        self._columns = columns
