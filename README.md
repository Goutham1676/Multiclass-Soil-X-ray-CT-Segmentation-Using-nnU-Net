# Multiclass Soil X-ray CT Segmentation Using nnU-Net

This project focuses on multiclass segmentation of soil X-ray CT images using
nnU-Net. The classes of interest are soil matrix, stones, organic matter,
roots, biopores, and other pores.

The goal is to build a workflow that starts with manual annotation of ground
truth labels and continues through nnU-Net training, prediction, and evaluation.

## Project Workflow

The planned workflow is:

CT images → annotation in Napari → manual annotation review →
nnU-Net data preparation → preprocessing → training → prediction → evaluation

Napari will be used to create the ground truth annotations. These annotations
will be manually reviewed before they are used for training.

nnU-Net will be used for multiclass segmentation, and the segmentation results
will mainly be evaluated using Dice scores for each class.

## Repository Structure

- `paper/` – project proposal and later manuscript files
- `soilct_segmentation/` – Python code for the project
- `guides/` – supporting documentation from the course template
- `.github/` – GitHub Actions workflows
- `environment.yml` – software environment information
- `pyproject.toml` – Python project configuration

## Setup

The project environment is defined in `environment.yml`.

Create the Conda environment from the repository root:

`conda env create -f environment.yml`

Activate the environment:

`conda activate soilct`

Then start JupyterLab:

`jupyter lab`

## Current Status

### Milestone 1

Milestone 1 established:

- the initial GitHub repository
- the project proposal
- the planned project workflow
- the initial software environment
- the initial repository structure

### Milestone 2

The current prototype now includes:

- 3D TIFF stack loading
- representative middle-slice selection
- CT intensity inspection
- optional user-controlled normalization
- Otsu-based matrix initialization
- interactive lower and upper threshold refinement
- multiclass annotation definitions through `dataset_info.json`
- 3D annotation-volume creation
- automatic reloading of existing annotations
- interactive annotation in Napari
- manual saving with `Ctrl+S`
- automatic saving when Napari closes
- reusable Python modules with docstrings
- a simplified user-facing notebook
- a detailed prototype/reference notebook
- automated tests using `pytest`

## Next Steps

The next stage of the project will focus on preparing completed ground truth
annotations for nnU-Net training.

Planned next steps include:

1. Complete and review representative multiclass annotations.
2. Convert CT images and labels into the nnU-Net dataset format.
3. Configure the nnU-Net dataset.
4. Run nnU-Net preprocessing.
5. Train the multiclass segmentation model.
6. Generate predictions on held-out CT images.
7. Evaluate segmentation performance using class-specific Dice scores.

## Related Work

The [nnUNet4SoilXrayCT repository](https://github.com/MaxPhal/nnUNet4SoilXrayCT)
provides an example of using nnU-Net for soil X-ray CT segmentation and will be
used as a reference during this project.

The goal here is not to completely reproduce that work, but to apply and
evaluate the workflow using the current dataset with a different set of
segmentation classes.