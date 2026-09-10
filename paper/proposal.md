# Multiclass Soil X-ray CT Segmentation Using nnU-Net

By Goutham Thotakuri



## Summary

X-ray computed tomography (CT) makes it possible to examine the internal structure of soil in three dimensions without physically disturbing the sample. However, separating different soil components from CT images can be difficult because several materials may have similar grayscale intensities.

This project will investigate using nnU-Net for multiclass segmentation of soil X-ray CT images. The initial classes of interest are soil matrix, stones, organic matter, roots, biopores, and other pores. The goal is to develop a reproducible workflow that prepares annotated CT data for nnU-Net, trains a segmentation model, applies the trained model to unseen images, and evaluates the resulting segmentations quantitatively.

The project will use nnU-Net as an existing deep-learning framework rather than developing a new neural-network architecture.



## Overview

Soil X-ray CT images contain valuable information about both soil and pore components, as well as biological features such as roots and other organic material. Identifying these components is important for studying how roots interact with soil structure and how different physical and biological features are distributed within the soil. The main question this project looks into is: How well can nnU-Net (not new neural network) be used for multiclass segmentation of soil X-ray CT images into matrix, stones, organic matter, roots, biopores, and other pores?



## Software or Project Description

This project aims to develop a workflow for annotating ground truth labels, preparing, training, and evaluating multiclass soil X-ray CT data.

Representative CT images will be annotated in Napari (open-source, interactive multi-dimensional image viewer designed for Python) using the defined classes: soil matrix, stones, organic matter, roots, biopores, and other pores. Since these annotations will be used as ground truth, they will be manually reviewed to make sure the labels are accurate and consistent. The annotated images and label masks will then be checked for matching dimensions, correct file pairing, and valid class labels before being prepared for nnU-Net.

The workflow will then include nnU-Net preprocessing, model training, prediction, and quantitative evaluation of the segmentation results.



## Project Goals and Timeline

The short-term goal is to set up the project workflow, define the segmentation classes, and begin creating ground truth annotations in Napari. The annotated images will then be prepared in a format that can be used by nnU-Net.



September

\- Set up the GitHub repository and software environment

\- Define the segmentation classes and label values

\- Begin annotating representative soil CT images in Napari

\- Check the annotations manually for labeling quality

\- Prepare the initial dataset for nnU-Net



October

\- Complete an initial set of training and validation images

\- Run nnU-Net preprocessing

\- Train an initial multiclass segmentation model



November

\- Run predictions on images that were not used for training

\- Evaluate the segmentation results for each class

\- Identify classes that are difficult to separate and make improvements where (if) possible



December

\- Finalize the workflow

\- Complete the documentation

\- Summarize the model results

\- Prepare the final report and presentation



By the end of the semester, the goal is to have a working workflow that goes from CT image annotation to multiclass segmentation and evaluation.



## Methods and Workflow

The project will use soil X-ray CT images as the input data. Ground truth labels will be created in Napari for soil matrix, stones, organic matter, roots, biopores, and other pores. The annotations will be manually reviewed before they are used for model training.

The basic workflow will be:

CT images → annotation in Napari → manual annotation review → label and image checks → nnU-Net data preparation → preprocessing → training → prediction → evaluation

I will use Python for data preparation, validation, and evaluation. nnU-Net will be used for the multiclass segmentation model.

Segmentation performance will mainly be evaluated using Dice scores for each class. GitHub will be used for version control, and the repository will include documentation and environment information for the workflow.



## Anticipated Challenges

A major challenge is that some soil components may have similar grayscale values, which can make both manual annotation and model segmentation difficult. Another challenge is creating accurate ground truth labels, since the quality of the annotations will directly affect model training and evaluation.

The 3D CT images are also large, so annotation and model training may take considerable time and computing resources. To keep the project manageable, the initial work will focus on a smaller representative dataset.



## Expected Outcomes

By the end of the semester, I expect to have a working workflow for annotating soil X-ray CT images, preparing the data for nnU-Net, training a multiclass segmentation model, generating predictions, and evaluating the results.

I feel the success of this project lies in producing multiclass segmentations on 3D X-ray CT images and whether the segmentation performance can be evaluated using Dice scores for each class.

The final repository will include the workflow, environment information, and documentation needed to understand and reproduce the main steps of the project.

