## Reflection

The exercises in this assignment helped me understand how analytical models are built, compared, and evaluated. Linear regression showed me how adjusted \\(R^2\\), p-values, and residual plots can be used together to judge model performance. Comparing the full and reduced models also showed that adding more variables does not always improve a model or make it easier to interpret. I also found StackGP useful because it showed how symbolic regression can search for an equation instead of starting with a fixed model form. With the synthetic data, StackGP recovered almost the same equation that was used to generate the response, while the real infant mortality data produced a more complicated model. This showed me that model accuracy and model interpretability both need to be considered when working with real data.

&#x09;These ideas are useful for my nnU-Net soil µCT segmentation project. Even though my project is based on image segmentation rather than regression, I still need to compare model performance carefully and identify where the model performs poorly. For example, I can use per-class Dice scores to evaluate how well nnU-Net segments soil matrix, stones, organic matter, roots, biopores, and other pores. Dice can be calculated as: 

&#x09;		\\\[

\\text{Dice}=\\frac{2TP}{2TP+FP+FN}

\\]

&#x09;Where \\(TP\\) is the number of correctly classified voxels for a class, \\(FP\\) is the number of voxels incorrectly classified as that class, and \\(FN\\) is the number of voxels from that class that were missed. I can compare Dice scores across different preprocessing steps or training settings to see whether those changes actually improve segmentation. Visual inspection of the predicted masks will also be important because a single score may not show where specific classes are being misclassified. Overall, this assignment helped me think more carefully about model evaluation, comparison, interpretation, and validation.

