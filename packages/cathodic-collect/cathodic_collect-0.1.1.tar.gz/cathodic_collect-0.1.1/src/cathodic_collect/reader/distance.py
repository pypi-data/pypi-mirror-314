import abc


class DistanceReader(abc.ABC):
    @abc.abstractmethod
    def get_distance(self, file_id: int) -> float:
        pass
