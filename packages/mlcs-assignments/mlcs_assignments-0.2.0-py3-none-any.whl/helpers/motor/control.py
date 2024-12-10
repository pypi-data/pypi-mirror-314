from typing import Protocol
from dataclasses import dataclass


@dataclass(frozen=True)
class ControlDecision:
    on: bool
    t_start: float
    t_end: float


class CachingController(Protocol):
    def control(self, t: float) -> bool:
        """Returns the control signal at time `t`."""
        ...

    def _in_cache(self, t: float) -> bool:
        """Checks if the cache contains a decision for time `t`."""
        ...

    def _from_cache(self, t: float) -> ControlDecision:
        """Returns the decision from the cache for time `t`."""
        ...

    def _add_to_cache(self, on: bool, t_end: float) -> None:
        """Adds a decision to the cache."""
        ...

    @property
    def cache(self) -> list[ControlDecision]:
        """The cache of control decisions."""
        ...

    @cache.setter
    def cache(self, value: list[ControlDecision]) -> None:
        """Sets the cache of control decisions."""
        ...


class CachingControllerMixin:
    """This mixin adds caching to a controller.

    Example:
        If you have a controller, you can add caching to it like this:

        ```python
        class MyController(CachingControllerMixin, ...):
            ...

        # Now `MyController` has caching capabilities and can be used like a normal controller.
        ```
    """

    _cache: list[ControlDecision]

    def __call__(self: CachingController, t: float) -> float:
        if self._in_cache(t):
            return self._from_cache(t).on

        on = self.control(t)
        self._add_to_cache(on, t)

        return 1.0 if on else 0.0

    def _in_cache(self: CachingController, t: float) -> bool:
        return any(decision.t_start <= t <= decision.t_end for decision in self.cache)

    def _from_cache(self: CachingController, t: float) -> ControlDecision:
        return next(
            decision
            for decision in self.cache
            if decision.t_start <= t <= decision.t_end
        )

    def _add_to_cache(self: CachingController, on: bool, t_end: float) -> None:
        if len(self.cache) == 0:
            t_start = 0.0
        else:
            t_start = self.cache[-1].t_end

        self.cache.append(ControlDecision(on=on, t_start=t_start, t_end=t_end))

    @property
    def cache(self) -> list[ControlDecision]:
        if not hasattr(self, "_cache"):
            self._cache = []
        return self._cache

    @cache.setter
    def cache(self, value: list[ControlDecision]) -> None:
        self._cache = value
