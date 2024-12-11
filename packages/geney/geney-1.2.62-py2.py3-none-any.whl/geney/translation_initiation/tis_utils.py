
import numpy as np
from geney.utils import unload_json
import joblib
import pkg_resources

pssm_file_path = pkg_resources.resource_filename('geney.translation_initiation', 'resources/kozak_pssm.json')
model_state = pkg_resources.resource_filename('geney.translation_initiation', 'resources/tis_regressor_model.joblib')
PSSM = unload_json(pssm_file_path)
TREE_MODEL = joblib.load(model_state)

def TISFInder(seq, index=None):
    '''
    Predicts the most likely start (TIS) and end (TTS) positions in a mature mRNA sequence.

    Parameters:
    var_seq (str): Mature mRNA sequence of a transcript with unknown TIS/TTS.
    var_index (list): Index coverage of the mRNA sequence.
    nstart (str): ORF of a mature reference sequence including start codon.
    istart (list): ORF index coverage of the reference sequence.

    Returns:
    tuple: A tuple containing the predicted relative positions of the start and end codons (TIS and TTS).
    '''

    start_codon_positions = [i for i in range(len(seq) - 2) if seq[i:i + 3] == 'ATG']
    if len(start_codon_positions) == 0:
        if index is None:
            return 0
        else:
            return index[0]

    kozak_scores = [calculate_kozak_score(seq, pos, PSSM) for pos in start_codon_positions]
    corresponding_end_codons = [get_end_codon(seq, pos) for pos in start_codon_positions]
    folding_scores = [calculate_folding_energy(seq, pos) for pos in start_codon_positions]
    # titer_scores = [calculate_titer_score(seq, pos) for por in start_codon_positions]

    input_X = np.array([kozak_scores, corresponding_end_codons, folding_scores]).transpose() #, titer_scores])
    scores = TREE_MODEL.predict(input_X)
    max_pos = np.argmax(scores)
    rel_start_pos = start_codon_positions[max_pos]

    if index is None:
        return rel_start_pos
    else:
        return index[rel_start_pos]


def calculate_kozak_score(seq, position, PSSM):
    """
    Calculates the Kozak score for a 9-nucleotide segment of a sequence,
    starting 3 nucleotides before the given position.

    Parameters:
    seq (str): The full nucleotide sequence.
    position (int): The relative position in the sequence to target for scoring.
    PSSM (np.array): Position-specific scoring matrix for Kozak sequence scoring.

    Returns:
    float: The calculated Kozak score, or None if the segment is not of valid length.

    Raises:
    ValueError: If the position is not valid within the sequence.
    """

    # Validate position for a valid 9-nucleotide segment
    if not 6 <= position < len(seq) - 9:
        return 0
        # raise ValueError("Position does not allow for a valid 9-nucleotide segment extraction.")

    # Extract the 9-nucleotide segment
    segment = seq[position - 6:position + 9]

    # Calculate score using list comprehension
    try:
        score = np.prod([PSSM[nucleotide][i] + 1 for i, nucleotide in enumerate(segment)])
    except KeyError as e:
        raise ValueError(f"Invalid nucleotide in sequence: {e}")

    return score

def calculate_folding_energy(seq, position, front_margin=20, back_margin=10):
    """
    Calculates the folding energy of a nucleotide sequence using ViennaRNA's RNAfold tool.

    Parameters:
    sequence (str): The nucleotide sequence for which folding energy is to be calculated.

    Returns:
    float: The folding energy of the sequence, or None if an error occurs.
    """
    import ViennaRNA
    segment = seq[max(0, position-front_margin):min(position+back_margin, len(seq))]
    return round(ViennaRNA.fold(segment)[-1], 3)

def get_end_codon(seq, start_position):
    """
    Finds the position of the first in-frame stop codon in a nucleotide sequence starting from a specified position.

    Parameters:
    seq (str): The nucleotide sequence.
    start_position (int): The relative position in the sequence to start searching for the stop codon.

    Returns:
    int: The relative position of the first in-frame stop codon after the start position.
         Returns -1 if no stop codon is found.
    """

    # Define stop codons
    stop_codons = ['TAG', 'TGA', 'TAA']

    # Check for each triplet (codon) in the sequence starting from start_position
    for i in range(start_position, len(seq) - 2, 3):
        codon = seq[i:i + 3]
        if codon in stop_codons:
            return i - start_position

    # Return -1 if no stop codon is found
    return 0

def calculate_titer_score(seq, pos):
    return 0


