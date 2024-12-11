from __future__ import annotations

from digitalhub.entities.task._base.models import CorePort, CoreServiceType
from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction
from pydantic import Field


class TaskSpecContainerServe(TaskSpecFunction):
    """
    TaskSpecContainerServe specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list[dict] | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        runtime_class: str | None = None,
        priority_class: str | None = None,
        replicas: int | None = None,
        service_ports: list | None = None,
        service_type: str | None = None,
        run_as_user: int | None = None,
        fs_group: int | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            runtime_class,
            priority_class,
            **kwargs,
        )
        self.replicas = replicas
        self.service_ports = service_ports
        self.service_type = service_type
        self.run_as_user = run_as_user
        self.fs_group = fs_group


class TaskValidatorContainerServe(TaskValidatorFunction):
    """
    TaskValidatorContainerServe validator.
    """

    replicas: int = Field(default=None, ge=0)
    """Number of replicas."""

    service_type: CoreServiceType = Field(default=CoreServiceType.NODE_PORT.value)
    """Service type."""

    service_ports: list[CorePort] = None
    """Service ports mapper."""

    run_as_user: int = Field(default=None, ge=0)
    """RunAsUser."""

    fs_group: int = Field(default=None, ge=1)
    """FSGroup."""
