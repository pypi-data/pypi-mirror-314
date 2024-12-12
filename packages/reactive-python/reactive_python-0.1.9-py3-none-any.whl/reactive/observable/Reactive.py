from reactive.shared import current_observers


class Reactive:
    def __init__(self, obj):
        object.__setattr__(self, "_data", obj)
        object.__setattr__(self, "_observers", [])

    def __getattr__(self, key):
        if key not in self._data:
            return None
        if len(current_observers) > 0:
            current_observer = current_observers[-1]
            self._observers.append(current_observer)
            current_observer._deps.append(self)
        return self._data[key]

    def __setattr__(self, key, value):
        self._data[key] = value
        self._trigger()

    def _trigger(self):
        for observer in self._observers:
            observer._effect()
