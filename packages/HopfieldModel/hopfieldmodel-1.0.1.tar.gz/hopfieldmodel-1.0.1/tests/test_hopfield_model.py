import unittest
import scanpy as sc
from schopfield.hopfield_model import HopfieldModel

class TestHopfieldModel(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Load the preprocessed PBMC dataset from scanpy
        adata = sc.datasets.pbmc3k_processed()
        self.data = adata.X  # Dense matrix of gene expression
        self.cell_types = adata.obs['louvain'].values  # Cell type annotations
        self.gene_names = adata.var_names.tolist()  # Gene names

        # Instantiate the HopfieldModel
        self.model = HopfieldModel(self.data, self.cell_types, self.gene_names)

    def test_normalize_data(self):
        """Test Z-score normalization of the data."""
        self.model.normalize_data()
        self.assertIsNotNone(self.model.normalized_data)
        self.assertAlmostEqual(self.model.normalized_data.mean(axis=0).all(), 0, places=7)

    def test_select_highly_variable_genes(self):
        """Test selection of highly variable genes."""
        self.model.normalize_data()
        self.model.select_highly_variable_genes(top_percent=10)
        self.assertIsNotNone(self.model.hvgs)
        self.assertGreater(self.model.hvgs.shape[1], 0)
        self.assertEqual(len(self.model.selected_genes), self.model.hvgs.shape[1])

    def test_construct_weight_matrices(self):
        """Test construction of weight matrices."""
        self.model.normalize_data()
        self.model.select_highly_variable_genes(top_percent=10)
        self.model.construct_weight_matrices()
        self.assertIsNotNone(self.model.weight_matrices)
        self.assertEqual(len(self.model.weight_matrices), self.data.shape[0])

    def test_compute_hopfield_energy(self):
        """Test Hopfield energy computation."""
        self.model.normalize_data()
        self.model.select_highly_variable_genes(top_percent=10)
        self.model.construct_weight_matrices()
        energy = self.model.compute_hopfield_energy(0)
        self.assertIsInstance(energy, float)

    def test_plot_transition_energy(self):
        """Test the transition energy plotting function."""
        self.model.normalize_data()
        self.model.select_highly_variable_genes(top_percent=10)
        self.model.construct_weight_matrices()
        # Ensure it runs without error
        model.plot_transition_energy("B cells", "NK cells")

    def test_plot_gene_transition_matrix(self):
        """Test the gene transition matrix plotting function."""
        self.model.normalize_data()
        self.model.select_highly_variable_genes(top_percent=10)
        self.model.construct_weight_matrices()
        top_genes_1, top_genes_2 = self.model.plot_gene_transition_matrix("0", "1")
        self.assertEqual(len(top_genes_1), 5)
        self.assertEqual(len(top_genes_2), 5)

if __name__ == "__main__":
    unittest.main()
