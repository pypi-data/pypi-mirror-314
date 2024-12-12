from reactive.shared import current_observers


class Watch:
    def __init__(self, effect):
        self._effect = effect
        self._deps = []
        self._track()

    def _track(self):
        current_observers.append(self)
        self._effect()
        current_observers.pop()

    def stop(self):
        for dep in self._deps:
            dep._observers.remove(self)
        self._deps = []
        self._effect = None
