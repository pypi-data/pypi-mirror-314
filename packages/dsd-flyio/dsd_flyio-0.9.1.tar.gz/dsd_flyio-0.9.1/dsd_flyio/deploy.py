"""Manages all Fly.io-specific aspects of the deployment process.

Notes:
- Internal references to Fly.io will almost always be flyio. Public references, may be fly_io.
- self.deployed_project_name and self.app_name are identical. The first is used in the
  simple_deploy CLI, but Fly refers to "apps" in their docs. This redundancy makes it
  easier to code Fly CLI commands.
"""

import simple_deploy

from dsd_flyio.platform_deployer import PlatformDeployer
from . import deploy_messages as platform_msgs


@simple_deploy.hookimpl
def simple_deploy_automate_all_supported():
    """Specify whether --automate-all is supported on the specified platform."""
    return True


@simple_deploy.hookimpl
def simple_deploy_get_automate_all_msg():
    """Get platform-specific confirmation message for --automate-all flag."""
    return platform_msgs.confirm_automate_all


@simple_deploy.hookimpl
def simple_deploy_get_platform_name():
    """Return the name of the platform that's being deployed to.

    DEV: Consider returning a config object if there ends up being more info to share
    back to core.
    """
    return "fly_io"


@simple_deploy.hookimpl
def simple_deploy_deploy():
    """Carry out platform-specific deployment steps."""
    platform_deployer = PlatformDeployer()
    platform_deployer.deploy()
