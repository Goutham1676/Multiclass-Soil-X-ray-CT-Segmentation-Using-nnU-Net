# Multiclass Soil X-ray CT Segmentation Using nnU-Net

This project focuses on multiclass segmentation of soil X-ray CT images using
nnU-Net. The classes of interest are soil matrix, stones, organic matter,
roots, biopores, and other pores.

The goal is to develop a workflow that starts with manual annotation of
ground truth labels and continues through nnU-Net training, prediction, and
evaluation.

## Project Workflow

The planned workflow is:

CT images → annotation in Napari → manual annotation review →
nnU-Net data preparation → preprocessing → training → prediction → evaluation

Napari will be used to create the ground truth annotations. The annotations
will be manually reviewed before they are used for training.

nnU-Net will be used for multiclass segmentation, and segmentation performance
will mainly be evaluated using Dice scores for each class.

## Repository Structure

- `paper/` – project proposal and later manuscript files
- `soilct_segmentation/` – Python code for the project
- `scripts/` – scripts used in the workflow
- `guides/` – supporting documentation from the course template
- `.github/` – GitHub Actions workflows
- `environment.yml` – software environment
- `pyproject.toml` – Python project configuration

## Current Status

Milestone 1 includes:
- initial GitHub repository setup
- project proposal
- project workflow
- initial software environment and repository structure

## Next Step

The next planned step is to finalize the segmentation class definitions and
begin creating representative ground truth annotations in Napari.

## Related Work

Existing work has demonstrated the use of nnU-Net for soil X-ray CT
segmentation. The `nnUNet4SoilXrayCT` repository will be used as a reference
while developing this project. This project is not intended to reproduce that
implementation, but to develop and evaluate the workflow for the current
dataset and segmentation classes.