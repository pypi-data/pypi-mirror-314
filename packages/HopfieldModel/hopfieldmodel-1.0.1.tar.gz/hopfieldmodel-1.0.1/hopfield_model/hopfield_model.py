import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import scanpy as sc
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import linregress
from scipy.cluster.hierarchy import linkage, leaves_list

class HopfieldModel:
    def __init__(self, data, cell_types, gene_names):
        """
        Initialize the Hopfield network with the gene expression data.

        Parameters:
        data (numpy.ndarray): A 2D array where rows represent cells and columns represent gene expression counts.
        cell_types (numpy.ndarray): Array of cell type labels for each cell.
        """
        self.data = data
        self.cell_types = cell_types
        self.gene_names = gene_names
        self.normalized_data = None
        self.hvgs = None  # Reduced dataset of highly variable genes
        self.weight_matrices = None  # List of weight matrices, one per cell

    def normalize_data(self):
        """
        Perform Z-score normalization on the input data.
        """
        if self.data.size == 0:
            raise ValueError("Input data is empty. Cannot normalize.")
            
        scaler = StandardScaler()
        self.normalized_data = scaler.fit_transform(self.data)

    def select_highly_variable_genes(self, top_percent=5):
        """
        Select the top highly variable genes based on variance.

        Parameters:
        top_percent (int): The percentage of genes to select based on variance.

        Returns:
        numpy.ndarray: A reduced dataset containing only the highly variable genes.
        """
        if self.normalized_data is None or self.normalized_data.size == 0:
            raise ValueError("Normalized data is empty. Cannot select highly variable genes.")

        variances = np.var(self.normalized_data, axis=0)
        if not np.any(variances > 0):
            raise ValueError("All genes have zero variance. Cannot select highly variable genes.")

        cutoff = np.percentile(variances, 100 - top_percent)
        self.hvgs = self.normalized_data[:, variances >= cutoff]
        if self.hvgs.shape[1] == 0:
            raise ValueError("No highly variable genes found with the given threshold.")

        self.selected_genes = np.array(self.gene_names)[variances >= cutoff]

    def construct_weight_matrices(self):
        """
        Construct a Hopfield network weight matrix for each cell.
        """
        if self.hvgs is None or self.hvgs.size == 0:
            raise ValueError("Highly variable genes are not selected. Cannot construct weight matrices.")

        n_cells, n_genes = self.hvgs.shape
        self.weight_matrices = []

        for cell in self.hvgs:
            weight_matrix = np.zeros((n_genes, n_genes))
            for i in range(n_genes):
                for j in range(n_genes):
                    if i != j:
                        weight_matrix[i, j] = cell[i] * cell[j]
            self.weight_matrices.append(weight_matrix)

    def compute_hopfield_energy(self, cell_index):
        """
        Compute the Hopfield energy for a specific cell.

        Parameters:
        cell_index (int): Index of the cell to compute energy for.

        Returns:
        float: The energy of the cell.
        """
        if self.weight_matrices is None or len(self.weight_matrices) == 0:
            raise ValueError("Weight matrices are not constructed. Cannot compute Hopfield energy.")
            
        weight_matrix = self.weight_matrices[cell_index]
        state = (self.hvgs[cell_index] > 0).astype(int)  # Use reduced dataset
        energy = -0.5 * np.sum(weight_matrix * np.outer(state, state))
        return energy

    def plot_grouped_energies(self, save_path="grouped_energies.png"):
        """
        Plot the average Hopfield energy grouped by cell types as a boxplot.
        """
        unique_cell_types = np.unique(self.cell_types)
        grouped_energies = []

        for cell_type in unique_cell_types:
            indices = np.where(self.cell_types == cell_type)[0]
            energies = [self.compute_hopfield_energy(i) for i in indices]
            grouped_energies.append(energies)

        plt.boxplot(grouped_energies, labels=unique_cell_types, patch_artist=True, boxprops=dict(facecolor='skyblue'))
        plt.xticks(rotation=45)
        plt.xlabel("Cell Types")
        plt.ylabel("Hopfield Energy")
        plt.title("Hopfield Energy by Cell Type")
        plt.savefig(save_path)
        plt.show()


    def plot_energy_pca(self, save_path="energy_pca.png"):
            """
            Plot cells in PCA space, colored by their Hopfield energy with distinct colors for each cell type.
            """
            # Compute energies for all cells
            energies = [self.compute_hopfield_energy(i) for i in range(self.hvgs.shape[0])]

            # Perform PCA on the highly variable genes
            pca = PCA(n_components=2)
            pca_coords = pca.fit_transform(self.hvgs)

            # Normalize energies for color scaling
            normalized_energies = (energies - np.min(energies)) / (np.max(energies) - np.min(energies))

            # Define a colormap for each cell type
            unique_cell_types = np.unique(self.cell_types)
            cell_type_colors = sns.color_palette("husl", len(unique_cell_types))
            cell_type_cmaps = {
                cell_type: LinearSegmentedColormap.from_list(f"{cell_type}_cmap", [(1, 1, 1), color])
                for cell_type, color in zip(unique_cell_types, cell_type_colors)
            }

            # Create a scatter plot
            plt.figure(figsize=(10, 8))
            for cell_type, color in zip(unique_cell_types, cell_type_colors):
                indices = np.where(self.cell_types == cell_type)[0]
                cmap = cell_type_cmaps[cell_type]
                plt.scatter(
                    pca_coords[indices, 0],
                    pca_coords[indices, 1],
                    c=normalized_energies[indices],
                    cmap=cmap,
                    label=cell_type,
                    alpha=0.7
                )

            plt.xlabel("PC1")
            plt.ylabel("PC2")
            plt.title("PCA of Cells Colored by Hopfield Energy")
            plt.legend(title="Cell Types")
            plt.colorbar(label="Normalized Energy")
            plt.savefig(save_path)
            plt.show()

    def plot_transition_energy(self, cell_type_1, cell_type_2, save_path="transition_energy.png"):
        """
        Plot cells along PC1 with their Hopfield energy for two specified cell types.

        Parameters:
        cell_type_1 (str): The first cell type.
        cell_type_2 (str): The second cell type.
        """
        # Get indices for the specified cell types
        indices_1 = np.where(self.cell_types == cell_type_1)[0]
        indices_2 = np.where(self.cell_types == cell_type_2)[0]
        indices = np.concatenate([indices_1, indices_2])

        # Compute energies for the selected cells
        energies = [self.compute_hopfield_energy(i) for i in indices]

        # Perform PCA on the highly variable genes
        pca = PCA(n_components=2)
        pca_coords = pca.fit_transform(self.hvgs[indices])

        # Extract PC1 and sort by it
        pc1 = pca_coords[:, 0]
        sorted_indices = np.argsort(pc1)
        pc1 = pc1[sorted_indices]
        energies = np.array(energies)[sorted_indices]

        # Fit a line to the data
        slope, intercept, _, _, _ = linregress(pc1, energies)
        line = slope * pc1 + intercept

        # Plot
        plt.figure(figsize=(10, 6))
        scatter = plt.scatter(pc1, energies, c=energies, cmap="coolwarm", edgecolor="none")
        plt.plot(pc1, line, color="black", linestyle="--", label="Best Fit")
        plt.colorbar(scatter, label="Hopfield Energy")
        plt.xlabel("PC1")
        plt.ylabel("Hopfield Energy")
        plt.title(f"Transition from {cell_type_1} to {cell_type_2}")
        plt.legend()
        plt.savefig(save_path)
        plt.show()

    def plot_gene_transition_matrix(self, cell_type_1, cell_type_2, save_path="gene_transition_matrix.png"):
        """
        Plot a gene transition matrix showing state changes between two cell types.

        Parameters:
        cell_type_1 (str): The first cell type.
        cell_type_2 (str): The second cell type.

        Returns:
        list, list: Top 5 genes associated with each cell type.
        """
        # Get indices for the specified cell types
        indices_1 = np.where(self.cell_types == cell_type_1)[0]
        indices_2 = np.where(self.cell_types == cell_type_2)[0]

        # Average states for each cell type
        avg_state_1 = np.mean((self.hvgs[indices_1] > 0).astype(int), axis=0)
        avg_state_2 = np.mean((self.hvgs[indices_2] > 0).astype(int), axis=0)

        # Create a transition matrix
        transition_matrix = np.vstack([avg_state_1, avg_state_2])

        # Perform hierarchical clustering
        linkage_matrix = linkage(transition_matrix.T, method="ward")
        ordered_indices = leaves_list(linkage_matrix)

        # Reorder transition matrix based on clustering
        clustered_matrix = transition_matrix[:, ordered_indices]

        # Ensure top genes for each cell type are arranged in expected order
        top_genes_1 = self.selected_genes[np.argsort(avg_state_1)[-5:][::-1]].tolist()
        top_genes_2 = self.selected_genes[np.argsort(avg_state_2)[-5:][::-1]].tolist()

        # Plot
        plt.figure(figsize=(8, 6))
        sns.heatmap(clustered_matrix, cmap="Blues", cbar=True, annot=False, xticklabels=False, yticklabels=[cell_type_1, cell_type_2])
        plt.title("Gene Transition Matrix")
        plt.xlabel("Genes")
        plt.ylabel("Cell Types")
        plt.savefig(save_path)
        plt.show()

        return top_genes_1, top_genes_2