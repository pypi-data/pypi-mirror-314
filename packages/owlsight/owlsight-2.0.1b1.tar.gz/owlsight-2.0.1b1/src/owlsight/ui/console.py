from enum import Enum, auto
from typing import List, Dict, Tuple, Union, Any, Optional
import traceback
import sys

from prompt_toolkit import Application
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application.current import get_app


    
from owlsight.utils.constants import COLOR_CODES, MENU_KEYS, MAIN_MENU, get_prompt_cache
from owlsight.utils.logger import logger

try:
    from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
except:
    NoConsoleScreenBufferError = Exception


class HistoryCompleter(Completer):
    """
    A completer that provides suggestions based on the input history.
    """

    def __init__(self, history):
        """
        Initialize with the InMemoryHistory object.
        """
        self.history = history

    def get_completions(self, document, complete_event):
        """
        Generate completions from the history.
        """
        text_so_far = document.text_before_cursor
        # Get all unique entries in the history
        unique_history_items = list(set(self.history.get_strings()))

        for item in unique_history_items:
            if item.startswith(text_so_far):
                yield Completion(item, start_position=-len(text_so_far))


class OptionType(Enum):
    SINGLE = auto()  # A static option that can be selected
    EDITABLE = auto()  # An option where the user can input text
    TOGGLE = auto()  # A toggle option that can switch between multiple values


class Selector:
    def __init__(self, options_dict: Dict[str, Union[None, str, List[Any]]], start_index: int = 0) -> None:
        """
        Initialize the Selector with the given options.

        Parameters
        ----------
        options_dict : Dict[str, Union[None, str, List[Any]]]
            A dictionary where the key is the option label and the value defines
            the type of option. None is for static options, a string for editable input
            (empty string or default value), and a list (e.g., [True, False], [1, 2, 3])
            for toggleable options.
        start_index : int, optional
            The index of the option to start with in the menu, default is 0.
        """
        self.current_index: int = start_index
        self.options: List[Tuple[str, OptionType]] = []
        self.selected: bool = False
        self.user_inputs: Dict[str, str] = {}  # To store user input for editable fields
        self.toggle_values: Dict[str, Any] = {}  # To store current value for toggleable fields
        self.toggle_choices: Dict[str, List[Any]] = {}  # To store possible toggle values

        # Parse the options dictionary to categorize the options
        for key, value in options_dict.items():
            if value is None:
                self.options.append((key, OptionType.SINGLE))
            elif isinstance(value, list):  # Toggleable option
                self.options.append((key, OptionType.TOGGLE))
                self.toggle_choices[key] = value  # Store available toggle values
                self.toggle_values[key] = value[0]  # Set default to the first value
            elif isinstance(value, str):
                self.options.append((key, OptionType.EDITABLE))
                self.user_inputs[key] = value  # Use the provided string as default value


