# mlbrecaps

A Python package for downloading Major League Baseball game highlights based on team and date.

### Installation

```
pip install mlbrecaps
```

Usage
The mlbrecaps package provides a simple function highlight_generator to download game highlights for a specified Major League Baseball team and date.

### Basic Python Example:

```
from mlbrecaps import scripts, Team, Date

# Download highlights for the Minnesota Twins game on October 3rd, 2023

highlights = scripts.get_highlights(Team("MIN"), Date(10, 3, 2023))

# Handle all the highlights to a folder
highlights.download("/path/to/folder/", verbose=True)
```

### Example in Google Colab

[Link to Google Colab](https://colab.research.google.com/drive/1QdHi8rVwSTW14DeO-GAqwc5nU8v6EqH-?usp=sharing)

### Run directly from the terminal

If you have the mlbrecaps package installed, you can use the following command to download highlights directly from the terminal:

```
python -m mlbrecaps
```

This command will prompt you to enter the team three-letter abbreviation, game date, and path to a videos download directory for the desired highlights.

### Examples

More examples are avaliable on [Github](https://github.com/MrRedwing/MLB-Recaps).

### Development

This package is under active development. Feel free to contribute by submitting pull requests!

### Contributing

All contributions are welcomed to improve the mlbrecaps package. To contribute simply submit a pull request.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
