from __future__ import annotations

from action import PaintAction
from data_structures.stack_adt import ArrayStack
from grid import Grid


class UndoTracker:

    def __init__(self):
        """
        Initialises an action and redo Array Stack of length max_actions
        Args:
            - Nothing

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(max_capacity), where max_capacity is the max_actions
            Worst: O(max_capacity), same as best
        """
        max_actions = 10000
        self.action_stack = ArrayStack(max_actions)
        self.redo_stack = ArrayStack(max_actions)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        Args:
            - action: an object of type PaintAction

        Raises:
            - Type Error: if action is not of Type PaintAction

        Returns:
            - None

        Complexity:
            Best: O(1), is_full and push are both constant
            Worst: O(1), same as best
        """
        if not isinstance(action, PaintAction):
            raise TypeError("grid input is not of type Grid")

        if self.action_stack.is_full():
            pass
        else:
            self.action_stack.push(action)

    def undo(self, grid: Grid) -> PaintAction | None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.
        Args:
            - grid: an object of type Grid

        Raises:
            - Type Error: if grid is not of type Grid

        Returns:
            - The action that was undone, or None

        Complexity:
            Best: O(undo_apply), all other operations are constant so will be dominated by undo_apply which will be
            constant or greater
            Worst: O(undo_apply), same as best
        """
        if not isinstance(grid, Grid):
            raise TypeError("grid input is not of type Grid")

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
        Args:
            - grid: an object of type Grid

        Raises:
            - Type Error: if grid is not of type Grid

        Returns:
            - The action that was redone, or None

        Complexity:
            Best: O(redo_apply), all other operations are constant so will be dominated by undo_apply which will be
            constant or greater
            Worst: O(redo_apply), same as best
        """
        if not isinstance(grid, Grid):
            raise TypeError("grid input is not of type Grid")

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