class OptionSelectorApp:
    def __init__(self) -> None:
        """
        Initialize the OptionSelectorApp, which is the main class for managing the user interface.
        """
        self.selector: Selector = None
        self.controls: List[Any] = []
        self.buffers: Dict[str, TextArea] = {}
        self.kb = KeyBindings()

        # Do not set the layout immediately; set it dynamically when the selector is ready.
        self.layout = None
        self.application = None
        self.history = {}
        self.build_key_bindings()

    def set_selector(self, selector: Selector) -> None:
        """
        Set a new Selector and rebuild the controls dynamically.
        This method is normally called every time the user makes a decision in a menu after pressing ENTER.
        """
        self.selector = selector
        self.controls = []
        self.buffers = {}
        self.build_controls()

        # Initialize the layout now that we have actual controls
        self.layout = Layout(HSplit(self.controls))

        try:
            self._initialize_application()
        except NoConsoleScreenBufferError:
            logger.error(f"Error initializing the application: {traceback.format_exc()}")
            sys.exit(1)

    def build_controls(self) -> None:
        """Build the controls for each option in the selector."""
        for i, (label, opt_type) in enumerate(self.selector.options):
            if opt_type == OptionType.SINGLE:
                control = self.create_single_option_control(i, label)
                self.controls.append(control)
            elif opt_type == OptionType.TOGGLE:
                control = self.create_toggle_option_control(i, label)
                self.controls.append(control)
            elif opt_type == OptionType.EDITABLE:
                control = self.create_editable_option_control(i, label)
                self.controls.append(control)

    def get_arrow(self, i: int) -> str:
        """Get the arrow for the current selection."""
        return ">" if i == self.selector.current_index else " "

    def invalidate(self) -> None:
        """Force redraw of the application."""
        app = get_app()
        if app:
            app.invalidate()

    def create_single_option_control(self, i: int, label: str) -> Window:
        """Create a control for a single option."""

        def get_text():
            arrow = self.get_arrow(i)
            return [("", f"{arrow} {label}")]

        control = FormattedTextControl(get_text)
        window = Window(content=control, height=1)
        return window

    def create_toggle_option_control(self, i: int, label: str) -> Window:
        """Create a control for a toggle option."""

        def get_text():
            arrow = self.get_arrow(i)
            current_value = self.selector.toggle_values[label]
            return [("", f"{arrow} {label}: {current_value}")]

        control = FormattedTextControl(get_text)
        window = Window(content=control, height=1)
        return window

    def create_editable_option_control(self, i: int, label: str) -> VSplit:
        """Create a control for an editable option."""
        # Create a TextArea for the editable field
        if label not in self.history:
            self.history[label] = FileHistory(get_prompt_cache())

        # Create the HistoryCompleter that fetches suggestions from the history
        completer = HistoryCompleter(self.history[label])

        text_area = TextArea(
            text=self.selector.user_inputs[label],
            multiline=False,
            wrap_lines=False,
            focus_on_click=True,
            height=1,  # Limit the TextArea to one line
            history=self.history[label],
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,  # Attach the completer for autocompletion from history
        )
        self.buffers[label] = text_area

        # Create a dynamic prompt that updates based on selection
        def get_prompt():
            arrow = self.get_arrow(i)
            return f"{arrow} {label} "

        prompt_control = FormattedTextControl(lambda: [("", get_prompt())])
        prompt_window = Window(content=prompt_control, dont_extend_width=True)

        # Combine the prompt and the TextArea in a VSplit
        control = VSplit(
            [
                prompt_window,
                text_area,
            ],
            height=1,
        )
        return control

    def update_focus(self, app: Application) -> None:
        """Set focus to the current control."""
        current_option, opt_type = self.selector.options[self.selector.current_index]
        if opt_type == OptionType.EDITABLE:
            app.layout.focus(self.buffers[current_option])
        else:
            app.layout.focus(self.controls[self.selector.current_index])

    def build_key_bindings(self) -> None:
        """Define the key bindings for the application."""

        @self.kb.add("up")
        def move_up(event):
            self.selector.current_index = (self.selector.current_index - 1) % len(self.selector.options)
            self.update_focus(event.app)
            self.invalidate()

        @self.kb.add("down")
        def move_down(event):
            self.selector.current_index = (self.selector.current_index + 1) % len(self.selector.options)
            self.update_focus(event.app)
            self.invalidate()

        @self.kb.add("left")
        def left(event):
            current_option, opt_type = self.selector.options[self.selector.current_index]
            if opt_type == OptionType.TOGGLE:
                choices = self.selector.toggle_choices[current_option]
                current_value = self.selector.toggle_values[current_option]
                current_index = choices.index(current_value)
                self.selector.toggle_values[current_option] = choices[(current_index - 1) % len(choices)]
            elif opt_type == OptionType.EDITABLE:
                # Move cursor to the left in the TextArea buffer
                buffer = self.buffers[current_option].buffer
                buffer.cursor_left()

            self.invalidate()

        @self.kb.add("right")
        def right(event):
            current_option, opt_type = self.selector.options[self.selector.current_index]
            if opt_type == OptionType.TOGGLE:
                choices = self.selector.toggle_choices[current_option]
                current_value = self.selector.toggle_values[current_option]
                current_index = choices.index(current_value)
                self.selector.toggle_values[current_option] = choices[(current_index + 1) % len(choices)]
            elif opt_type == OptionType.EDITABLE:
                # Move cursor to the right in the TextArea buffer
                buffer = self.buffers[current_option].buffer
                buffer.cursor_right()

            self.invalidate()

        @self.kb.add("enter")
        def enter(event):
            self.selector.selected = True
            current_option, opt_type = self.selector.options[self.selector.current_index]
            if opt_type == OptionType.EDITABLE:
                # Update the user input from the TextArea buffer
                user_input = self.buffers[current_option].text
                self._handle_editable_input(current_option, user_input)
                self.selector.user_inputs[current_option] = user_input
            event.app.exit()

        @self.kb.add("c-c")
        @self.kb.add("c-q")
        def exit_(event):
            event.app.exit()

    def run(self) -> None:
        """Run the application."""

        # Set initial focus
        def pre_run():
            self.update_focus(self.application)

        self.application.run(pre_run=pre_run)

    def _handle_editable_input(self, current_option, user_input) -> None:
        """Handle the input for editable fields."""
        if current_option == MENU_KEYS["assistant"]:
            self.history[current_option].append_string(user_input)

    def _initialize_application(self) -> None:
        """Initialize the application with the layout and key bindings."""
        self.application = Application(
            layout=self.layout,
            key_bindings=self.kb,
            full_screen=False,
        )


