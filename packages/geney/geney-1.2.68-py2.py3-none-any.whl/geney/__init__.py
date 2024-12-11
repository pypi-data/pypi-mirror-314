from .config_setup import get_config
config = get_config()
from .Fasta_segment import Fasta_segment
from .utils import *

mut_id = 'KRAS:12:25227343:G:T'
epistasis_id = 'KRAS:12:25227343:G:T|KRAS:12:25227344:A:T'

def available_genes(organism='hg38'):
    import os
    for file in os.listdir(config[organism]['MRNA_PATH'] / 'protein_coding'):
        gene = file.split('_')[-1].strip('.pkl')
        yield gene


# import os
# import json
# from pathlib import Path
#
# config_file = os.path.join(os.path.expanduser('~'), '.oncosplice_setup', 'config.json')
# if Path(config_file).exists():
#     config_setup = {k: Path(p) for k, p in json.loads(open(config_file).read()).items()}
#
# else:
#     print("Database not set up.")
#     config_setup = {}
#
