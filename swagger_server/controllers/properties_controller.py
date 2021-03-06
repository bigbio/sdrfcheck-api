import os
import pathlib
from collections import defaultdict

import connexion
import six

from models.map_template_column import MapTemplateColumn  # noqa: E501
from models.ontology_term import OntologyTerm  # noqa: E501
from models.post_translational_modification import PostTranslationalModification  # noqa: E501
from models.template import Template  # noqa: E501
from models.template_column import TemplateColumn  # noqa: E501
from swagger_server.models.ontology_term import OntologyTerm

from swagger_server import util
from unimod.unimod import UnimodDatabase
import yaml

from util import get_ontology_text_from_columnname, compare_string

from swagger_server.ols import OlsClient


def find_data_properties(template=None):  # noqa: E501
  """Find properties for rows of the SDRF data files

     # noqa: E501

    :param template: Status values that need to be considered for filter
    :type template: str

    :rtype: List[OntologyTerm]
    """
  return 'do some magic!'


def find_post_translational_modifications(filter=None, page=0, pageSize=100):  # noqa: E501
  """Find values for an specific property, for example possible taxonomy values for Organism property

     # noqa: E501

    :param filter: Keyword to filter the list of possible values
    :type filter: str
    :param page: Number of the page with the possible values for the property
    :type page: int
    :param pageSize: Number of values with the possible values for the property
    :type pageSize: int

    :rtype: List[PostTranslationalModification]
    """

  unimod_database = UnimodDatabase()
  l = unimod_database.search_mods_by_keyword(keyword=filter)
  list_found = l[(page * pageSize):(page * pageSize) + pageSize]
  return list_found

def find_sample_properties(template=None):  # noqa: E501
  """Find properties for rows of the SDRF samples

     # noqa: E501

    :param template: Status values that need to be considered for filter
    :type template: str

    :rtype: List[OntologyTerm]
    """
  return 'do some magic!'


def find_values_by_property(accession, ontology, filter=None, page=None, pageSize=None):  # noqa: E501
  """
  Find values for an specific property, for example possible taxonomy values for Organism property

  # noqa: E501

  :param accession: Accession of the property in the Ontology
  :type accession: str
  :param ontology: Ontology to loockup the property
  :type ontology: str
  :param filter: Keyword to filter the list of possible values
  :type filter: str
  :param page: Number of the page with the possible values for the property
  :type page: int
  :param pageSize: Number of values with the possible values for the property
  :type pageSize: int

  :rtype: List[OntologyTerm]
  """
  client = OlsClient()
  results = client.search(filter, ontology=ontology, childrenOf=[accession])
  terms = []
  if results is not None and len(results) > 0:
    for old_term in results:
      ontologyTerm = OntologyTerm(id = old_term['obo_id'], name = old_term['label'],
                                  ontology = old_term['ontology_prefix'], iri_id=old_term['iri'])
      terms.append(ontologyTerm)
  terms = terms[(page * pageSize):(page * pageSize) + pageSize]
  return terms

def get_properties():  # noqa: E501
  """Get all the posible properties

  :rtype: List[TemplateColumn]
  """
  relevant_path = str(pathlib.Path(__file__).parent) + "/" + "../resources/templates/"
  included_extensions = ['yaml']
  file_names = [fn for fn in os.listdir(relevant_path)
                if any(fn.endswith(ext) for ext in included_extensions)]
  map_columns = []
  columns = {}
  for file_name in file_names:
    with open(relevant_path + os.sep + file_name) as file:
      # The FullLoader parameter handles the conversion from YAML
      # scalar values to Python the dictionary format
      yaml_file = yaml.load(file, Loader=yaml.FullLoader)
      for yaml_column in yaml_file['template']['columns']:
        name = yaml_column
        ontology = yaml_file['template']['columns'][yaml_column]
        type = ontology['type']
        ontology_term = None
        columns[yaml_column] = ontology

  relevant_path = str(pathlib.Path(__file__).parent) + "/" + "../resources/terms/"
  included_extensions = ['yaml']
  file_names = [fn for fn in os.listdir(relevant_path)
                if any(fn.endswith(ext) for ext in included_extensions)]

  for file_name in file_names:
    with open(relevant_path + os.sep + file_name) as file:
      # The FullLoader parameter handles the conversion from YAML
      # scalar values to Python the dictionary format
      yaml_file = yaml.load(file, Loader=yaml.FullLoader)
      for yaml_column in yaml_file['terms']:
        ontology = yaml_file['terms'][yaml_column]
        type = ontology['type']
        columns[yaml_column] = ontology

  for yaml_column in columns:
      ontology = columns[yaml_column]
      ontology_term = None
      if 'ontology_accession' in ontology:
        accession = ontology['ontology_accession']
        cv = ontology['ontology']
        ontology_term = OntologyTerm(id=accession, name=yaml_column, ontology=cv, iri_id=ontology['ols_uri'])
      column = TemplateColumn(name=yaml_column, type_node=ontology['type'], ontology_term=ontology_term, searchable=ontology['searchable'])
      map_columns.append(column)
  return list(set(map_columns))

