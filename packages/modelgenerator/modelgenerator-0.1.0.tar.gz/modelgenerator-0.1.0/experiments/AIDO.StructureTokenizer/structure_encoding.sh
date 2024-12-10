# 0. you possibly need to install git lfs if you haven't
# git lfs install
# this script ONLY support single gpu for now, but we will support multi-gpu soon

# 1. download the sample dataset
mkdir data
git clone https://huggingface.co/datasets/genbio-ai/sample-structure-dataset data/protstruct_sample_data

set -ex

# 2. run encoding and then decoding
# check logs/protstruct_model/casp15_pdb_files
# *_input.pdb are the original pdb files
# *_output.pdb are the reconstructed pdb files
# CUDA_VISIBLE_DEVICES=0 mgen predict --config=experiments/AIDO.StructureTokenizer/encode_decode.yaml


# 3. run encoding only
# check logs/protstruct_encode/casp15_struct_tokens.pt for the output tokens
# logs/protstruct_encode/codebook.pt for the codebook
CUDA_VISIBLE_DEVICES=0 mgen predict --config=experiments/AIDO.StructureTokenizer/encode.yaml

# 4. decode the tokens from step 3
# check logs/protstruct_decode/casp15_pdb_files for the output structures
CUDA_VISIBLE_DEVICES=0 mgen predict --config=experiments/AIDO.StructureTokenizer/decode.yaml
