import argparse

# from pathlib import Path # TODOLATER:

# Local imports
from .app import app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8050)
    parser.add_argument("-d", "--debug", type=bool, default=True)
    # parser.add_argument("-r", "--reset", type=bool, default=False)
    args = parser.parse_args()

    # if args.reset:
    #     # Reset the state
    #     print("Resetting the state...")
    #     Path("state.json").unlink(missing_ok=True)

    app.run(debug=args.debug, port=args.port)
