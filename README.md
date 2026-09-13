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
- `scripts/` – scripts used in the workflow
- `guides/` – supporting documentation from the course template
- `.github/` – GitHub Actions workflows
- `environment.yml` – software environment information
- `pyproject.toml` – Python project configuration

## Setup

The project environment is currently defined in `environment.yml`.

Installation and setup instructions for Napari, nnU-Net, and other required
tools will be added to this README as the project progresses.

## Current Status

For Milestone 1, the repository currently includes:

- the initial GitHub repository setup
- the project proposal
- the planned project workflow
- the initial software environment and repository structure

## Next Step

The next step is to finalize the segmentation class definitions and begin
creating representative ground truth annotations in Napari.

## Related Work

The [nnUNet4SoilXrayCT repository](https://github.com/MaxPhal/nnUNet4SoilXrayCT)
repository provides an example of using nnU-Net for soil X-ray CT segmentation and will be used as a reference during this project. The goal here is not to completely reproduce that work, but to apply and evaluate the workflow using the current dataset with a different set of segmentation classes.