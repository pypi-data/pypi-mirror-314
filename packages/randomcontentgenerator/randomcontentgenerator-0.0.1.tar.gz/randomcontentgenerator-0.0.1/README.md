This library provides utilities to generate mock data for testing purposes, including numbers, text, identifiers, and structured data.

## Modules Overview

1. **Number Generator**
   - Generate random integers, floats, or numbers with custom ranges.
   - Example:
     ```python
     generate_number(type="int", min=1, max=100)  # Random integer between 1 and 100
     ```

2. **Identifier Generator**
   - Generate unique identifiers like UUIDs, credit card numbers, or custom IDs.
   - Example:
     ```python
     generate_identifier(type="uuid")  # Random UUID-like string
     ```

3. **Text Generator**
   - Create random names, email addresses, or custom text strings.
   - Examples:
     ```python
     generate_name()  # Random name
     generate_email()  # Random email
     ```

4. **Structured Data Generator**
   - Generate structured mock data based on a schema definition.
   - Example:
     ```python
     schema = {"name": "random_name", "age": "random_int(min=18, max=60)"}
     generate_structured_data(schema, count=5)  # List of 5 data rows
     ```

## Formatting Data
Structured data can be saved in JSON, CSV, or Parquet formats:
- Example:
  ```python
  format_data(data, format_type="json", file_name="data")  # Save as data.json
  format_data(data, format_type="csv", file_name="data")   # Save as data.csv
  format_data(data, format_type="parquet", file_name="data")  # Save as data.parquet