app = OptionSelectorApp()


def get_user_choice(
    options_dict: Dict[str, Union[None, str, List[Any]]],
    return_value_only: bool = True,
    start_index: int = 0,
) -> Union[str, Dict[str, Any]]:
    """
    Runs the command-line interface that allows the user to select or input options.

    Parameters
    ----------
    options_dict : Dict[str, Union[None, str, List[Any]]]
        The options to display to the user.
    return_value_only : bool, optional
        If True, return only the value; if False, return a dictionary with the key.
    start_index : int, optional
        The index of the option to start with in the menu, default is 0.

    Returns
    -------
    Union[str, Dict[str, Any]]
        The selected or inputted option as a string or dictionary.
    """
    global app
    selector = Selector(options_dict, start_index)
    app.set_selector(selector)
    app.run()

    # Return the selected option based on its type
    if selector.selected:
        selected_option, opt_type = selector.options[selector.current_index]
        if opt_type == OptionType.EDITABLE:
            # Update the user input from the TextArea buffer
            selector.user_inputs[selected_option] = app.buffers[selected_option].text
            # Return the user input for editable fields
            return (
                {selected_option: selector.user_inputs[selected_option]}
                if not return_value_only
                else selector.user_inputs[selected_option]
            )
        elif opt_type == OptionType.TOGGLE:
            # Return the current value for toggle fields
            return (
                {selected_option: selector.toggle_values[selected_option]}
                if not return_value_only
                else selector.toggle_values[selected_option]
            )
        else:
            # Return the label for static single-select fields
            return selected_option

    return ""


# TODO: refactor this part to handle mainmenu OR other menus in a more structured way
def get_user_input(
    menu: Optional[Dict[str, Union[None, str, List[Any]]]] = None, start_index: int = 0
) -> Tuple[str, Union[str, None]]:
    """
    Gets the user input from menu and returns the user choice and the corresponding key from the menu.

    Parameters
    ----------
    menu:  Optional[dict]
        The menu options to display
        if None, the main menu is displayed
    start_index:  int
        The starting index for the menu options

    Returns
    -------
    Tuple[str, Union[str, None]]
        The user choice and the corresponding option from the menu
    """
    if menu is None:
        menu = MAIN_MENU

    user_choice: Union[str, Dict] = get_user_choice(
        menu,
        return_value_only=False,
        start_index=start_index,
    )

    if isinstance(user_choice, dict):
        option = list(user_choice.keys())[0]
        return user_choice[option], option
    return user_choice, None


def print_colored(text: str, color: str) -> None:
    """
    Print text in the specified color.

    Parameters
    ----------
    text : str
        The text to print.
    color : str
        The color to print the text. Options are 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', and 'reset'.

    Raises
    ------
    ValueError
        If the provided color is not valid.
    """
    if color not in COLOR_CODES:
        raise ValueError(f"Invalid color '{color}'. Valid options are: {', '.join(COLOR_CODES.keys())}")

    color_code = COLOR_CODES[color]
    reset_code = COLOR_CODES["reset"]

    # Print the text with the selected color and reset the color afterward
    print(f"{color_code}{text}{reset_code}")
