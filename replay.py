from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue


class ReplayTracker:
    def __init__(self) -> None:
        """
        Initialises replay and bool circular queues of size max_actions to track the replays to be done and whether
        they are undos or not
        Args:
            - No arguments

        Raises:
            - Nothing

        Returns:
            - None

        Complexity:
            Best: O(max_capacity), where max_capacity is max_actions, based on ArrayR
            Worst: O(max_capacity), same as best
        """
        max_actions = 10000
        self.replay_queue = CircularQueue(max_actions)
        self.bool_tracker = CircularQueue(max_actions)

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """

        pass

    def add_action(self, action: PaintAction, is_undo: bool = False) -> None:
        """
        Adds an action to the replay.
        Args:
            - action: an object of type PaintAction
            - is_undo: a bool specifying whether the action was an undo action or not. Special, Redo, and Draw all
            have this is False.

        Raises:
            - Type Error: if action is not of Type PaintAction

        Returns:
            - None

        Complexity:
            Best: O(1), append and is_full are both constant
            Worst: O(1), same as best
        """
        if not isinstance(action, PaintAction):
            raise TypeError("action input is not of type PaintAction")

        if self.replay_queue.is_full():
            pass
        else:
            self.replay_queue.append(action)
            self.bool_tracker.append(is_undo)

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Args:
            - grid: a Grid object

        Raises:
            - Type Error: if grid is not of type Grid

        Returns:
            - bool: If there were no more actions to play, and so nothing happened, return True. Otherwise, return
            False.

        Complexity:
            Best: O(n), where n is the greater complexity of redo_apply and undo_apply
            Worst: O(n), where n is the greater complexity of redo_apply and undo_apply
        """
        if not isinstance(grid, Grid):
            raise TypeError("grid input is not of type Grid")

        if self.replay_queue.is_empty():
            self.replay_queue.clear()
            return True
        else:
            undo_bool = self.bool_tracker.serve()
            action = self.replay_queue.serve()
            if not undo_bool:
                action.redo_apply(grid)
            else:
                action.undo_apply(grid)

            return False


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g)  # action 1, special
    f2 = r.play_next_action(g)  # action 2, draw
    f3 = r.play_next_action(g)  # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)
