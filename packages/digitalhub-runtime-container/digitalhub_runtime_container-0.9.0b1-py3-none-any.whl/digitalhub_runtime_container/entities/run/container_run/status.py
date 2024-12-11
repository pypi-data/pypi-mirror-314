from __future__ import annotations

from digitalhub.entities.run._base.status import RunStatus


class RunStatusContainerRun(RunStatus):
    """
    RunStatusContainerRun status.
    """

    def __init__(
        self,
        state: str,
        message: str | None = None,
        transitions: list[dict] | None = None,
        k8s: dict | None = None,
        service: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(state, message, transitions, k8s, **kwargs)
        self.service = service
