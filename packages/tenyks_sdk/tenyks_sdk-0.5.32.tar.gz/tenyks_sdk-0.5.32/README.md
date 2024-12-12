<a href="https://www.tenyks.ai/">
    <img src="https://assets-global.website-files.com/63a0220866f41638081f4fce/64ef648b87b00109b3260832_Tenyks_Logo_transparent-p-500.webp" alt="Tenyks logo" title="Tenyks" align="right" height="60" />
</a>

# Tenyks SDK

**Tenyks SDK** is Python toolkit which allows for integration and extensibility to the [Tenyks platform](https://www.tenyks.ai/).

You can use **Tenyks SDK** to:
* develop custom Data Quality Checks (DQC) to run on your datasets
* develop custom Model Metrics to assess your models' performance

## Quickstart to create DQcs or metrics for a user/customer:

This is the repo you're looking for: [https://github.com/tenyks-ai/sdk-customer-template](https://github.com/tenyks-ai/sdk-customer-template).

## Custom DQCs

A Data Quality Check is a check that is performed on a dataset or a subset of the dataset using images/annotations/embeddings. Each DQC can detect one or more subsets of the dataset that have a specific problem with a specific severity. The idea is to have many DQCs, each of which identifies a particular problem/feature so as to have a suite that the user can execute. 

There are already a number of implemented DQCs in the Tenyks platform, but via the SDK it is possible to create new, completely customised DQCs according to the specific requirements of your use case. You can then add your custom DQCs to the platform and they will run together with the default DQCs. It is possible to run the DQCs locally to test their operation.

### DQC Interface

Every custom DQC must implement (it is a subclass of) the `DataQualityCheck` interface:

```python
class DataQualityCheck(ABC):
    @classmethod
    @abstractmethod
    def create(cls, dqc_input: DQCInput) -> "DataQualityCheck":
        pass

    @classmethod
    @abstractmethod
    def get_check_type(cls):
        raise NotImplementedError()

    @abstractmethod
    def get_version(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_description(self) -> str:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_display_name(cls) -> str:
        return NotImplementedError()

    @classmethod
    @abstractmethod
    def get_dependencies(cls) -> List[DqcDependency]:
        return NotImplementedError()

    @classmethod
    @abstractmethod
    def runs_on(cls) -> DqcRunsOn:
        return NotImplementedError()

    @abstractmethod
    def perform_check(self) -> List[DQCIndividualCheckResult]:
        raise NotImplementedError()
```
### DQC Registry

To run a suite of custom DQCs there needs to be a mapping between the type/name of the check and the class which implements it. This allows the DQC runner to access the registry and know where to find the classes of the checks. The registry has the following format:

```python
from .checks.custom_dqc_one import CustomDqcOne
from .checks.custom_dqc_two import CustomDqcTwo
from .checks.custom_dqc_three import CustomDqcThree

dqc_registry = {
    CustomDqcOne.__CHECK_TYPE: CustomDqcOne,
    CustomDqcTwo.__CHECK_TYPE: CustomDqcTwo,
    CustomDqcThree.__CHECK_TYPE: CustomDqcThree,
    # Additional custom DQCs can be added here.
}

```

### Folder structure

This is how the folder for your custom DQCs should be structured:

```
custom_dqcs
├── checks
│   ├── custom_dqc_one.py
│   ├── custom_dqc_two.py
│   ├── custom_dqc_three.py
│   ├── __init__.py
├── run_local (optional, to run DQCs locally)
├── controller.py
├── dqc_registry.py
└── __init__.py
```

The `examples/custom_dqcs` folder provides a complete example, it is highly recommended to start from there. You can (in a separate branch or fork) modify its contents to suit your needs.

### DQC Input

You need to specify the location of the input parameters, the location of the file where the results of the checks execution will be saved, and the list of checks to be executed.
As you can see in `examples/custom_dqcs/run_local/input_template.json`, this is a possible input format for the DQCs suite:

```python
{
    "job_id": "job_1" # This is relevant only for non-local execution, locally any string works
    "coco_location": {
        "s3_uri": "s3://tenyks-dev-storage/andrea/kitti_5/metadata/annotations.json",
        "type": "aws_s3",
        "credentials": {
            "aws_access_key_id": "***",
            "aws_secret_access_key": "***",
            "region_name": "***",
        },
    },
    "output_location": {
        "s3_uri": "s3://tenyks-dev-storage/andrea/kitti_5/metadata/custom_dqc_output.json",
        "type": "aws_s3",
        "credentials": {
            "aws_access_key_id": "***",
            "aws_secret_access_key": "***",
            "region_name": "***",
        },
    },
    "check_types": ["dqcOne", "dqcTwo", "dqcThree"],  # subset of the check keys in the dqc_registry
}
```

## Custom Metrics

A Model Metric is a performance metric that is calculated comparing the predictions of a model with the ground truth annotations.

There are already some metrics implemented in the Tenyks platform, but via the SDK it is possible to create new, completely customised metrics according to the specific requirements of your use case. You can then add your custom metrics to the platform in order to run them on the dataset and models uploaded there. It is possible to run the metrics locally to test them.

### Metric Interface

Every custom Model Metric must implement (it is a subclass of) the `ModelMetric` interface:

```python
class ModelMetric(ABC):

    @classmethod
    @abstractmethod
    def create(
        cls,
        model_metric_input: ModelMetricInput,
    ) -> "ModelMetric":
        pass

    @classmethod
    @abstractmethod
    def get_metric_name(cls):
        raise NotImplementedError()

    @abstractmethod
    def run_metric(self) -> List[Dict]:
        raise NotImplementedError()

```
### Metrics Registry

To run custom Metrcs there needs to be a mapping between the type/name of the metric and the class which implements it. This allows the Metrics runner to access the registry and know where to find the classes of the checks. The registry has the following format:

```python
from .metrics.custom_metric_one import CustomMetricOne
from .metrics.custom_metric_two import CustomMetricTwo
from .metrics.custom_metric_three import CustomMetricThree

dqc_registry = {
    CustomMetricOne._METRIC_NAME: CustomMetricOne,
    CustomMetricTwo._METRIC_NAME: CustomMetricTwo,
    CustomMetricThree._METRIC_NAME: CustomMetricThree,
    # Additional custom metrics can be added here.
}

```

### Folder structure

This is how the folder for your custom metrics should be structured:

```
custom_metrics
├── metrics
│   ├── custom_metric_one.py
│   ├── custom_metric_two.py
│   ├── custom_metric_three.py
│   ├── __init__.py
├── run_local (optional, to run metrics locally)
├── controller.py
├── model_metrics_registry.py
└── __init__.py
```

The `examples/custom_metrics` folder provides a complete example, it is highly recommended to start from there. You can (in a separate branch or fork) modify its contents to suit your needs.

### Metric Input

You need to specify the location of the input parameters, the location of the file where the results of the metrics execution will be saved, and the name of the metric to be executed.
As you can see in `examples/custom_metrics/run_local/input_template.json`, this is a possible input format:

```python
{
    "task_id": "job_1", # This is relevant only for non-local execution, locally any string works
    "metric_name": "cocoeval_metric",
    "task_type": "segm",
    "iou_thresholds": [ 0.5],
    "dataset_categories_file_location": {
        "type": "aws_s3",
        "s3_uri": "s3://tenyks-dev-storage/tenyks/kitti_200_segmentation/metadata/model_metrics/map_mar_v1/3bbaa478-9b69-4922-bd56-01fcb770329f/dataset_categories.json",
        "credentials": {
            "aws_access_key_id": "***",
            "aws_secret_access_key": "***",
            "region_name": "***",
        },
    },
    "model_folder_locations": [
        {
            "model_key": "my_model",
            "output_location": {
                "type": "aws_s3",
                "s3_uri": "s3://tenyks-dev-storage/tenyks/kitti_200_segmentation/metadata/model_metrics/map_mar_v1/3bbaa478-9b69-4922-bd56-01fcb770329f/my_model/",
                "credentials": {
                    "aws_access_key_id": "***",
                    "aws_secret_access_key": "***",
                    "region_name": "***",
                },
            },
        },
    ],
    "metrics_results_file_location": {
        "type": "aws_s3",
        "s3_uri": "s3://tenyks-dev-storage/tenyks/kitti_200_segmentation/metadata/model_metrics/map_mar_v1/3bbaa478-9b69-4922-bd56-01fcb770329f/metric_result_from_local_sdk.json",
        "credentials": {
            "aws_access_key_id": "***",
            "aws_secret_access_key": "***",
            "region_name": "***",
        },
    },
}
```