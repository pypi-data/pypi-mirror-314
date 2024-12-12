from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from dataclasses import field
from itertools import chain
from typing import List
from uuid import UUID

from kleinkram.api.client import AuthenticatedClient
from kleinkram.api.routes import _get_files_by_mission
from kleinkram.api.routes import _get_missions_by_project
from kleinkram.api.routes import _get_projects
from kleinkram.errors import InvalidMissionSpec
from kleinkram.errors import InvalidProjectSpec
from kleinkram.models import File
from kleinkram.models import Mission
from kleinkram.models import Project
from kleinkram.utils import filtered_by_patterns

MAX_PARALLEL_REQUESTS = 32
SPECIAL_PATTERN_CHARS = ["*", "?", "[", "]"]


@dataclass
class ProjectSpec:
    patterns: List[str] = field(default_factory=list)
    ids: List[UUID] = field(default_factory=list)


@dataclass
class MissionSpec:
    patterns: List[str] = field(default_factory=list)
    ids: List[UUID] = field(default_factory=list)
    project_spec: ProjectSpec = field(default=ProjectSpec())


@dataclass
class FileSpec:
    patterns: List[str] = field(default_factory=list)
    ids: List[UUID] = field(default_factory=list)
    mission_spec: MissionSpec = field(default=MissionSpec())


def check_mission_spec_is_creatable(spec: MissionSpec) -> None:
    if not mission_spec_is_unique(spec):
        raise InvalidMissionSpec(f"Mission spec is not unique: {spec}")
    # cant create a missing by id
    if spec.ids:
        raise InvalidMissionSpec(f"cant create mission by id: {spec}")


def check_project_spec_is_creatable(spec: ProjectSpec) -> None:
    if not project_spec_is_unique(spec):
        raise InvalidProjectSpec(f"Project spec is not unique: {spec}")
    # cant create a missing by id
    if spec.ids:
        raise InvalidProjectSpec(f"cant create project by id: {spec}")


def _pattern_is_unique(pattern: str) -> bool:
    for char in SPECIAL_PATTERN_CHARS:
        if char in pattern:
            return False
    return True


def project_spec_is_unique(spec: ProjectSpec) -> bool:
    # a single project id is specified
    if len(spec.ids) == 1 and not spec.patterns:
        return True

    # a single project name is specified
    if len(spec.patterns) == 1 and _pattern_is_unique(spec.patterns[0]):
        return True
    return False


def mission_spec_is_unique(spec: MissionSpec) -> bool:
    # a single mission id is specified
    if len(spec.ids) == 1 and not spec.patterns:
        return True

    # a single mission name a unique project spec are specified
    if (
        project_spec_is_unique(spec.project_spec)
        and len(spec.patterns) == 1
        and _pattern_is_unique(spec.patterns[0])
    ):
        return True
    return False


def get_projects_by_spec(
    client: AuthenticatedClient, spec: ProjectSpec
) -> List[Project]:
    projects = _get_projects(client)

    matched_names = filtered_by_patterns(
        [project.name for project in projects], spec.patterns
    )

    if not spec.patterns and not spec.ids:
        return projects

    return [
        project
        for project in projects
        if project.name in matched_names or project.id in spec.ids
    ]


def get_missions_by_spec(
    client: AuthenticatedClient, spec: MissionSpec
) -> List[Mission]:
    projects = get_projects_by_spec(client, spec.project_spec)

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_REQUESTS) as executor:
        missions = chain.from_iterable(
            executor.map(
                lambda project: _get_missions_by_project(client, project), projects
            )
        )

    missions = list(missions)

    if not spec.patterns and not spec.ids:
        return list(missions)

    matched_names = filtered_by_patterns(
        [mission.name for mission in missions], spec.patterns
    )

    filter = [
        mission
        for mission in missions
        if mission.name in matched_names or mission.id in spec.patterns
    ]

    return filter


def get_files_by_spec(client: AuthenticatedClient, spec: FileSpec) -> List[File]:
    missions = get_missions_by_spec(client, spec.mission_spec)

    # collect files
    with ThreadPoolExecutor(max_workers=MAX_PARALLEL_REQUESTS) as executor:
        files = chain.from_iterable(
            executor.map(
                lambda mission: _get_files_by_mission(client, mission), missions
            )
        )

    if not spec.patterns and not spec.ids:
        return list(files)
    matched_names = filtered_by_patterns([file.name for file in files], spec.patterns)

    return [file for file in files if file.name in matched_names or file.id in spec.ids]
