# h5visualizer

Welcome to **h5visualizer**! This is a Python tool that allows you to visualize Keras model layers as cubes in 3D. It's a simple yet cool way to get a 3D representation of your Keras model, helping you understand its structure better. You can adjust the scale of the visualization, and the script supports both direct command-line usage and interactive file input.

## Features:
- Visualizes Keras models (saved as `.h5` files) in 3D.
- You can adjust the scale of the model layers with the `--scale` argument (optional).
- Easy-to-use, just clone, install, and run.

## Installation

### Clone the Repository:
First, clone this repository to your local machine:

```bash
git clone https://github.com/krazykarthik2/h5visualizer.git
cd h5visualizer
```
Install the Package:
Next, install the package in editable mode:

```bash
pip install --editable .
```

### This will install the tool and make it globally accessible, so you can use it anywhere on your machine.

## Usage
Once everything is set up, you can run the visualizer by providing the path to your .h5 model file and optionally adjusting the scale. Here's the basic syntax:

```bash
python -m h5visualizer --filepath "path_to_your_model.h5" --scale 0.1
--filepath: Path to the .h5 Keras model file (required).
--scale: Scale factor for the 3D model layers (optional, default is 0.1).
```
If you don’t provide the scale, it will use the default value of 0.1. You can easily change this to zoom in or out the model layers.

If you don’t pass the file path via the command line, the tool will prompt you to enter it interactively.

Example:
```bash
python -m h5visualizer --filepath "path_to_model.h5" --scale 0.2
```
This will load the model from "path_to_model.h5", visualize it with a scale of 0.2, and show it in 3D!
