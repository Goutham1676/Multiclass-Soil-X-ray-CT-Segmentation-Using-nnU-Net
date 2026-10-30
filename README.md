# Multiclass Soil X-ray CT Segmentation Using nnU-Net

This project focuses on multiclass segmentation of soil X-ray CT images using
nnU-Net. The classes of interest are soil matrix, stones, organic matter,
roots, biopores, and other pores.

The goal is to build a workflow that starts with manual annotation of ground
truth labels and continues through nnU-Net training, prediction, and evaluation.

## Project Workflow

The current workflow focuses on preparing soil X-ray CT images and creating multiclass annotations.

1. Load, inspect, and normalize the CT stack.
2. Use Otsu thresholding and an interactive slider to select the initial soil matrix.
3. Open the image in Napari for manual annotation and refinement.
4. Save the annotations as a 3D TIFF stack for continued editing.

Existing annotations are loaded directly without repeating the threshold selection.

The next phase will involve preparing the annotated images for nnU-Net training, prediction, and evaluation using class-wise Dice scores.

## Repository Structure

- `paper/` – project proposal and later manuscript files
- `soilct_segmentation/` – Python code for the project
- `environment.yml` – software environment information
- `pyproject.toml` – Python project configuration


## Setup

Clone the repository and navigate to the project folder.

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate soilct
```

Start JupyterLab:

```bash
jupyter lab
```


The `00_prototype_development_reference.ipynb` notebook shows the annotation workflow step by step, including the code used for preprocessing, threshold selection, and Napari annotation.

The `01_soil_ct_annotation_workflow.ipynb` notebook provides a simpler workflow using the functions organized in `soilct_segmentation/`.



## Testing and Validation

Before running pytest, make sure the `soilct` environment is activated. Run these commands from the repository root:

`conda activate soilct`

Run the tests using either command:

`python -m pytest`

or

`make test`

- **test_imports.py** checks that the required libraries can be imported.

- **test_pytest.py** tests core annotation functions and selected invalid inputs.

Expected result: 11 tests passed.

I manually checked the annotation workflow using the input CT stack. Edits made in Napari were saved and remained present after closing and reopening the workflow.
To repeat this check, run 01_soil_ct_annotation_workflow.ipynb, edit an annotation, save with Ctrl+S or close the Napari window, and reopen it to confirm that the edit remains.

### Assumptions and Limitations

- Zero-valued voxels are treated as background during normalization and Otsu threshold calculation.

- Initial matrix labels are based on intensity thresholds and require manual review.

- Workflow validation currently covers the input CT stack. nnU-Net training, prediction, and segmentation accuracy have not yet been evaluated.


## Current Status

### Milestone 1

Milestone 1 established:

- the initial GitHub repository
- the project proposal
- the planned project workflow
- the initial software environment
- the initial repository structure

### Milestone 2

Milestone 2 established the initial working environment for soil X-ray CT segmentation and annotation. The main outcomes are:

- created the preprocessing environment for loading, inspecting, and normalizing a subset of 3D soil X-ray CT images
- developed an initial segmentation workflow using Otsu thresholding with user-adjustable thresholds
- integrated a Napari-based interface for multiclass annotation and manual refinement
- added support for saving and reloading annotation volumes for continued editing
- organized the workflow into reusable Python modules with a simplified notebook interface
- added basic automated tests and validated the workflow through GitHub Actions

### Milestone 3

For this milestone, I added tests to check that the required libraries can be imported. All 11 tests passed using both pytest and `make test`. 
I also checked that edits made in Napari were saved and still present after reopening the annotation. 
Instructions for running the tests and the current assumptions and limitations are included above.
These results will support the testing and software quality discussion in the final report.

### Milestone 4

For this milestone, I updated the README with setup instructions, annotation steps, and input and output details. I also reviewed the Python docstrings and notebook documentation.

All 11 tests passed using make check, and Ruff found no issues.

These updates will help others run the workflow and document the methods in the final JOSS-style paper.

## Next Steps

The next phase will focus on:

- completing and reviewing representative multiclass annotations
- preparing CT images and labels in nnU-Net format
- training and evaluating the multiclass segmentation model

## Related Work

The [nnUNet4SoilXrayCT repository](https://github.com/MaxPhal/nnUNet4SoilXrayCT)
provides an example of using nnU-Net for soil X-ray CT segmentation and will be
used as a reference during this project.

The goal here is not to completely reproduce that work, but to apply and
evaluate the workflow using the current dataset with a different set of
segmentation classes.