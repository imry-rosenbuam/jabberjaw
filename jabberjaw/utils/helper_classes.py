from abc import ABC,abstractclassmethod,abstractmethod

class Serializable(ABC):
    
    @abstractmethod
    def Serialize(self) -> dict:
        """
        the fucntion serializes the object such that it can be streamed 
        Returns:
            dict: a dictionary that contains all the data needed to deserialize the object
        """
        pass
    
    @abstractclassmethod
    def DeSerializer(cls, data: dict):
        """the function takes a serialized object and deserialize it to a python object

        Args:
            data (dict): serialized object data
        """
        pass


if __name__ == "__main__":
    
    print("Le Fin")