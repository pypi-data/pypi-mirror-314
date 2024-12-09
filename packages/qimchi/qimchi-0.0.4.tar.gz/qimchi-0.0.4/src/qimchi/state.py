import json

from pathlib import Path
from dataclasses import dataclass, field

# Local imports
from qimchi.logger import logger


# Default vars
DATA_REFRESH_INTERVAL = 1_000  # ms

# Default filter options
DEFAULT_SAVGOL_OPTS = {
    "window": 5,
    "polyorder": 2,
}

DEFAULT_SMA_WINDOW = 5

DEFAULT_NORM_OPTS = {
    "axis": "z",
    "axis_idx": 0,
}

DEFAULT_GC_OPTS = {
    "gamma": 2.0,  # skimage default is 1.0
    "gain": 2.0,  # skimage default is 1.0
}

DEFAULT_LC_OPTS = {
    "gain": 1.0,
    "inv": False,
}

DEFAULT_SC_OPTS = {
    "cutoff": 0.5,
    "gain": 10.0,
}

DEFAULT_POLYFIT_OPTS = {
    "deg": 5,
    "window": [0, 1],  # TODOLATER: window
}

# TODOLATER: Can allow specifying the range to scale to.
# TODOLATER: See: https://scikit-image.org/docs/stable/api/skimage.exposure.html#skimage.exposure.rescale_intensity
DEFAULT_RI_OPTS = {
    "in_range": "image",  # skimage default is "image"
}

DEFAULT_ROTA_OPTS = {
    "angle": 0,
}

# TODO: Sort this out @s.anupam
DEFAULT_HMAP_COLSCALE = "viridis"
DEFAULT_LINE_MODE = "lines+markers"
DEFAULT_LINE_COLOR = "red"
DEFAULT_LINE_WIDTH = 2
DEFAULT_LINE_OPACITY = 1.0
DEFAULT_LINE_DASH = "solid"
DEFAULT_LINE_SHAPE = "linear"
DEFAULT_SPLINE_SMOOTHING = 0.0
DEFAULT_MARKER_COLOR = "blue"
DEFAULT_MARKER_SIZE = 5
DEFAULT_MARKER_OPACITY = 1.0
LINE_MODE_OPTS = [
    {"label": "Lines", "value": "lines"},
    {"label": "Markers", "value": "markers"},
    {"label": "Lines + Markers", "value": "lines+markers"},
]
LINE_COLOR_OPTS = MARKER_COLOR_OPTS = GRID_COLOR_OPTS = TICK_COLOR_OPTS = [
    # Some random colors # TODO: Sort this out @s.anupam
    "red",
    "blue",
    "green",
    "purple",
    "orange",
    "black",
    "brown",
    "gray",
]
LINE_DASH_OPTS = [
    {"label": "Solid", "value": "solid"},
    {"label": "Dash", "value": "dash"},
    {"label": "Dot", "value": "dot"},
    {"label": "Long Dash", "value": "longdash"},
    {"label": "Dash Dot", "value": "dashdot"},
    {"label": "Long Dash Dot", "value": "longdashdot"},
]
LINE_SHAPE_OPTS = [
    {"label": "Linear", "value": "linear"},
    {"label": "Spline", "value": "spline"},
    {"label": "Step", "value": "hv"},
    {"label": "Step Before", "value": "hvh"},
    {"label": "Step After", "value": "vhv"},
]
DEFAULT_MARKER_SYMBOL = "diamond-tall-open"
MARKER_SYMBOL_OPTS = [
    {"label": "Circle", "value": "circle"},
    {"label": "Square", "value": "square"},
    {"label": "Diamond", "value": "diamond"},
    {"label": "Cross", "value": "cross"},
    {"label": "X", "value": "x"},
    {"label": "Triangle-Down", "value": "triangle-down"},
    {"label": "Triangle-Left", "value": "triangle-left"},
    {"label": "Triangle-Right", "value": "triangle-right"},
    {"label": "Triangle-Up", "value": "triangle-up"},
    {"label": "Diamond-Tall", "value": "diamond-tall"},
    {"label": "Diamond-Tall-Open", "value": "diamond-tall-open"},
    {"label": "Diamond-Wide", "value": "diamond-wide"},
    {"label": "Diamond-Wide-Open", "value": "diamond-wide-open"},
    {"label": "Hourglass", "value": "hourglass"},
    {"label": "Hourglass-Open", "value": "hourglass-open"},
]
# Grid & tick options
DEFAULT_AXIS_TYPE = "linear"
DEFAULT_GRID_COLOR = DEFAULT_TICK_COLOR = "gray"
DEFAULT_SHOWGRID = True
DEFAULT_NTICKS = 5
DEFAULT_GRID_WIDTH = 1  # px
DEFAULT_GRID_DASH = "solid"
AXIS_TYPE_OPTS = [
    {"label": "Linear", "value": "linear"},
    {"label": "Log", "value": "log"},
]
GRID_DASH_OPTS = [
    {"label": "Solid", "value": "solid"},
    {"label": "Dash", "value": "dash"},
    {"label": "Dot", "value": "dot"},
    {"label": "Long Dash", "value": "longdash"},
    {"label": "Dash Dot", "value": "dashdot"},
    {"label": "Long Dash Dot", "value": "longdashdot"},
]
DEFAULT_TICK_WIDTH = 1  # px
DEFAULT_TICK_LENGTH = 5  # px
DEFAULT_TICK_ANGLE = 0  # deg

