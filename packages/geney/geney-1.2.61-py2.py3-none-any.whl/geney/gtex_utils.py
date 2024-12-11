import pandas as pd
from tqdm import tqdm

# Set pandas display options (if necessary)
pd.options.display.max_rows = 999

# Read metadata
metadata = pd.read_csv('GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt', delimiter='\t')
metadata_tissue_mapper = metadata[['SAMPID', 'SMTS']].drop_duplicates().set_index('SAMPID').to_dict()['SMTS']

# Initialize an empty DataFrame for combined results
combined_df = pd.DataFrame()

# Define chunk size
tpm_mean = []
# Process the main data file in chunks
for chunk in tqdm(pd.read_csv('GTEx_Analysis_2017-06-05_v8_RSEMv1.3.0_transcript_tpm.gct', header=2, chunksize=1000,
                              delimiter='\t')):
    # Perform the same operations on the chunk
    chunk = chunk.set_index(['transcript_id', 'gene_id']).rename(columns=metadata_tissue_mapper)
    # Append the processed chunk to the combined DataFrame
    tpm_mean.append(chunk.T.groupby(by=chunk.columns).mean().T)

# Compute the mean TPM per tissue
tpm_mean = pd.concat(tpm_mean)


cancer_projects = {
    "Adrenal Gland": "ACC",
    "Bladder": "BLCA",
    "Brain": ["GBM", "LGG"],  # Note: Brain maps to two projects
    "Breast": "BRCA",
    "Colon": "COAD",
    "Esophagus": "ESCA",
    "Kidney": ["KICH", "KIRC", "KIRP"],  # Note: Kidney maps to three projects
    "Liver": "LIHC",
    "Lung": "LUNG",
    "Ovary": "OV",
    "Pancreas": "PAAD",
    "Prostate": "PRAD",
    "Skin": "SKCM",
    "Stomach": "STAD",
    "Testis": "TGCT",
    "Uterus": "UCS"
}

tissue_projects = {
    "ACC": "Adrenal Gland",
    "BLCA": "Bladder",
    "GBM": "Brain",
    "LGG": "Brain",
    "BRCA": "Breast",
    "COAD": "Colon",
    "ESCA": "Esophagus",
    "KICH": "Kidney",
    "KIRC": "Kidney",
    "KIRP": "Kidney",
    "LIHC": "Liver",
    "LUNG": "Lung",
    "OV": "Ovary",
    "PAAD": "Pancreas",
    "PRAD": "Prostate",
    "SKCM": "Skin",
    "STAD": "Stomach",
    "TGCT": "Testis",
    "UCS": "Uterus"
}

