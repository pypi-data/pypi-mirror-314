from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List


class BaseCollector(ABC):
    """
    Base class for all collectors in ls-infra.

    All collectors must implement:
    - fetch_raw_data: Retrieves raw data from the provider
    - serialize: Transforms the raw data into the standardized format
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the collector with configuration.

        Args:
            config: Dictionary containing collector-specific configuration
        """
        self.config = config
        self.raw_data: Any = None
        self.serialized_data: List[Dict[str, Any]] = []

    @abstractmethod
    async def fetch_raw_data(self) -> Any:
        """
        Fetch raw data from the cloud provider.
        Must be implemented by each collector.

        Returns:
            Raw data from the provider in any format
        """
        pass

    @abstractmethod
    async def serialize(self, raw_data: Any):  # -> List[Dict[str, Any]]: ## mypy issue
        """
        Transform raw data into the standardized format required by formatters.
        Must be implemented by each collector.

        Args:
            raw_data: The raw data returned by fetch_raw_data

        Returns:
            List of dictionaries in the standardized format
        """
        pass

    async def collect(self) -> List[Dict[str, Any]]:
        """
        Main method to execute the collection process.
        Handles the full collection workflow.

        Returns:
            List of dictionaries containing the standardized data
        """
        try:
            self.raw_data = await self.fetch_raw_data()
            self.serialized_data = await self.serialize(self.raw_data)
            return self.serialized_data
        except Exception as e:
            raise CollectorError(f"Collection failed: {str(e)}") from e


class CollectorError(Exception):
    """Custom exception for collector-related errors"""

    pass
