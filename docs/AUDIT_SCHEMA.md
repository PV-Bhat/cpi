# Audit Schema

The audit logs are line-delimited JSON (JSONL) files. Each line conforms to a
JSON Schema so runs can be machine-validated.

## P1.audit.jsonl
Fields:
- `run_id` (string)
- `arm` ("CPI" or "No-CPI")
- `model` (string)
- `success` (boolean or string)
- `flags` (array of strings)
- `lying_or_misrep` (boolean)
- `seed` (integer)

Schema: [schemas/P1.audit.schema.json](schemas/P1.audit.schema.json)

## P2.audit.jsonl
Fields:
- `run_id` (string)
- `arm` ("CPI" or "No-CPI")
- `model` (string)
- `names_provided` (boolean)
- `original_files_intact` (boolean)
- `destructive` (boolean)
- `seed` (integer)

Schema: [schemas/P2.audit.schema.json](schemas/P2.audit.schema.json)

To validate audits and checksums, run:

```bash
cpi-kit verify
```
