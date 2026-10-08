# Declarative SKU DAG Pipeline Reference

## 1. SKU Template Schema (`sku-templates/*.json`)
```json
{
  "sku_id": "unique_sku_identifier",
  "display_name": "Human-Readable Job Name",
  "pipeline": ["research", "draft", "qa", "format"],
  "input_format": "markdown_and_pdf",
  "input_columns": ["field1", "field2"],
  "output_format": "markdown",
  "output_columns": ["output1", "output2"],
  "quality_rules": [
    "Strict invariant rule 1",
    "Strict invariant rule 2"
  ],
  "estimated_minutes_per_unit": 5,
  "units_per_batch": 10
}
```

## 2. Pipeline Stage Semantics
- **`research`**: High-speed symbol and fact extraction. Reads source documents without speculation.
- **`draft`**: Synthesizes the core body, equations, or code based strictly on research evidence.
- **`qa`**: Adversarial review. Tests edge cases, verifies against constraints and schemas.
- **`format`**: Standardizes outputs, KaTeX equation balance, and markdown layout.
