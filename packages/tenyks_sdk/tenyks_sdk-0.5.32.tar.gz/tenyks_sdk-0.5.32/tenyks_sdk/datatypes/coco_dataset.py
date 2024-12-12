from typing import Any, Dict, List, Optional, TypedDict


class CocoImage(TypedDict):
    id: int
    file_name: str
    width: int
    height: int
    license: Optional[int] = None
    flickr_url: Optional[str] = None
    coco_url: Optional[str] = None
    date_captured: Optional[str] = None


class CocoAnnotation(TypedDict):
    id: int
    image_id: int
    category_id: int
    segmentation: List[Any]
    area: float
    bbox: List[float]
    iscrowd: int


class CocoCategory(TypedDict):
    id: int
    name: str
    supercategory: Optional[str] = None


class CocoDataset(TypedDict):
    images: List[CocoImage]
    annotations: List[CocoAnnotation]
    categories: List[CocoCategory]
    info: Optional[Dict[str, Any]] = None
    licenses: Optional[List[Dict[str, Any]]] = None
