from abc import ABC, abstractmethod


class CollectionInterface(ABC):
    @abstractmethod
    def create_collection(self):
        pass

    @abstractmethod
    def delete_collection(self):
        pass

    @abstractmethod
    def display_collection(self):
        pass

    @abstractmethod
    def add_log(self):
        pass

    @abstractmethod
    def delete_log(self):
        pass
