from __future__ import annotations

from abc import ABC, abstractmethod

from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet
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

    def __init__(self):
        super().__init__()
        self.stack = ArrayStack(1)
        self.special_bool = False

    def add(self, layer: Layer) -> bool:
        self.layer = layer  # should this be in init?
        # initialise an adt that can store 1 object, stack of length 1?

        # add layer to stack
        if self.stack.is_full():
            self.stack.pop()
            self.stack.push(self.layer)
        else:
            self.stack.push(self.layer)

        # need to return true if the LayerStore was actually changed
        # how to know if the layer store was changed?
        # could peek, store previous colour somewhere, add

    def erase(self, layer: Layer) -> bool:
        # can pop since there should be only 1 item in the stack
        if self.stack.is_empty():
            return self.stack.is_empty()
        else:
            self.stack.pop()
        return self.stack.is_empty()

    def special(self):
        # applies the colour and then invert it? - wed app opt
        # needs to change the way get colour works? - wed app opt
        """
        Keeps the current layer, but always applies an inversion of the colours after the layer has been applied
        """

        '''Special is just a switch, have implementation in get_color which runs depending on what the switch is set
        to in special'''

        if not self.special_bool:
            self.special_bool = True
        elif self.special_bool:
            self.special_bool = False

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        self.start = start  # 3 int tuple that is a colour
        self.timestamp = timestamp
        self.x = x
        self.y = y

        # take the layer stored in self.stack
        # put self.start into that layer, return result
        if self.stack.is_empty():
            return self.start

        if not self.special_bool:
            self.layer_peek = self.stack.peek()
            self.colour = self.layer_peek.apply(self.start, self.timestamp, self.x, self.y)
        elif self.special_bool:
            self.layer_peek = self.stack.peek()
            self.current_color = self.layer_peek.apply(self.start, self.timestamp, self.x, self.y)
            self.colour = invert.apply(self.current_color, self.timestamp, self.x, self.y)

        return self.colour


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self):
        super().__init__()
        self.max_size = len(get_layers())
        self.queue = CircularQueue(self.max_size * 100)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        self.layer = layer
        self.queue.append(self.layer)

        # check if queue is full?

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Erasing from an Additive Layer always removes the oldest remaining layer (first element)
        """
        self.queue_length = len(self.queue)  # should this be self.queue.length
        self.queue.serve()
        return self.queue_length == len(self.queue) + 1  # returns true if length of queue has decreased by 1

    def special(self):
        # copied and pasted from ed forums
        my_stack = ArrayStack(self.max_size * 100)  # used to reverse
        result_queue = CircularQueue(self.max_size * 100)  # used for computing the result

        for _ in range(len(self.queue)):
            item = self.queue.serve()
            my_stack.push(item)
            self.queue.append(item)  # restore my_queue’s items

        while not my_stack.is_empty():
            item = my_stack.pop()
            if item:  # empty string is False in boolean context
                result_queue.append(item)

        self.queue = result_queue

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        colour = start

        # looping through length(self.queue)
        count = 0
        while count < self.queue.length:
            # layer = serve() first element -> Layer
            layer = self.queue.serve()

            # colour = layer.apply(colour, timestamp, x, y)
            colour = layer.apply(colour, timestamp, x, y)

            # need to append layer back to self.queue
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

    def __init__(self):
        super().__init__()
        self.max_size = len(get_layers())
        self.sorted_list = ArraySortedList(self.max_size * 100)
        self.special_sorted_list = ArraySortedList(self.max_size * 100)

    def add(self, layer: Layer) -> bool:
        # key is layer.index
        key = layer.index
        # list item of layer and layer.index
        list_item = ListItem(layer, key)

        self.sorted_list.add(list_item)

    def erase(self, layer: Layer) -> bool:
        # .remove from sorted_list_adt
        key = layer.index
        list_item = ListItem(layer, key)
        if self.sorted_list.__contains__(list_item):
            self.sorted_list.remove(list_item)

    def special(self):
        # look at array sorted list (sorted by index currently)
        # dont change original one
        # add another sorted list of layers of the applied layers but these are alphabetically sorted
        # use layer.name as the key

        for i in range(self.sorted_list.length):
            list_item = self.sorted_list[i]
            value = list_item.value
            key = value.name
            list_item_special = ListItem(value, key)
            self.special_sorted_list.add(list_item_special)

        if self.special_sorted_list.length % 2 == 1:
            index = self.special_sorted_list.length // 2
            self.special_sorted_list.delete_at_index(index)
        else:
            index = (self.special_sorted_list.length // 2) - 1
            self.special_sorted_list.delete_at_index(index)

        self.sorted_list = self.special_sorted_list

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        colour = start

        # looping through length(self.queue)
        count = 0
        while count < self.sorted_list.length:
            # layer = serve() first element -> Layer
            list_item = self.sorted_list[count]

            layer = list_item.value

            # colour = layer.apply(colour, timestamp, x, y)
            colour = layer.apply(colour, timestamp, x, y)

            count += 1

        return colour
