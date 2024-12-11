import unittest
import numpy as np
import string
from src.GAlgoPy_ar4mus.initialize_population import initialize_population


class TestInitializePopulation(unittest.TestCase):
    def test_number_genes_no_range_provided(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=3,
                genes_type="number",
                allow_repetition=False
            )
        self.assertEqual(str(context.exception), "gene_range must be provided for genes_type = 'number'.")

    def test_number_genes_insufficient_unique_values(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=10,  # Request more unique values than available in the range.
                genes_type="number",
                gene_range=[1, 5],  # Only 5 unique values.
                allow_repetition=False
            )
        self.assertEqual(
            str(context.exception),
            "Insufficient unique values for the specified gene range without repetition."
        )

    def test_letters_insufficient_unique_values(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=60,  # More than the total number of letters (52).
                genes_type="letters",
                allow_repetition=False
            )
        self.assertEqual(
            str(context.exception),
            "Insufficient unique values for the specified genes without repetition."
        )

    def test_uppercase_letters_insufficient_unique_values(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=30,  # More than the total number of uppercase letters (26).
                genes_type="uppercase_letters",
                allow_repetition=False
            )
        self.assertEqual(
            str(context.exception),
            "Insufficient unique values for the specified genes without repetition."
        )

    def test_lowercase_letters_insufficient_unique_values(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=30,  # More than the total number of lowercase letters (26).
                genes_type="lowercase_letters",
                allow_repetition=False
            )
        self.assertEqual(
            str(context.exception),
            "Insufficient unique values for the specified genes without repetition."
        )

    def test_custom_genes_no_values_provided(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=3,
                genes_type="custom",
                custom_value=[],  # Empty list of custom values.
                allow_repetition=False
            )
        self.assertEqual(str(context.exception), "Insufficient unique values for the specified genes without repetition.")

    def test_custom_genes_no_values_provided_without_allow_repetition(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=3,
                genes_type="custom",
                custom_value=[],  # Empty list of custom values.
            )
        self.assertEqual(str(context.exception), "For genes_type = 'custom', custom_value is required.")

    def test_custom_genes_insufficient_unique_values(self):
        with self.assertRaises(ValueError) as context:
            initialize_population(
                pop_size=5,
                num_genes=5,
                genes_type="custom",
                custom_value=["A", "B", "C"],  # Only 3 unique values provided.
                allow_repetition=False
            )
        self.assertEqual(
            str(context.exception),
            "Insufficient unique values for the specified genes without repetition."
        )

    def test_binary_genes(self):
        pop_size = 10
        num_genes = 5
        population = initialize_population(pop_size, num_genes, genes_type="binary")
        self.assertEqual(population.shape, (pop_size, num_genes))
        self.assertTrue(np.all(np.isin(population, [0, 1])))

    def test_number_genes_with_range(self):
        pop_size = 10
        num_genes = 5
        gene_range = [0, 10]
        population = initialize_population(pop_size, num_genes, genes_type="number", gene_range=gene_range)
        self.assertEqual(population.shape, (pop_size, num_genes))
        self.assertTrue(np.all(population >= gene_range[0]))
        self.assertTrue(np.all(population <= gene_range[1]))

    def test_number_genes_no_repetition(self):
        pop_size = 10
        num_genes = 5
        gene_range = [0, 10]
        population = initialize_population(pop_size, num_genes, genes_type="number", gene_range=gene_range,
                                           allow_repetition=False)
        self.assertEqual(population.shape, (pop_size, num_genes))
        for individual in population:
            self.assertEqual(len(set(individual)), num_genes)  # No repetitions in individuals.

    def test_letters_genes(self):
        pop_size = 10
        num_genes = 5
        population = initialize_population(pop_size, num_genes, genes_type="letters")
        self.assertEqual(population.shape, (pop_size, num_genes))
        valid_letters = list(string.ascii_letters)
        self.assertTrue(np.all([gene in valid_letters for gene in population.flatten()]))

    def test_uppercase_letters(self):
        pop_size = 10
        num_genes = 5
        population = initialize_population(pop_size, num_genes, genes_type="uppercase_letters")
        self.assertEqual(population.shape, (pop_size, num_genes))
        valid_letters = list(string.ascii_uppercase)
        self.assertTrue(np.all([gene in valid_letters for gene in population.flatten()]))

    def test_lowercase_letters(self):
        pop_size = 10
        num_genes = 5
        population = initialize_population(pop_size, num_genes, genes_type="lowercase_letters")
        self.assertEqual(population.shape, (pop_size, num_genes))
        valid_letters = list(string.ascii_lowercase)
        self.assertTrue(np.all([gene in valid_letters for gene in population.flatten()]))

    def test_custom_genes(self):
        pop_size = 10
        num_genes = 5
        custom_value = ['A', 'B', 'C', 'D', 'E']
        population = initialize_population(pop_size, num_genes, genes_type="custom", custom_value=custom_value)
        self.assertEqual(population.shape, (pop_size, num_genes))
        self.assertTrue(np.all([gene in custom_value for gene in population.flatten()]))

    def test_invalid_gene_type(self):
        with self.assertRaises(ValueError):
            initialize_population(10, 5, genes_type="invalid_type")

    def test_number_genes_without_range_error(self):
        with self.assertRaises(ValueError):
            initialize_population(10, 5, genes_type="number")

    def test_custom_genes_without_values_error(self):
        with self.assertRaises(ValueError):
            initialize_population(10, 5, genes_type="custom", custom_value=[])


if __name__ == "__main__":
    unittest.main()
