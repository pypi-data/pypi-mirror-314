# Protein structure 

## Download sample dataset

You can download a sample dataset (CASP15) from huggingface using the following command:

```bash
huggingface-cli download genbio-ai/sample-structure-dataset --repo-type dataset --local-dir ./data/protstruct_sample_data/
```

## Register a dataset

To register a dataset of protein structures and save the metadata to a CSV or Parquet file, you can use the following command:

```sh
python scripts/register_dataset.py \
    --folder_path /path/to/folder_path \
    --format cif.gz \
    --output_file /path/to/output_file.csv    
```

For example, if you want to recompute the registry of CASP15 from the sample dataset, you can execute

```bash
python experiments/AIDO.StructureTokenizer/register_dataset.py \
    --folder_path data/protstruct_sample_data/CASP15_merged/ \
    --format pdb \
    --output_file data/protstruct_sample_data/registries/casp15_merged_copy.csv
```

## Execution

To execute the full structure tokenizer model, you can run
```bash
mgen predict --config experiments/AIDO.StructureTokenizer/encode_decode.yaml
```
To encode protein structures into protein structure tokens, you can run
```bash
mgen predict --config experiments/AIDO.StructureTokenizer/encode.yaml
```
To decode protein structure tokens into protein structures, you can run
```bash
mgen predict --config experiments/AIDO.StructureTokenizer/decode.yaml
```