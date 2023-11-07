# Run Executable
To run the executebale in root folder the command: 

`./dist/main`

# Run Tests
To excute the tests run in root folder:

`make build-test`

`make test`

# Developing

## Environment

[Python 3.10.12](https://www.python.org/downloads/) and [Ubuntu 22.04.3 LTS](https://releases.ubuntu.com/)

Install the requirements.txt:

`pip install -r ./requirements.txt`

## Running Code

Run the game by typing in root folder the command:

`python main.py`

Run the tests by typing in root folder the command:

`python -m pytest -l --color=yes -p no:cacheprovider`

# Create Executable
To package everything into a single executable run in root folder the command:

`pyinstaller --onefile main.py`

# Enabling Extra Features
If you wish to control the bird with arrow keys go to `./configs/game_settings.py` and set `BIRD_MOVEMENT` to any string, i.e. `"controllable"` (default is `"random"`).

If you wish to generate randomly `N` pointees then go to `main.py` and replace `pointees = pnt.generate_pointees()` with `pointees = pnt.generate_pointees_randomly(N)`.