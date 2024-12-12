"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import os
from pathlib import Path
from aplos_nca_saas_sdk.utilities.environment_services import EnvironmentServices
from aplos_nca_saas_sdk.integration_testing.integration_test_suite import (
    IntegrationTestSuite,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_configurations import (
    TestConfiguration,
)


def main():
    """Run the tests"""

    evs: EnvironmentServices = EnvironmentServices()
    env_file = os.getenv("ENV_FILE")
    if env_file:
        # if we have an environment file defined, let's load it
        evs.load_environment(starting_path=__file__, file_name=env_file)

    its: IntegrationTestSuite = IntegrationTestSuite()
    config: TestConfiguration = TestConfiguration()

    # normally we'd pull a test configuration file from Secrets Manager, Parameter Store, or some other secure location
    # here we're going to pull the sample file and then override some it's values.
    config_file = os.path.join(Path(__file__).parent, "configs", "config_sample.json")
    # load it so we can see what it looks like
    config.load(file_path=config_file)

    # override the configuration
    override_config(config)

    its.test(test_config=config)


def override_config(config: TestConfiguration):
    """Override the configuration for the tests"""
    username = os.getenv("TEST_USERNAME")
    password = os.getenv("TEST_PASSWORD")
    domain = os.getenv("TEST_DOMAIN")

    if not username or not password or not domain:
        raise RuntimeError(
            "TEST_USERNAME, TEST_PASSWORD, and TEST_DOMAIN must be set in the environment"
        )

    config.logins.list.clear()
    config.logins.add(username=username, password=password, domain=domain)

    config.app_config.domains.clear()
    config.app_config.domains.append(domain)


if __name__ == "__main__":
    main()
