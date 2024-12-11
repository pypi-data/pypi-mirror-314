import numpy as np
import string
import math

def initialize_population(
        pop_size: int,
        num_genes: int,
        genes_type: str = "number",
        gene_range: list = None,
        uniform: bool = False,
        custom_value: list = None,
        allow_repetition: bool = True
) -> np.ndarray:
    """
    This function initializes a population for a genetic algorithm.

    Args:
        pop_size (int): The size of the population (number of individuals).
        num_genes (int): The number of genes per individual.
        genes_type (str): The type of genes to initialize. Valid types include:
            - 'binary': Genes take values 0 or 1.
            - 'number': Genes take numeric values within a given range.
            - 'letters': Genes take values from the entire alphabet (uppercase and lowercase).
            - 'uppercase_letters': Genes take values from uppercase letters only.
            - 'lowercase_letters': Genes take values from lowercase letters only.
            - 'custom': Genes take values from a user-defined set of values.
        gene_range (list): A list with two values [min, max], specifying the range for 'number' genes.
        uniform (bool): Whether to generate continuous uniform values (for 'number' genes only).
        custom_value (list): A list of custom values to randomly choose from (for 'custom' genes).
        allow_repetition (bool): Whether to allow repetition of genes within an individual.

    Returns:
        np.ndarray: A 2D NumPy array representing the initialized population.

    Raises:
        ValueError: If 'gene_range' is not provided for 'number' genes or if 'custom_value' is
                    not provided for 'custom' genes. Also, raises an error for invalid 'genes_type'.
    """

    # Validate that the range or values are sufficient when repetitions are not allowed
    if not allow_repetition:
        if genes_type == "number":
            if gene_range is None:
                raise ValueError("gene_range must be provided for genes_type = 'number'.")
            min_val, max_val = gene_range
            unique_values_count = math.floor(max_val) - math.ceil(min_val) + 1
            if unique_values_count < num_genes:
                raise ValueError("Insufficient unique values for the specified gene range without repetition.")
        elif genes_type in ["letters", "uppercase_letters", "lowercase_letters", "custom"]:
            if genes_type == "letters":
                unique_values_count = len(string.ascii_letters)
            elif genes_type == "uppercase_letters":
                unique_values_count = len(string.ascii_uppercase)
            elif genes_type == "lowercase_letters":
                unique_values_count = len(string.ascii_lowercase)
            elif genes_type == "custom":
                unique_values_count = len(custom_value)
            if unique_values_count < num_genes:
                raise ValueError("Insufficient unique values for the specified genes without repetition.")
    #

    # Match-case block to handle different types of genes initialization
    match genes_type:
        # Binary genes: Generate random 0 or 1 values for the entire population.
        case "binary":
            if allow_repetition:
                population = np.random.randint(2, size=(pop_size, num_genes))
            else:
                raise ValueError("Binary genes cannot disallow repetition as there are only 2 values.")

        # Numeric genes: Generate values in a specified range.
        case "number":
            if gene_range is None:
                # Raise an error if the range for numeric values is not provided.
                raise ValueError("gene_range must be provided for genes_type = 'number'.")
            min_val, max_val = gene_range  # Unpack the range into minimum and maximum values.
            if allow_repetition:
                if uniform:
                    # Generate continuous uniform random values within the specified range.
                    population = np.random.uniform(
                        low=min_val,
                        high=max_val,
                        size=(pop_size, num_genes)
                    )
                else:
                    # Generate discrete random integer values within the range.
                    population = np.random.randint(
                        low=math.ceil(min_val),  # Round the minimum value up.
                        high=math.floor(max_val) + 1,  # Round the maximum value down and include it.
                        size=(pop_size, num_genes)
                    )
            else:
                # Generate individuals without repetition
                population = np.array([
                    np.random.choice(
                        range(math.ceil(min_val), math.floor(max_val) + 1),
                        size=num_genes,
                        replace=False
                    ) for _ in range(pop_size)
                ])

        # Alphabetic genes (both uppercase and lowercase).
        case "letters":
            all_letters = list(string.ascii_letters)  # Create a list of all letters.
            if allow_repetition:
                population = np.random.choice(all_letters, size=(pop_size, num_genes))
            else:
                population = np.array([
                    np.random.choice(all_letters, size=num_genes, replace=False)
                    for _ in range(pop_size)
                ])

        # Uppercase alphabetic genes only.
        case "uppercase_letters":
            uppercase_letters = list(string.ascii_uppercase)  # Create a list of uppercase letters.
            if allow_repetition:
                population = np.random.choice(uppercase_letters, size=(pop_size, num_genes))
            else:
                population = np.array([
                    np.random.choice(uppercase_letters, size=num_genes, replace=False)
                    for _ in range(pop_size)
                ])

        # Lowercase alphabetic genes only.
        case "lowercase_letters":
            lowercase_letters = list(string.ascii_lowercase)  # Create a list of lowercase letters.
            if allow_repetition:
                population = np.random.choice(lowercase_letters, size=(pop_size, num_genes))
            else:
                population = np.array([
                    np.random.choice(lowercase_letters, size=num_genes, replace=False)
                    for _ in range(pop_size)
                ])

        # Custom genes: Values are chosen from a user-defined set.
        case "custom":
            if len(custom_value) == 0:
                # Raise an error if no custom values are provided.
                raise ValueError("For genes_type = 'custom', custom_value is required.")

            if allow_repetition:
                population = np.random.choice(custom_value, size=(pop_size, num_genes))
            else:
                population = np.array([
                    np.random.choice(custom_value, size=num_genes, replace=False)
                    for _ in range(pop_size)
                ])

        # Invalid gene type: Raise an error if the gene type is not recognized.
        case _:
            raise ValueError(
                f"Invalid genes_type: {genes_type}. Valid types are: 'binary', 'number',"
                f" 'letters', 'uppercase_letters', 'lowercase_letters', 'custom'")

    # Return the generated population as a NumPy array.
    return population
