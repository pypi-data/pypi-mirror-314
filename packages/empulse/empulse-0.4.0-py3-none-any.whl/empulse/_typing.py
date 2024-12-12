from typing import Protocol, Any


class Fittable(Protocol):

    def fit(self, X, y, sample_weight=None, **kwargs: Any) -> "Fittable":  # TODO: allow more other kwargs
        ...
