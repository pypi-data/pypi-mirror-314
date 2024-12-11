from enum import Enum


class ArtifactType(str, Enum):
    ''' ____WARNING____'''
    '''Please note that changing this strings can effect visualization of
      results in the reports because we query artifact table base on those and
      they kept in the artifacts table in the subtype attribute as strings '''

    REPORT_DESCRIPTION = "report_description"
    SCAN_GRAPH = "scan_graph"
