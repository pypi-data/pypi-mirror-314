from .base import BaseFormatter
from isahitlab.helpers.points import normalize_points, points_to_vertices, corners_to_bbox
from isahitlab.helpers.labels import find_label_in_main_list
from typing import List, Dict, Union
from isahitlab.domain.task import TaskPayload
from isahitlab.domain.project import ProjectType
import logging


logger = logging.getLogger(__name__)

class KiliToLabFormatter(BaseFormatter):
    """Formatter used to ensure retrocompatibilty with kili"""

    project_configuration: Dict
    is_sequence: bool = False
    project_type: ProjectType = None

    def __init__(self,project_configuration : Dict) -> None :
        self.project_configuration = project_configuration
        
        self.is_sequence = project_configuration.get("metadata", {}).get("toolOptions", {}).get("sequence", False)
        self.project_type = project_configuration['projectType']

        if self.project_type == "form":
            raise Exception("Kili compatibiliy is not supported for form project")

        if self.is_sequence:
            raise Exception("Kili compatibiliy is not supported for sequence project")


    def format_tasks(self, tasks: List[TaskPayload]) -> List[Dict]:

        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append(TaskPayload(
                task.name, 
                task.resources, 
                self._format_data(task.data)
                ))
        
        return formatted_tasks


    def _format_data(self, data : Dict) -> Dict:
        formatted_data = {
            "annotations": []
        }

        annotations = data["OBJECT_DETECTION_JOB"]["annotations"]
        resolution = data.get("resolution", None)

        for annotation in annotations:
            formatted_data["annotations"].append(self._format_annotation(annotation, resolution))


        return formatted_data

    def _format_annotation(self, annotation : Dict, resolution : Union[Dict, None]) -> Dict:

        formatted = {
            "polygons": [],
            "labels" : {}
        }

        bounding_polys = annotation["boundingPoly"]

        for bounding_poly in bounding_polys:
            if self.project_type == 'iat-rectangle':
                formatted["polygons"].append(self._format_bounding_poly_for_rectangle(bounding_poly, resolution))
            else:
                formatted["polygons"].append(self._format_bounding_poly_for_polygon(bounding_poly, resolution))

        if "categories" in annotation and len(annotation["categories"]) > 0:
            label_id = annotation["categories"][0]["name"]
            if label_id:
                matching = find_label_in_main_list(label_id, self.project_configuration)
                if not matching:
                    raise Exception("No label found for category \"{}\"".format(label_id))
                formatted["labels"] = matching

        if "children" in annotation:
            logger.warning("Mapping of \"children\" is not supported")

        return formatted
    
    def _format_bounding_poly_for_rectangle(self, bounding_poly : Dict, resolution : Union[Dict, None]) -> Dict:
        if "normalizedVertices" in bounding_poly:
            vertices = corners_to_bbox(points_to_vertices(bounding_poly["normalizedVertices"]))
        elif "vertices" in bounding_poly:
            if not resolution:
                raise Exception("Resolution (width, height) is required to normalize vertices. You can also directly provide \"normalizedVertices\" instead of \"vertices\".")
            vertices = corners_to_bbox(points_to_vertices(normalize_points(bounding_poly["vertices"])))

        return {
            "geometry": {
                "vertices": vertices,
                "type": "rectangle"
            }
        }
    
    def _format_bounding_poly_for_polygon(self, bounding_poly : Dict, resolution : Union[Dict, None]) -> Dict:
        if "normalizedVertices" in bounding_poly:
            vertices = points_to_vertices(bounding_poly["normalizedVertices"])
        elif "vertices" in bounding_poly:
            if not resolution:
                raise Exception("Resolution (width, height) is required to normalize vertices. You can also directly provide \"normalizedVertices\" instead of \"vertices\".")
            vertices = points_to_vertices(normalize_points(bounding_poly["vertices"]))

        return {
            "geometry": {
                "vertices": vertices,
                "type": "polygon"
            }
        }
