from typing import List, Dict, Any
import random

# Base Class
class Randomizer:
    def __init__(self, allow_duplicates: bool = True):
        self.inputs: List[str | int] = []
        self.results: List[str | int] = []
        self.allow_duplicates = allow_duplicates

    def add_input(self, input_data: str | int):
        """Adds a single input to the list."""
        self.inputs.append(input_data)

    def add_inputs(self, input_list: List[str | int]):
        """Adds multiple inputs to the list."""
        self.inputs.extend(input_list)

    def clear_inputs(self):
        """Clears all inputs."""
        self.inputs.clear()

    def get_results(self) -> List[str | int]:
        """Returns the results."""
        return self.results

# Subclass: GroupRandomizer
class GroupRandomizer(Randomizer):
    def __init__(self, allow_duplicates: bool = True):
        super().__init__(allow_duplicates)
        self.group_size: int = 0
        self.number_of_groups: int = 0

    def set_group_size(self, size: int):
        """Sets the desired group size."""
        self.group_size = size

    def set_number_of_groups(self, count: int):
        """Sets the desired number of groups."""
        self.number_of_groups = count

    def generate_groups(self) -> List[List[str | int]]:
        """Randomly divides inputs into groups based on group_size or number_of_groups."""
        items = self.inputs[:]
        if not self.allow_duplicates:
            items = list(set(items))
        random.shuffle(items)
        if self.group_size > 0:
            self.results = [items[i:i + self.group_size] for i in range(0, len(items), self.group_size)]
        elif self.number_of_groups > 0:
            self.results = [items[i::self.number_of_groups] for i in range(self.number_of_groups)]
        else:
            self.results = []
        return self.results

# Subclass: ShuffleRandomizer
class ShuffleRandomizer(Randomizer):
    def shuffle_items(self) -> List[str | int]:
        """Randomly shuffles the order of the inputs and updates results."""
        items = self.inputs[:]
        if not self.allow_duplicates:
            items = list(set(items))
        random.shuffle(items)
        self.results = items
        return self.results

    def pick_single_item(self) -> str | int:
        """Randomly picks a single item from the inputs."""
        items = self.inputs[:]
        if not self.allow_duplicates:
            items = list(set(items))
        self.results = [random.choice(items)]
        return self.results[0]

# Subclass: OutputGenerator
class OutputGenerator(Randomizer):
    def __init__(self):
        super().__init__()
        self.output_type: str = ""
        self.constraints: Dict[str, Any] = {}

    def set_output_type(self, type: str):
        """Sets the type of output to generate."""
        self.output_type = type

    def set_constraints(self, constraints: Dict[str, Any]):
        """Configures generation constraints."""
        self.constraints = constraints

    def generate_output(self, count: int = 1) -> List[Any]:
        """Generates one or more random outputs based on the type and constraints."""
        self.results = []
        if self.output_type == "number":
            start, end = self.constraints.get("range", (0, 10))
            self.results = [random.randint(start, end) for _ in range(count)]
        elif self.output_type == "letter":
            charset = self.constraints.get("charset", "abcdefghijklmnopqrstuvwxyz")
            self.results = [random.choice(charset) for _ in range(count)]
        elif self.output_type == "custom":
            options = self.constraints.get("options", [])
            self.results = [random.choice(options) for _ in range(count)]
        return self.results

# Helper Class: Preferences
class Preferences:
    def __init__(self):
        self.allow_duplicates: bool = True

    def toggle_duplicates(self, allow: bool):
        """Enables or disables duplicate results."""
        self.allow_duplicates = allow

# Subclass: ResultDisplay
class ResultDisplay:
    @staticmethod
    def display_on_screen(results: List[Any]):
        """Displays results in a user-friendly format."""
        for index, result in enumerate(results, start=1):
            print(f"Result {index}: {result}")
