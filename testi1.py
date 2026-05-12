from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

Condition = Callable[['Step', Optional['Step']], bool]

import time
import keyboard

@dataclass
class Step:
    name: str
    comment: str
    on_enter: Optional[Callable[['Step'], None]] = None
    on_exit: Optional[Callable[['Step'], None]] = None

    # Execute the step's enter callback when the step becomes active.
    def enter(self) -> None:
        if self.on_enter:
            self.on_enter(self)

    # Execute the step's exit callback when the step is left.
    def exit(self) -> None:
        if self.on_exit:
            self.on_exit(self)


class Sequence:
    # Initialize the sequence with steps and optional automatic transition conditions.
    def __init__(self, steps: List[Step], auto_forward_condition: Optional[Condition] = None,
                 auto_backward_condition: Optional[Condition] = None) -> None:
        if not steps:
            raise ValueError('Sequence must contain at least one step.')
        self.steps = steps
        self.current_index = 0
        self.auto_forward_condition = auto_forward_condition
        self.auto_backward_condition = auto_backward_condition
        self._enter_current_step()

    # Return the currently active step in the sequence.
    @property
    def current_step(self) -> Step:
        return self.steps[self.current_index]

    # Enter the current step and invoke its enter callback.
    def _enter_current_step(self) -> None:
        self.current_step.enter()

    # Exit the current step and invoke its exit callback.
    def _exit_current_step(self) -> None:
        self.current_step.exit()

    # Advance to the next step if available and run transition callbacks.
    def next(self) -> bool:
        if self.current_index >= len(self.steps) - 1:
            return False
        self._exit_current_step()
        self.current_index += 1
        self._enter_current_step()
        return True

    # Move back to the previous step if available and run transition callbacks.
    def previous(self) -> bool:
        if self.current_index <= 0:
            return False
        self._exit_current_step()
        self.current_index -= 1
        self._enter_current_step()
        return True

    # Jump directly to a specific step index in the sequence.
    def go_to(self, index: int) -> bool:
        if index < 0 or index >= len(self.steps) or index == self.current_index:
            return False
        self._exit_current_step()
        self.current_index = index
        self._enter_current_step()
        return True

    # Check automatic conditions and transition forward or backward if triggered.
    def update(self) -> None:
        next_step = self.steps[self.current_index + 1] if self.current_index < len(self.steps) - 1 else None
        previous_step = self.steps[self.current_index - 1] if self.current_index > 0 else None
        if self.auto_forward_condition and next_step and self.auto_forward_condition(self.current_step, next_step):
            self.next()
        elif self.auto_backward_condition and previous_step and self.auto_backward_condition(self.current_step, previous_step):
            self.previous()

    # Set a new condition for automatic forward transitions.
    def set_auto_forward_condition(self, condition: Condition) -> None:
        self.auto_forward_condition = condition

    # Set a new condition for automatic backward transitions.
    def set_auto_backward_condition(self, condition: Condition) -> None:
        self.auto_backward_condition = condition

    # Return the relative progress through the sequence as a float between 0.0 and 1.0.
    @property
    def progress(self) -> float:
        return self.current_index / (len(self.steps) - 1) if len(self.steps) > 1 else 1.0

    # Return the sequence completion percentage as an integer from 0 to 100.
    @property
    def percentage_complete(self) -> int:
        return int(self.progress * 100)

    # Produce a readable string representation of the current sequence state.
    def __str__(self) -> str:
        return f"Sequence(index={self.current_index}, step={self.current_step.name}, percent={self.percentage_complete}%)"


class Testisovellus:
    def __init__(self) -> None:
        self.sequence = Sequence(
            steps=[
                Step(name='Initialize', comment='Alkuvalmistelut'),
                Step(name='eka', comment='Eka vaihe'),
                Step(name='toka', comment='Toinen vaihe'),
                Step(name='kolmas', comment='Kolmas vaihe'),
                Step(name='Finalize', comment='Viimeinen vaihe'),
            ],
            auto_forward_condition=lambda current, next_step: current.name == 'Initialize',
            auto_backward_condition=lambda current, previous_step: current.name == 'Process'
        )
    def ohje(self):
        print('komennot:')
        print('0 lopetus')
        print('1 eteenpäin')
        print('2 taaksepäin')

    def suorita(self):
        self.ohje()
        while True:
            print("")
            komento = input("komento: ")
            if komento == "0":
                break
            elif komento == "1":
                moved = self.sequence.next()
                print('Moved forward:', moved, self.sequence)
            elif komento == "2":
                moved = self.sequence.previous()
                print('Moved backward:', moved, self.sequence)
            else:
                self.ohje()


class sekvenssi1:
    def __init__(self):
        self.sequence = Sequence(
            steps=[
                Step(name='Initialize', comment='Alkuvalmistelut'),
                Step(name='eka', comment='Eka vaihe'),
                Step(name='toka', comment='Toinen vaihe'),
                Step(name='kolmas', comment='Kolmas vaihe'),
                Step(name='Finalize', comment='Viimeinen vaihe'),
            ],
            auto_forward_condition=lambda current, next_step: current.name == 'Initialize',
            auto_backward_condition=lambda current, previous_step: current.name == 'Process'
        )



    # Process key press events: 1 for forward, 2 for backward, return True if ESC pressed.
    def key_event(self) -> bool:
        if keyboard.is_pressed('1'):
            moved = self.sequence.next()
            print('Moved forward:', moved, self.sequence)
            time.sleep(0.3)
        elif keyboard.is_pressed('2'):
            moved = self.sequence.previous()
            print('Moved backward:', moved, self.sequence)
            time.sleep(0.3)
        elif keyboard.is_pressed('esc'):
            return True
        return False

    def run(self):
        print('Sequence Control Running')
        print('Press 1 for next, 2 for previous, ESC to exit')
        while True:
            print('')
            print(self.sequence)
            
            # Check for key presses over 1 second interval
            start_time = time.time()
            while time.time() - start_time < 1.0:
                if self.key_event():
                    print('Program terminated.')
                    return
                time.sleep(0.05)






if __name__ == '__main__':

    app = sekvenssi1()
    app.run()