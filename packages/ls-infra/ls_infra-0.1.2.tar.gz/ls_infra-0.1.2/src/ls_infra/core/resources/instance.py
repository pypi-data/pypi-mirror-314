from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class ResourceInstance:
    """
    Generic representation of an infrastructure resource.
    All fields are optional to accommodate different provider capabilities.

    Attributes:
        provider: Cloud provider name (aws, gcp, azure, etc.)
        account_id: Cloud provider account identifier
        identity: Credential identity used to access the account
        instance_id: Provider's unique identifier for the instance
        name: Instance name/label
        region: Region where the instance is deployed
        zone: Availability zone where the instance is deployed
        tags: Instance tags/labels
        primary_public_ip: Main public IP address
        private_public_ip: Main private IP address
        state: Current instance state (running, stopped, etc.)
        metadata: Additional provider-specific information (raw_data converted to dict)
        raw_data: Original response data from the provider
    """

    provider: Optional[str] = None
    account_id: Optional[str] = None
    identity: Optional[str] = None
    instance_id: Optional[str] = None
    name: Optional[str] = None
    region: Optional[str] = None
    zone: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    primary_public_ip: Optional[str] = None
    private_public_ip: Optional[str] = None
    state: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    raw_data: Optional[Any] = None

    @property
    def unique_id(self) -> str:
        """
        Generate a unique identifier for the resource.
        Uses account_id and/or identity if available.
        """
        account_info = []
        if self.account_id:
            account_info.append(self.account_id)
        if self.identity:
            account_info.append(self.identity)

        account_part = ":".join(account_info) if account_info else "default"
        parts = [
            self.provider or "unknown",
            account_part,
            self.region or "unknown",
            self.instance_id or "unknown",
        ]
        return ":".join(parts)
