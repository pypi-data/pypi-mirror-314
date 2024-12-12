import abc


class ResistivityReader(abc.ABC):
    @abc.abstractmethod
    def get_resistivity(self, file_id: int) -> float:
        pass
