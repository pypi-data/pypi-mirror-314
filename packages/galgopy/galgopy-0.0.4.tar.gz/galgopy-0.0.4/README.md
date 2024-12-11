![GAlgoPy](https://9uy6uxjgfktmbsba.public.blob.vercel-storage.com/GAlgoPy-2FOjRJYbQ9wcKq2sNSLDwMuAxLcgAi.png)

# GAlgoPy (Genetic Algorithm Python)
## Population Initialization Function
This repository contains a Python function, initialize_population, designed for initializing populations in genetic algorithms. The function is highly flexible, allowing users to customize the type of genes, the range of values, and whether repetition is allowed.

### Features
The **initialize_population** function supports the following features:

* **Binary Genes**: Initialize genes as binary values (0 or 1).
* **Numeric Genes**: Define genes as numeric values within a specified range, with options for discrete integers or continuous uniform values.
* **Binary Genes**: Initialize genes as binary values (0 or 1).
* **Numeric Genes**: Define genes as numeric values within a specified range, with options for discrete integers or continuous uniform values.
* **Alphabetic Genes**: Use letters (uppercase, lowercase, or both) as gene values.
* **Custom Genes**: Define a custom set of values for genes.
* **Repetition Control**: Optionally allow or disallow repetition of gene values within individuals.
* **Uniform Distribution**: For numeric genes, optionally generate values with continuous uniform distribution.

### Function Parameters
* **pop_size (int)**: The number of individuals in the population.
* **num_genes (int)**: The number of genes per individual.
* **genes_type (str)**: Specifies the type of genes.Supported values:
   * *'binary'*: Binary values (0 or 1).
   * *'number'*: Numeric values within a specified range.
   * *'letters'*: All alphabetic characters (uppercase and lowercase).
   * *'uppercase_letters'*: Uppercase alphabetic characters only.
   * *'lowercase_letters'*: Lowercase alphabetic characters only.
   * *'custom'*: Custom values provided by the user.
* **gene_range (list)**: A list [min, max] specifying the range of numeric genes (required for genes_type='number').
* **uniform (bool)**: If True, generates continuous uniform values for numeric genes.
* **custom_value (list)**: A list of custom values (required for genes_type='custom').
* **allow_repetition (bool)**: If False, ensures genes are unique within an individual.
### Returns
* **np.ndarray**: A 2D NumPy array representing the initialized population. Each row corresponds to an individual, and each column corresponds to a gene.
### Error Handling
Raises **ValueError** if:
* Required parameters (gene_range for 'number' or custom_value for 'custom') are missing.
* There are insufficient unique values to satisfy the num_genes requirement when allow_repetition=False.
* An invalid genes_type is provided.

## Examples
Binary Genes:
```
population = initialize_population(pop_size=5, num_genes=10, genes_type='binary')
```
Numeric Genes:
```
population = initialize_population(
    pop_size=5,
    num_genes=10,
    genes_type='number',
    gene_range=[1, 100]
)
```
Numeric Genes (Continuous Uniform):
```
population = initialize_population(
    pop_size=5,
    num_genes=10,
    genes_type='number',
    gene_range=[0, 1],
    uniform=True
)
```
Alphabetic Genes:
```
population = initialize_population(
    pop_size=5,
    num_genes=5,
    genes_type='letters'
)
```
Custom Genes:
```
population = initialize_population(
    pop_size=5,
    num_genes=5,
    genes_type='custom',
    custom_value=['A', 'B', 'C', 1, 2]
)
```
Numeric Genes Without Repetition:
```
population = initialize_population(
    pop_size=5,
    num_genes=5,
    genes_type='number',
    gene_range=[1, 10],
    allow_repetition=False
)
```
## How to Use
1 - Import the function into your project:
```
from GAlgoPy import initialize_population
```
2 - Call the function with your desired parameters.

3 - Use the generated population for your genetic algorithm.