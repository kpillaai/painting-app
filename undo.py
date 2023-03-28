from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack


class UndoTracker:

    def __init__(self):
        max_actions = 10000
        self.action_stack = ArrayStack(max_actions)
        self.redo_stack = ArrayStack(max_actions)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        # initialise ADT of size 10000
        # check if ADT is full, if yes then break, if not add action to the adt
        if self.action_stack.is_full():
            pass
        else:
            self.action_stack.push(action)

    def undo(self, grid: Grid) -> PaintAction | None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        # checking if stack of PaintActions is empty, if yes return None
        if self.action_stack.is_empty():
            return None

        else:
            # peek to take the last action
            action = self.action_stack.peek()

            # undo the action on the grid
            action.undo_apply(grid)

            # add the undone action to a redo stack
            self.redo_stack.push(action)

            # remove the undone action from the action stack
            self.action_stack.pop()

            # return the undone action
            return action

    def redo(self, grid: Grid) -> PaintAction | None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        # check if stack of PaintActions is empty, if yes return None
        if self.redo_stack.is_empty():
            return None
        else:
            # peek to get the latest undone action
            action = self.redo_stack.peek()

            # redo the latest undone action on the grid
            action.redo_apply(grid)

            # put the redone action back onto the action stack
            self.action_stack.push(action)

            # remove the redone action from redo stack
            self.redo_stack.pop()

            # return the redone action
            return action
