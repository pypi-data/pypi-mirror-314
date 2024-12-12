from .Watch import Watch

class WatchAttr(Watch):
    def __init__(self, attributes, effect):
        self._attributes = attributes
        super().__init__(effect)
        self._track()

    def _track(self):
        self.stop()
        for attr in self._attributes:
            if hasattr(attr, "_observers") and attr._observers is not None:
                if self not in attr._observers:
                    attr._observers.append(self)
                    self._deps.append(attr)
        if self._effect:
            self._effect()


    def stop(self):
        for dep in self._deps:
            dep._observers.remove(self)
        self._deps = []