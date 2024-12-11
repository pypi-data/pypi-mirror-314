# HopfieldModel

**Author**: Ashish Phal

**BIOEN537: Computational Systems Biology. University of Washington, Seattle.**

A Python package designed to model single-cell data using Hopfield networks, enabling energy-based analysis of cellular transitions.

**License**: MIT  
**Current version**: 1.0.0  
**Last updated**: 2024-12-10  

## Background

Understanding cellular differentiation and transitions is crucial in developmental biology and regenerative medicine. Hopfield networks provide a framework for modeling these processes by representing gene expression states as memory patterns and computing energy landscapes that describe transitions between cell states.

The `HopfieldModel` package facilitates these analyses with tools to normalize gene expression data, select highly variable genes, compute cell-specific Hopfield energy, and visualize cellular transitions. The package is intended for researchers and students working with single-cell RNA sequencing data, offering a streamlined and accessible approach to study cell states and transitions.

---

## Installation

### **Package Dependencies**

This package requires Python 3.7 or higher and the following Python packages:
- `numpy`: Numerical computing
- `matplotlib`: Data visualization
- `scikit-learn`: Machine learning and PCA analysis
- `scanpy`: Single-cell analysis
- `seaborn`: Statistical data visualization
- `scipy`: Scientific computing

These dependencies will be automatically installed when you install the package using pip.

### **Installing the Package**

To install the package, run the following command:

```bash
pip install HopfieldModel
```

## Example Visualizations

### 1. Transition Energy Plot
This plot shows the transition of cells between two specified types along PC1, with their Hopfield energy.

![Transition Energy Plot](docs/trajectory.png)

---

### 2. PCA Visualization
Cells are projected into PCA space, with each point colored by its Hopfield energy. Different colors represent distinct cell types.

![PCA Plot](docs/energy_pca.png)

---

### 3. Gene Transition Matrix
This heatmap displays the gene state changes between two cell types, clustered hierarchically. The clustering highlights key genes involved in the transition.

![Gene Transition Matrix](docs/gene_matrix.png)

---

### 4. Hopfield Energy Boxplot
This boxplot shows the distribution of Hopfield energy across different cell types, enabling a comparison of differentiation potency.

![Energy Boxplot](docs/boxplot.png)


