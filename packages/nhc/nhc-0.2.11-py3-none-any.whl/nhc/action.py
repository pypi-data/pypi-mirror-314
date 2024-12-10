class NHCAction:
    """A Niko Action."""

    def __init__(self, controller, action):
        """Init Niko Action."""
        self._state = action["value1"]
        self._id = action["id"]
        self._type = action["type"]
        self._name = action["name"]
        self._controller = controller
        self._suggested_area = controller.locations[action["location"]]

    @property
    def state(self):
        """A Niko Action state."""
        return self._state

    @property
    def suggested_area(self):
        """A Niko Action location."""
        return self._suggested_area

    @property
    def name(self):
        """A Niko Action state."""
        return self._name

    @property
    def id(self):
        """A Niko Action action_id."""
        return self._id

    @property
    def type(self):
        """The Niko Action type."""
        return self._type

    def is_light(self) -> bool:
        """Is a light."""
        return self.type == 1

    def is_dimmable(self) -> bool:
        """Is a dimmable light."""
        return self.type == 2

    def is_fan(self) -> bool:
        """Is a fan."""
        return self.type == 3

    def is_cover(self) -> bool:
        """Is a cover."""
        return self.type == 4

    def update_state(self, state):
        """Update state."""
        self._state = state
