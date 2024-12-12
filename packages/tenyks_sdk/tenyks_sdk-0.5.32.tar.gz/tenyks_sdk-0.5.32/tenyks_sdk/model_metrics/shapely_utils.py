from typing import Dict, List, Tuple

from tenyks_sdk.utils.tenyks_internal_export import (
    TenyksBoundingBox,
    TenyksBoundingBoxMatch,
    TenyksImage,
)


class ShapelyUtils:
    def get_shapely_annotations_and_predictions(
        self,
        tenyks_images: List[TenyksImage],
    ) -> Tuple[Dict, Dict]:
        """
        Dictionary of: {
            image_key: {
                category_id: [list of polygons]
            }
        }
        """
        shapely_annotations, shapely_predictions = dict(), dict()

        for tenyks_image in tenyks_images:
            image_key = tenyks_image.image_key
            bounding_box_matches = tenyks_image.bounding_box_matches

            shapely_annotations, shapely_predictions = (
                self.__combine_matches_per_image_and_class(
                    shapely_annotations,
                    shapely_predictions,
                    bounding_box_matches,
                    image_key,
                )
            )

        return shapely_annotations, shapely_predictions

    def __combine_matches_per_image_and_class(
        self,
        shapely_annotations: Dict,
        shapely_predictions: Dict,
        bounding_box_matches: List[TenyksBoundingBoxMatch],
        image_key: str,
    ) -> Tuple[Dict, Dict]:
        shapely_annotations[image_key] = dict()
        shapely_predictions[image_key] = dict()
        for match in bounding_box_matches:
            annotation = match.annotation
            prediction = match.prediction

            shapely_annotations = self.__fill_shapely_annotations_per_match(
                annotation, shapely_annotations, image_key
            )
            shapely_predictions = self.__fill_shapely_annotations_per_match(
                prediction, shapely_predictions, image_key
            )

            return shapely_annotations, shapely_predictions

    def __fill_shapely_annotations_per_match(
        self, annotation: TenyksBoundingBox, shapely_annotations: Dict, image_key: str
    ) -> Dict:
        if annotation.id is not None and getattr(annotation, "segmentation", []):
            category_id = annotation.category_id
            segmentation = annotation.segmentation

            if category_id not in shapely_annotations[image_key]:
                shapely_annotations[image_key][category_id] = []

            shapely_annotations[image_key][category_id].extend(segmentation)

        return shapely_annotations
