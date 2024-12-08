from typing import Any, Dict
from typing_extensions import override
from masterpiece import MasterPiece


class JDatabase(MasterPiece):
    """The base class for data storage classes.Serves as an abstract interface for managing
    interactions with various types of databases. Designed to support multiple backend databases,
    this class provides a unified API for writing sensor data and other parameters, ensuring that the
    system can seamlessly integrate with different storage solutions.
    """

    token: str = ""
    org: str = "juham"
    host: str = ""
    database = "home"

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def write(self, point: Any) -> None:
        """Write record to database table.

        @param point point to be written
        """
        raise Exception("write not implemented")

    def write_point(self, name : str, tags : dict[str, Any], fields : Dict[str, Any], ts : str) ->None:
        """Write record to the database table.

        Args:
            name (str): name of the measurement
            tags (dict[str, Any]): tags (indexed keys)
            fields (dict[str, Any]) measurement data
            ts (str) time stamp

        Returns:
            None

        """
        raise Exception("write not implemented")


    def read(self, point: Any) -> None:
        raise Exception("read not implemented")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_database"] = {}
        attributes = ["host", "org", "database", "token"]
        for attr in attributes:
            if getattr(self, attr) != getattr(type(self), attr):
                data["_base"][attr] = getattr(self, attr)
        return data

    @override
    def from_dict(self, data_dict: Dict[str, Any]) -> None:
        super().from_dict(data_dict)
        for key, value in data_dict["_database"].items():
            setattr(self, key, value)
