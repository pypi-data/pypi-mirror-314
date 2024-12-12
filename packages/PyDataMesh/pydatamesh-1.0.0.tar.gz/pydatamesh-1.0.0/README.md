# PyDataMesh

PyDataMesh is a Python-based library designed to implement core concepts of data mesh architecture. It facilitates decentralised data ownership, robust data governance, and a unified catalog for managing metadata. This library enables teams to manage their data domains, create data products, and enforce policies while adhering to data mesh principles.

## Key Features

### 1. **Data Domains**
- Encapsulate data ownership within logical boundaries.
- Maintain collections of data products specific to a domain.

### 2. **Data Products**
- Self-contained, discoverable datasets.
- Query datasets using flexible filters.
- Provide metadata to enhance discoverability and governance.

### 3. **Unity Catalog Integration**
- Manage metadata for data products.
- Register, retrieve, and list metadata for enhanced context.

### 4. **Data Platform**
- Facilitate the addition and management of domains and data products.
- Provide a centralised interface for accessing decentralised data.

### 5. **Federated Governance**
- Apply governance policies across domains to ensure compliance.
- Example: Masking sensitive data or enforcing specific access rules.

## Installation

To install PyDataMesh, clone the repository and add it to your project:

```bash
# Clone the repository
git clone https://github.com/vpdeva/PyDataMesh.git

# Navigate to the folder
cd PyDataMesh
```

## Example Usage

Here is an example of how to use PyDataMesh:

```python
import pandas as pd
from core.data_mesh import PyDataMesh

if __name__ == "__main__":
    data_mesh = PyDataMesh()

    # Create domains
    data_mesh.create_domain("Sales")
    data_mesh.create_domain("HR")

    # Add data products
    sales_data = pd.DataFrame({"order_id": [1, 2, 3], "amount": [100, 200, 300]})
    hr_data = pd.DataFrame({"employee_id": [1, 2], "name": ["Alice", "Bob"]})

    data_mesh.add_data_product("Sales", "SalesData", sales_data, metadata={"owner": "Sales Team", "description": "Sales transaction data."})
    data_mesh.add_data_product("HR", "EmployeeData", hr_data, metadata={"owner": "HR Team", "description": "Employee information."})

    # Query data products
    print(data_mesh.query_data_product("Sales", "SalesData", {"amount": 200}))

    # Add governance policy
    def mask_amount(data):
        data["amount"] = data["amount"].apply(lambda x: "MASKED" if x > 150 else x)
        return data

    data_mesh.add_governance_policy("Sales", mask_amount)

    # Get data with policies
    print(data_mesh.get_data_with_policies("Sales", "SalesData"))

    # Retrieve metadata
    print(data_mesh.get_product_metadata("Sales", "SalesData"))

    # List all registered products
    print(data_mesh.list_registered_products())
```

## Folder Structure

```
PyDataMesh/
├── core/
│   └── data_mesh.py  # Core library implementation
├── examples/
│   └── example_usage.py  # Example usage of the library
└── README.md  # Library documentation
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
