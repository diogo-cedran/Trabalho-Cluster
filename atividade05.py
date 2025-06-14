from typing import Dict, List, Union, Any
from abc import ABC, abstractmethod
import numpy as np
from dataclasses import dataclass
from enum import Enum

class DataType(Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"

@dataclass
class DataPoint:
    values: List[Union[float, str]]
    data_types: List[DataType]
    cluster_id: int = -1
    is_centroid: bool = False

class DataConverter(ABC):
    @abstractmethod
    def convert(self, value: Any) -> float:
        pass

class CategoricalConverter(DataConverter):
    def __init__(self):
        self._mapping: Dict[str, float] = {}
        self._reverse_mapping: Dict[float, str] = {}
        self._next_value = 0.0

    def convert(self, value: str) -> float:
        if value not in self._mapping:
            self._mapping[value] = self._next_value
            self._reverse_mapping[self._next_value] = value
            self._next_value += 1.0
        return self._mapping[value]

    def reverse_convert(self, value: float) -> str:
        return self._reverse_mapping.get(value, "Unknown")

class NumericalConverter(DataConverter):
    def convert(self, value: Union[int, float]) -> float:
        return float(value)

class DataStructure:
    def __init__(self):
        self._data_points: List[DataPoint] = []
        self._converters: Dict[int, DataConverter] = {}
        self._clusters: Dict[int, List[DataPoint]] = {}

    def add_data_point(self, values: List[Union[float, str]], data_types: List[DataType]) -> None:
        if len(values) != len(data_types):
            raise ValueError("Number of values must match number of data types")

        for i, data_type in enumerate(data_types):
            if i not in self._converters:
                if data_type == DataType.CATEGORICAL:
                    self._converters[i] = CategoricalConverter()
                else:
                    self._converters[i] = NumericalConverter()

        converted_values = [
            self._converters[i].convert(value)
            for i, value in enumerate(values)
        ]

        data_point = DataPoint(
            values=values,
            data_types=data_types,
            cluster_id=-1,
            is_centroid=False
        )
        
        self._data_points.append(data_point)
        self._assign_to_cluster(data_point)

    def _assign_to_cluster(self, data_point: DataPoint) -> None:
        if not self._clusters:
            data_point.cluster_id = 0
            data_point.is_centroid = True
            self._clusters[0] = [data_point]
            return

        converted_point = [
            self._converters[i].convert(value)
            for i, value in enumerate(data_point.values)
        ]

        min_distance = float('inf')
        nearest_cluster = None

        for cluster_id, cluster_points in self._clusters.items():
            centroid = self._calculate_centroid(cluster_points)
            distance = self._calculate_euclidean_distance(converted_point, centroid)
            
            if distance < min_distance:
                min_distance = distance
                nearest_cluster = cluster_id

        data_point.cluster_id = nearest_cluster
        self._clusters[nearest_cluster].append(data_point)

    def _calculate_centroid(self, points: List[DataPoint]) -> List[float]:
        if not points:
            return []

        converted_points = [
            [self._converters[i].convert(point.values[i]) for i in range(len(point.values))]
            for point in points
        ]
        
        return np.mean(converted_points, axis=0).tolist()

    def _calculate_euclidean_distance(self, point1: List[float], point2: List[float]) -> float:
        return np.sqrt(np.sum((np.array(point1) - np.array(point2)) ** 2))

    def get_converted_values(self, data_point: DataPoint) -> List[float]:
        return [
            self._converters[i].convert(value)
            for i, value in enumerate(data_point.values)
        ]

    def get_original_values(self, data_point: DataPoint) -> List[Union[float, str]]:
        return data_point.values

if __name__ == "__main__":
    ds = DataStructure()

    ds.add_data_point(
        values=["red", 1.5, "small"],
        data_types=[DataType.CATEGORICAL, DataType.NUMERICAL, DataType.CATEGORICAL]
    )

    ds.add_data_point(
        values=["blue", 2.0, "medium"],
        data_types=[DataType.CATEGORICAL, DataType.NUMERICAL, DataType.CATEGORICAL]
    )

    ds.add_data_point(
        values=["red", 1.8, "large"],
        data_types=[DataType.CATEGORICAL, DataType.NUMERICAL, DataType.CATEGORICAL]
    )

    first_point = ds._data_points[0]
    print("Valores originais:", ds.get_original_values(first_point))
    print("Valores convertidos:", ds.get_converted_values(first_point))