def get_properties_from_text(sdrf_properties):  # noqa: E501
  """
  Get the templates for Sample metadata and Data files
  # noqa: E501

  :param sdrf_properties: A List of properties from SDRF in plain text
  :type sdrf_properties: List[str]
  :rtype: List[TemplateColumn]
  """

  relevant_path = str(pathlib.Path(__file__).parent) + "/" + "../resources/templates/"
  included_extensions = ['yaml']
  file_names = [fn for fn in os.listdir(relevant_path)
                if any(fn.endswith(ext) for ext in included_extensions)]
  map_columns = []
  columns = {}
  for file_name in file_names:
    with open(relevant_path + os.sep + file_name) as file:
      # The FullLoader parameter handles the conversion from YAML
      # scalar values to Python the dictionary format
      yaml_file = yaml.load(file, Loader=yaml.FullLoader)
      for yaml_column in yaml_file['template']['columns']:
        name = yaml_column
        ontology = yaml_file['template']['columns'][yaml_column]
        type = ontology['type']
        ontology_term = None
        columns[yaml_column] = ontology

  relevant_path = str(pathlib.Path(__file__).parent) + "/" + "../resources/terms/"
  included_extensions = ['yaml']
  file_names = [fn for fn in os.listdir(relevant_path)
                if any(fn.endswith(ext) for ext in included_extensions)]

  for file_name in file_names:
    with open(relevant_path + os.sep + file_name) as file:
      # The FullLoader parameter handles the conversion from YAML
      # scalar values to Python the dictionary format
      yaml_file = yaml.load(file, Loader=yaml.FullLoader)
      for yaml_column in yaml_file['terms']:
        name = yaml_column
        ontology = yaml_file['terms'][yaml_column]
        type = ontology['type']
        ontology_term = None
        columns[yaml_column] = ontology

  process_colums = []
  for ontology_text in sdrf_properties:
    for yaml_column in columns:
      text_key = get_ontology_text_from_columnname(ontology_text)
      if text_key is not None and compare_string(text_key, yaml_column):
        ontology = columns[yaml_column]
        accession = ontology['ontology_accession']
        cv = ontology['ontology']
        ontology_term = OntologyTerm(id = accession, name = yaml_column, ontology = cv, iri_id=ontology['ols_uri'])
        other_terms = []
        type = ontology['type']
        if 'otherSearchTerm' in columns[yaml_column]:
          for old_term in columns[yaml_column]['otherSearchTerm']:
            other_terms.append(OntologyTerm(id = old_term['ontology_accession'], name = old_term['name'], ontology = old_term['ontology'], iri_id=old_term['ols_uri']))
        column = TemplateColumn(name = yaml_column, type_node=type, ontology_term = ontology_term, searchable=ontology['searchable'], other_search_term=other_terms)
        map_columns.append(MapTemplateColumn(ontology_text, column))
        process_colums.append(ontology_text)
        break
      if text_key is None:
        map_columns.append(MapTemplateColumn(ontology_text, TemplateColumn(type_node='None', searchable=False)))
        process_colums.append(ontology_text)
        break
    if ontology_text not in process_colums:
      map_columns.append(MapTemplateColumn(ontology_text, TemplateColumn(type_node='None', searchable=False)))

  return map_columns


def get_templates():  # noqa: E501
  """
  Get the templates for Sample metadata and Data files
  # noqa: E501
  :rtype: List[Template]
  """

  relevant_path = str(pathlib.Path(__file__).parent) + "/" + "../resources/templates/"
  included_extensions = ['yaml']
  file_names = [fn for fn in os.listdir(relevant_path)
                if any(fn.endswith(ext) for ext in included_extensions)]
  templates = []
  for file_name in file_names:
    with open(relevant_path + os.sep + file_name) as file:
      # The FullLoader parameter handles the conversion from YAML
      # scalar values to Python the dictionary format
      yaml_file = yaml.load(file, Loader=yaml.FullLoader)
      columns = []
      for yaml_column in yaml_file['template']['columns']:
        name = yaml_column
        ontology = yaml_file['template']['columns'][yaml_column]
        type = ontology['type']
        ontology_term = None
        if 'ontology_accession' in ontology:
          accession = ontology['ontology_accession']
          cv = ontology['ontology']
          ontology_term = OntologyTerm(id = accession, name = name, ontology = cv, iri_id=ontology['ols_uri'])
        column = TemplateColumn(name = name, type_node=type, ontology_term = ontology_term, searchable = ontology['searchable'])
        columns.append(column)
      template = Template(yaml_file['template']['name'], yaml_file['template']['type'],
                          yaml_file['template']['description'], columns)
      templates.append(template)
  return templates