# Default filter options
DEFAULT_SAVGOL_WINDOW_LENGTH = 5
DEFAULT_SAVGOL_POLYORDER = 2


class JSONStateEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for the JSONState dataclass.

    """

    def default(self, obj):
        if isinstance(obj, Path):
            return str(obj.resolve())
        return super().default(obj)


class JSONStateDecoder(json.JSONDecoder):
    """
    Custom JSON decoder for the JSONState dataclass.

    """

    def __init__(self):
        super().__init__(object_hook=self.object_hook)

    def object_hook(self, obj):
        if "state_file" in obj:
            obj["state_file"] = Path(obj["state_file"])
        if "dataset_path" in obj:
            obj["dataset_path"] = Path(obj["dataset_path"])
        return obj


@dataclass
class JSONState:
    # FS stuff
    state_file: Path = Path(__file__).parent / "state.json"
    logger.warning(f"State file: {state_file}")

    # selector.py
    dataset_path: Path = Path("")
    dataset_type: str = ""
    measurement_path: Path = Path("")
    measurement_last_fmt: str = ""

    # datasets.py
    wafer_id: str = ""
    device_type: str = ""
    device_id: str = ""
    measurement_type: str = ""
    measurement: str = ""

    # NOTE: Specs for plot_states
    # 1. No data stored, only things like:
    #   1.1 deps (list) - List of dependent variables
    #   1.2 indeps (list) - List of independent variables
    #   1.3 theme (dict) - Not all keys are applicable to all plots
    # 2. `slider` config (dict)
    # 3. `filters_order` (list) - List of filters applied in order
    # 4. `filters_opts` (dict) - Dict of filters with options
    # 5. `plots_menu` (list) - Open/Close State etc. of the options in the plots-menu
    # And more stuff. Check state.json.
    plot_states: dict[str, dict] = field(default_factory=dict)

    def load_state(self) -> dict:
        """
        Loads the state from the local JSON file if it exists.
        Otherwise, creates the state from the default values.

        """
        state_file = self.state_file
        if state_file.exists():
            try:
                with open(state_file, "r") as f:
                    self.__dict__.update(json.load(f, cls=JSONStateDecoder))
                logger.debug("State loaded from disk.")
            except json.JSONDecodeError:
                logger.warning(
                    "Error decoding state. Backing up current file and creating a new state file..."
                )
                # Rename the current state file
                try:
                    state_file.rename(state_file.with_suffix(".json.bak"))
                except FileExistsError:
                    logger.error(
                        f"Backup file {state_file.with_suffix('.json.bak')} already exists and will be overwritten."
                    )
                    # Overwrite the existing backup file
                    state_file.with_suffix(".json.bak").unlink()
                    state_file.rename(state_file.with_suffix(".json.bak"))

                # Create a new state file
                self.save_state()
                logger.warning(
                    f"New state file created at {state_file}.\nOld state file backed up at {state_file}.bak."
                )

                # Load the new state file # NOTE: No recursion here
                self.load_state()

            except Exception as err:
                logger.error(f"Error loading state: {err}", exc_info=True)
                exit()
        else:
            logger.debug("State loaded anew.")
        return self.__dict__

    def save_state(self) -> None:
        """
        Saves the given state to the local JSON file.

        """
        data = self.__dict__

        state_file = self.state_file
        with open(state_file, "w") as f:
            json.dump(data, f, indent=4, cls=JSONStateEncoder)


# Load the state from disk or create a new one
_state = JSONState()
_state.load_state()
