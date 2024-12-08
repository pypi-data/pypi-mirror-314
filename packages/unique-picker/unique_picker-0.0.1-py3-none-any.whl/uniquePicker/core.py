import random


class UniqueRandom:
    def __init__(self, items):
        """Initialize with a list of items."""
        self.items = items[:]
        self._current_cycle = []

    def choice(self):
        """
        Return a random item from the list without repeating
        until all items are exhausted in the current cycle.
        """
        if not self._current_cycle:
            self._current_cycle = self.items[:]
            random.shuffle(self._current_cycle)
        return self._current_cycle.pop()


# Singleton instance to maintain state
_instance = None


def choice(items):
    """
    Select a random item from the list without repeating until all items are covered.
    """
    global _instance
    if _instance is None or _instance.items != items:
        _instance = UniqueRandom(items)
    return _instance.choice()
