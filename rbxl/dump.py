import os
from typing import Dict, Optional

from roblox_studio.branches import RobloxBranch
from roblox_studio.deployments import DeploymentClient, DeploymentType, OperatingSystem
from roblox_studio.dump import APIDump, APIDumpClass, ClassMemberProperty


class IndexedAPIDump:
    def __init__(self, dump: APIDump):
        self._dump: APIDump = dump
        self._sorted: bool = False
        self._class_by_class_name: Dict[str, APIDumpClass] = {}
        self._class_properties_by_property_name: Dict[str, Dict[str, ClassMemberProperty]] = {}

    def sort(self):
        assert not self._sorted, "Already sorted"
        self._sorted = True

        for dump_class in self._dump.classes:
            properties_index = {}
            self._class_by_class_name[dump_class.name] = dump_class

            for class_member in dump_class.members:
                if class_member.member_type == "Property":
                    properties_index[class_member.name] = class_member

            self._class_properties_by_property_name[dump_class.name] = properties_index

    @property
    def dump(self):
        return self._dump

    @property
    def sorted(self):
        return self._sorted

    def get_class_by_name(self, name: str) -> Optional[APIDumpClass]:
        assert self._sorted
        return self._class_by_class_name.get(name)

    def get_class_properties_by_name(self, name: str) -> Optional[Dict[str, ClassMemberProperty]]:
        assert self._sorted
        return self._class_properties_by_property_name.get(name)


async def fetch_dump(
        branch: Optional[RobloxBranch] = None,
        operating_system: Optional[OperatingSystem] = None,
        deployment_type: Optional[DeploymentType] = None
):
    if branch is None:
        branch = RobloxBranch.production
    if operating_system is None:
        if os.name == "nt":
            operating_system = OperatingSystem.windows
        elif os.name == "posix":
            operating_system = OperatingSystem.mac,
        else:
            raise NotImplementedError("Unknown operating system. To silence, pass the \"operating_system\" kwarg.")

    if deployment_type is None:
        if operating_system == OperatingSystem.mac:
            deployment_type = DeploymentType.studio_64
        else:
            deployment_type = DeploymentType.studio

    async with DeploymentClient() as deployment_client:
        deployment_history = await deployment_client.get_deployments(
            branch=branch,
            operating_system=operating_system
        )
        deployment = deployment_history.get_latest_deployment(
            deployment_type=deployment_type
        )

        dump = await deployment.get_api_dump()
        sorted_dump = IndexedAPIDump(dump)
        sorted_dump.sort()

        return sorted_dump
