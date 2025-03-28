from __future__ import annotations

from abc import ABC, abstractmethod

from data_structures.array_sorted_list import ArraySortedList
from data_structures.queue_adt import CircularQueue
from data_structures.sorted_list_adt import ListItem
from data_structures.stack_adt import ArrayStack
from layer_util import Layer
from layer_util import get_layers
from layers import *


class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass


class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        """
        Initialises an ArrayStack and a boolean variable for the special function
        Args:
            - Nothing

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(1), initialising an ArrayStack is constant complexity
            Worst: O(1), same as best
        """
        super().__init__()
        self.stack = ArrayStack(1)
        self.special_bool = False

    def add(self, layer: Layer) -> bool:
        """
        Set the single layer.
        Returns true if the LayerStore was actually changed.
        Args:
            - layer: a Layer object

        Raises:
            - TypeError: if input is not of type Layer

        Returns:
            - bool: True if the LayerStore was changed, false if not

        Complexity:
            Best: O(1), to add a layer even if the stack is empty, pushing is constant complexity
            Worst: O(1), same as best, popping and pushing and checking is_full are all constant complexity
        """
        if not isinstance(layer, Layer):
            raise TypeError("Input is not a Layer")
        if self.stack.is_full():
            self.stack.pop()
            self.stack.push(layer)
            return True
        else:
            self.stack.push(layer)
            return True

    def erase(self, layer: Layer) -> bool:
        """
        Removes the single layer. Ignores what is currently selected.
        Returns true if the LayerStore was actually changed.
        Args:
            - layer: a Layer object

        Raises:
            - TypeError: if input is not of type Layer

        Returns:
            - bool: True if the LayerStore was changed, false if not

        Complexity:
            Best: O(1), constant complexity for is_empty
            Worst: O(1), same as best, constant complexity for all operations
        """
        if not isinstance(layer, Layer):
            raise TypeError("Input is not a Layer")

        if self.stack.is_empty():
            return self.stack.is_empty()
        else:
            self.stack.pop()

        return self.stack.is_empty()

    def special(self) -> None:
        """
        Keeps the current layer, but always applies an inversion of the colours after the layer has been applied
        Args:
            - Nothing

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(1), assignment is constant
            Worst: O(1), same as best, assignment is constant
        """

        if not self.special_bool:
            self.special_bool = True
        elif self.special_bool:
            self.special_bool = False

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
            - start: tuple of ints, this is the RGB value of the starting colour
            - timestamp: int, used for animated layers
            - x: int, x coordinate where get_colour is being called
            - y: int, y coordinate where get_colour is being called

        Raises:
            - Value Error: when x or y are less than 0

        Returns:
            - result: a tuple of ints, this will be the resulting colour after checking the applied layers

        Complexity: Best: O(1), if the special function hasn't been toggled and there is no layer applied meaning the
        stack is empty, is_empty is constant and returning a value is constant
        Worst: O(apply), if the special function is on and a layer has been applied. In this case, peek is O(1), so the
        dominating complexity would be apply
        """
        if x < 0:
            raise ValueError("x must be greater than 0")
        if y < 0:
            raise ValueError("y must be greater than 0")

        if not self.special_bool:
            if self.stack.is_empty():
                return start
            else:
                layer_peek = self.stack.peek()
                colour = layer_peek.apply(start, timestamp, x, y)
        elif self.special_bool:
            if self.stack.is_empty():
                colour = invert.apply(start, timestamp, x, y)
            else:
                layer_peek = self.stack.peek()
                current_color = layer_peek.apply(start, timestamp, x, y)
                colour = invert.apply(current_color, timestamp, x, y)

        return colour


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        """
        Initialises a CircularQueue of the maximum size of the number of layers multiplied by 100

        Args:
            - Nothing

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(self.max_size), dependent on ArrayR where the complexity is O(max_capacity)
            Worst: O(self.max_size), same as best
        """
        super().__init__()
        self.max_size = len(get_layers())
        self.queue = CircularQueue(self.max_size * 100)

    def add(self, layer: Layer) -> bool:
        """
        Add a new layer to be added last.
        Returns true if the LayerStore was actually changed.
        Args:
            - layer: a Layer object

        Raises:
            - TypeError: if layer input is not of type Layer

        Returns:
            - bool: True if the LayerStore was changed, false if not

        Complexity:
            Best: O(1), all constant operations
            Worst: O(1), same as best
        """
        if not isinstance(layer, Layer):
            raise TypeError("Input is not a Layer")

        if not self.queue.is_full():
            queue_length = self.queue.length
            self.queue.append(layer)
            return queue_length + 1 == self.queue.length
        else:
            return False

    def erase(self, layer: Layer) -> bool:
        """
        Removes the oldest remaining layer (first element)
        Returns true if the LayerStore was actually changed.
        Args:
            - layer: a Layer object

        Raises:
            - TypeError: if input is not of type Layer

        Returns:
            - bool: True if the LayerStore was changed, false if not

        Complexity:
            Best: O(1), all constant operations
            Worst: O(1), same as best
        """
        if not isinstance(layer, Layer):
            raise TypeError("Input is not a Layer")

        if not self.queue.is_empty():
            queue_length = self.queue.length
            self.queue.serve()
            return queue_length == self.queue.length + 1
        else:
            return False

    def special(self) -> None:
        """
        Reverse the order of current layers (first becomes last, etc.)
        Args:
            - Nothing

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(n) where n is the length of either the stack or the queue
            Worst: O(n), same as best
        """
        # creating stack to reverse
        result_stack = ArrayStack(self.max_size * 100)
        # creating queue for the result
        result_queue = CircularQueue(self.max_size * 100)

        for i in range(self.queue.length):
            layer = self.queue.serve()
            result_stack.push(layer)
            # restoring layers to queue
            self.queue.append(layer)

        while not result_stack.is_empty():
            result_layer = result_stack.pop()
            if result_layer:
                result_queue.append(result_layer)

        self.queue = result_queue

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
            - start: tuple of ints, this is the RGB value of the starting colour
            - timestamp: int, used for animated layers
            - x: int, x coordinate where get_colour is being called
            - y: int, y coordinate where get_colour is being called

        Raises:
            - Value Error: when x or y are less than 0

        Returns:
            - result: a tuple of ints, this will be the resulting colour after checking the applied layers

        Complexity:
            Best: O(n*apply), where n is the length of the queue and apply is the apply function
            Worst: O(n*apply), same as best
        """
        if x < 0:
            raise ValueError("x must be greater than 0")
        if y < 0:
            raise ValueError("y must be greater than 0")
        colour = start
        count = 0
        while count < self.queue.length:
            layer = self.queue.serve()
            colour = layer.apply(colour, timestamp, x, y)
            self.queue.append(layer)
            count += 1
        return colour


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        """
        Initialises an ArraySortedList
        Args:
            - Nothing

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(1), initialising an Array Sorted List is constant
            Worst: O(1), same as best
        """
        super().__init__()
        self.number_of_layers = 9
        self.sorted_list = ArraySortedList(self.number_of_layers)

    def add(self, layer: Layer) -> bool:
        """
        Ensure this layer type is applied.
        Returns true if the LayerStore was actually changed.
        Args:
            - layer: a Layer object

        Raises:
            - TypeError: if layer input is not of type Layer

        Returns:
            - bool: True if the LayerStore was changed, false if not

        Complexity:
            Best: O(log len(sorted_list)), or when the item is last
            Worst: O(len(sorted_list)), or when the item is first
        """
        if not isinstance(layer, Layer):
            raise TypeError("Input is not a Layer")
        key = layer.index
        list_item = ListItem(layer, key)
        self.sorted_list.add(list_item)
        return self.sorted_list.__contains__(list_item)

    def erase(self, layer: Layer) -> bool:
        """
        Ensure this layer type is not applied.
        Returns true if the LayerStore was actually changed.
        Args:
            - layer: a Layer object

        Raises:
            - TypeError: if input is not of type Layer

        Returns:
            - bool: True if the LayerStore was changed, false if not

        Complexity:
            Best: O(1), item to be erased is the first element in the sorted list
            Worst: O(n), where n is the length of the sorted list
        """
        key = layer.index
        erase_list_item = ListItem(layer, key)
        for i in self.sorted_list:
            if self.sorted_list.__contains__(erase_list_item):
                self.sorted_list.remove(erase_list_item)
        return self.sorted_list.__contains__(erase_list_item)

    def special(self) -> None:
        """
        Deletes the median layer of the lexicographically sorted currently applying layers
        Args:
            - Nothing

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(n), where n is the length of the sorted list
            Worst: O(n), same as best
        """
        special_sorted_list = ArraySortedList(self.number_of_layers)
        if not self.sorted_list.is_empty():
            for i in range(self.sorted_list.length):
                list_item = self.sorted_list[i]
                value = list_item.value
                key = value.name
                list_item_special = ListItem(value, key)
                special_sorted_list.add(list_item_special)

            if special_sorted_list.length % 2 == 1:
                index = special_sorted_list.length // 2
                # get item at index, item_to_delete is a ListItem
                item_to_delete = special_sorted_list[index]

            else:
                index = (special_sorted_list.length // 2) - 1
                item_to_delete = special_sorted_list[index]

            # new_value should be a Layer from the item_to_delete ListItem
            new_value = item_to_delete.value
            # new_key should be the unique index of the Layer
            new_key = new_value.index
            new_list_item = ListItem(new_value, new_key)
            new_index = self.sorted_list.index(new_list_item)
            self.sorted_list.delete_at_index(new_index)

    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
            - start: tuple of ints, this is the RGB value of the starting colour
            - timestamp: int, used for animated layers
            - x: int, x coordinate where get_colour is being called
            - y: int, y coordinate where get_colour is being called

        Raises:
            - Value Error: when x or y are less than 0

        Returns:
            - result: a tuple of ints, this will be the resulting colour after checking the applied layers

        Complexity:
            Best: O(n*apply), where n is the length of the sorted list and apply is the apply function
            Worst: O(n*apply), same as best
        """
        if x < 0:
            raise ValueError("x must be greater than 0")
        if y < 0:
            raise ValueError("y must be greater than 0")

        colour = start
        count = 0
        while count < self.sorted_list.length:
            list_item = self.sorted_list[count]
            layer = list_item.value
            colour = layer.apply(colour, timestamp, x, y)
            count += 1
        return colour
