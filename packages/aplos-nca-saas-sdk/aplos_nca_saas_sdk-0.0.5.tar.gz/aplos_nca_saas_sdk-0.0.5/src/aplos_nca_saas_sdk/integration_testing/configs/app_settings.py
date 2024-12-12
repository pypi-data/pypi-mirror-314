"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Dict, Any
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase


class ApplicationDomain(ConfigBase):
    """
    Application Domain: Defines the domains that the application configuration tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__domain: str | None = None

    @property
    def domain(self) -> str:
        """The domain to validate"""
        if self.__domain is None:
            raise RuntimeError("Domain is not set")
        return self.__domain

    @domain.setter
    def domain(self, value: str):
        self.__domain = value


class ApplicationSettings:
    """
    Application Settings: Defines the domains that the application settings (configuration endpoint) tests will check against

    """

    def __init__(self):
        self.__domains: List[ApplicationDomain] = []

    @property
    def domains(self) -> List[ApplicationDomain]:
        return self.__domains

    @domains.setter
    def domains(self, value: List[ApplicationDomain]):
        self.__domains = value

    def load(self, test_config: Dict[str, Any]):
        """Load the domains from the config"""
        domains: List[Dict[str, Any]] = test_config.get("domains", [])

        domain: Dict[str, Any]
        for domain in domains:
            app_domain = ApplicationDomain()
            app_domain.domain = domain.get("domain", None)
            app_domain.enabled = bool(domain.get("enabled", True))

            self.__domains.append(app_domain)
