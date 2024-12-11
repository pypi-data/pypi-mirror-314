import copy

from Bio import pairwise2
import re
import numpy as np
import pandas as pd
from .splicing_utils import find_transcript_missplicing, develop_aberrant_splicing, Missplicing
from .seqmat_utils import *
from .mutation_utils import *
from .tis_utils import find_tis

def find_continuous_gaps(sequence):
    """Find continuous gap sequences in an alignment."""
    return [(m.start(), m.end()) for m in re.finditer(r'-+', sequence)]


def get_logical_alignment(ref_prot, var_prot):
    """
    Aligns two protein sequences and finds the optimal alignment with the least number of gaps.

    Parameters:
    ref_prot (str): Reference protein sequence.
    var_prot (str): Variant protein sequence.

    Returns:
    tuple: Optimal alignment, number of insertions, and number of deletions.
    """

    if var_prot == '':
        print("here")
        var_prot = ref_prot[0]

    # Perform global alignment
    alignments = pairwise2.align.globalms(ref_prot, var_prot, 1, -1, -3, 0, penalize_end_gaps=(True, True))
    if len(alignments) == 0:
        print(ref_prot, var_prot)
        print(alignments)

    # Selecting the optimal alignment
    if len(alignments) > 1:
        # Calculate continuous gaps for each alignment and sum their lengths
        gap_lengths = [sum(end - start for start, end in find_continuous_gaps(al.seqA) + find_continuous_gaps(al.seqB))
                       for al in alignments]
        optimal_alignment = alignments[gap_lengths.index(min(gap_lengths))]
    else:
        optimal_alignment = alignments[0]

    return optimal_alignment


def find_indels_with_mismatches_as_deletions(seqA, seqB):
    """
    Identify insertions and deletions in aligned sequences, treating mismatches as deletions.

    Parameters:
    seqA, seqB (str): Aligned sequences.

    Returns:
    tuple: Two dictionaries containing deletions and insertions.
    """
    if len(seqA) != len(seqB):
        raise ValueError("Sequences must be of the same length")

    mapperA, counter = {}, 0
    for i, c in enumerate(list(seqA)):
        if c != '-':
            counter += 1
        mapperA[i] = counter

    mapperB, counter = {}, 0
    for i, (c1, c2) in enumerate(list(zip(seqA, seqB))):
        if c2 != '-':
            counter += 1
        mapperB[i] = counter

    seqA_array, seqB_array = np.array(list(seqA)), np.array(list(seqB))

    # Find and mark mismatch positions in seqB
    mismatches = (seqA_array != seqB_array) & (seqA_array != '-') & (seqB_array != '-')
    seqB_array[mismatches] = '-'
    modified_seqB = ''.join(seqB_array)

    gaps_in_A = find_continuous_gaps(seqA)
    gaps_in_B = find_continuous_gaps(modified_seqB)

    insertions = {mapperB[start]: modified_seqB[start:end].replace('-', '') for start, end in gaps_in_A if
                  seqB[start:end].strip('-')}
    deletions = {mapperA[start]: seqA[start:end].replace('-', '') for start, end in gaps_in_B if
                 seqA[start:end].strip('-')}

    return deletions, insertions


def parabolic_window(window_size):
    """Create a parabolic window function with a peak at the center."""
    x = np.linspace(-1, 1, window_size)
    return 0.9 * (1 - x ** 2) + 0.1


def transform_conservation_vector(conservation_vector, window=13, factor=4):
    """
    Transforms a 1D conservation vector using different parameters.

    Args:
        conservation_vector (numpy.ndarray): Input 1D vector of conservation values.

    Returns:
        numpy.ndarray: A matrix containing transformed vectors.
    """
    # window = 13
    # factor = 4
    convolving_window = parabolic_window(window)
    transformed_vector = np.convolve(conservation_vector, convolving_window, mode='same') / np.sum(convolving_window)
    assert len(transformed_vector) == len(conservation_vector), f"Len Ref: {len(conservation_vector)}, Len New: {len(transformed_vector)}"
    # Compute exponential factors
    exp_factors = np.exp(-transformed_vector * factor)

    # Normalize and scale exponential factors
    # exp_factors /= exp_factors.sum()
    return exp_factors


def find_modified_positions(sequence_length, deletions, insertions, reach_limit=16):
    """
    Identify unmodified positions in a sequence given deletions and insertions.

    :param sequence_length: Length of the sequence.
    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param reach_limit: Limit for considering the effect of insertions/deletions.
    :return: Array indicating unmodified positions.
    """
    unmodified_positions = np.zeros(sequence_length, dtype=float)

    for pos, deletion in deletions.items():
        deletion_length = len(deletion)
        unmodified_positions[pos:pos + deletion_length] = 1

    for pos, insertion in insertions.items():
        reach = min(len(insertion) // 2, reach_limit)
        front_end, back_end = max(0, pos - reach), min(sequence_length, pos + reach)
        # len_start, len_end = pos - front_end, back_end - pos + 1
        # gradient_front = np.linspace(0, 1, len_start, endpoint=False)
        # gradient_back = np.linspace(0, 1, len_end, endpoint=True)[::-1]
        # combined_gradient = np.concatenate([gradient_front, gradient_back])  #np.array([1]),
        # print(len(unmodified_positions[front_end:back_end]), len(combined_gradient))
        unmodified_positions[front_end:back_end] = 1 #combined_gradient

    return unmodified_positions


def calculate_penalty(domains, cons_scores, W, is_insertion=False):
    """
    Calculate the penalty for mutations (either insertions or deletions) on conservation scores.

    :param domains: Dictionary of mutations (inserted or deleted domains).
    :param cons_scores: Conservation scores.
    :param W: Window size.
    :param is_insertion: Boolean flag to indicate if the mutation is an insertion.
    :return: Penalty array.
    """
    penalty = np.zeros(len(cons_scores))
    for pos, seq in domains.items():
        mutation_length = len(seq)
        weight = max(1.0, mutation_length / W)

        if is_insertion:
            reach = min(W // 2, mutation_length // 2)
            penalty[pos - reach:pos + reach] = weight * cons_scores[pos - reach:pos + reach]
        else:  # For deletion
            penalty[pos:pos + mutation_length] = cons_scores[pos:pos + mutation_length] * weight

    return penalty


def calculate_legacy_oncosplice_score(deletions, insertions, cons_vec, W):
    """
    Calculate the legacy Oncosplice score based on deletions, insertions, and conservation vector.

    :param deletions: Dictionary of deletions.
    :param insertions: Dictionary of insertions.
    :param cons_vec: Conservation vector.
    :param W: Window size.
    :return: Legacy Oncosplice score.
    """
    smoothed_conservation_vector = np.exp(np.negative(moving_average_conv(cons_vec, W, 2)))
    del_penalty = calculate_penalty(deletions, smoothed_conservation_vector, W, is_insertion=False)
    ins_penalty = calculate_penalty(insertions, smoothed_conservation_vector, W, is_insertion=True)
    combined_scores = del_penalty + ins_penalty
    return np.max(np.convolve(combined_scores, np.ones(W), mode='same'))


def moving_average_conv(vector, window_size, factor=1):
    """
    Calculate the moving average convolution of a vector.

    Parameters:
    vector (iterable): Input vector (list, tuple, numpy array).
    window_size (int): Size of the convolution window. Must be a positive integer.
    factor (float): Scaling factor for the average. Default is 1.

    Returns:
    numpy.ndarray: Convolved vector as a numpy array.
    """
    if not isinstance(vector, (list, tuple, np.ndarray)):
        raise TypeError("vector must be a list, tuple, or numpy array")
    if not isinstance(window_size, int) or window_size <= 0:
        raise ValueError("window_size must be a positive integer")
    if len(vector) < window_size:
        raise ValueError("window_size must not be greater than the length of vector")
    if factor == 0:
        raise ValueError("factor must not be zero")

    return np.convolve(vector, np.ones(window_size), mode='same') / window_size

def find_splice_site_proximity(pos, transcript):
    for i, (ex_start, ex_end) in enumerate(transcript.exons):
        if min(ex_start, ex_end) <= pos <= max(ex_start, ex_end):
            return i + 1, None, abs(pos - ex_start), abs(pos - ex_end)

    for i, (in_start, in_end) in enumerate(transcript.introns):
        if min(in_start, in_end) <= pos <= max(in_start, in_end):
            return None, i + 1, abs(pos - in_end), abs(pos - in_start)

    return None, None, np.inf, np.inf

def define_missplicing_events(ref, var):
    ref_introns, ref_exons = ref.introns, ref.exons
    var_introns, var_exons = var.introns, var.exons

    num_ref_exons = len(ref_exons)
    num_ref_introns = len(ref_introns)

    partial_exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} truncated: {(t1, t2)} --> {(s1, s2)}' for (s1, s2) in var_exons for
         exon_count, (t1, t2) in enumerate(ref_exons)
         if (not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)))
         or (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)))])

    partial_intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} partially retained: {(t1, t2)} --> {(s1, s2)}' for (s1, s2)
         in var_introns for intron_count, (t1, t2) in enumerate(ref_introns)
         if (not ref.rev and ((s1 == t1 and s2 < t2) or (s1 > t1 and s2 == t2)))
         or (ref.rev and ((s1 == t1 and s2 > t2) or (s1 < t1 and s2 == t2)))])

    exon_skipping = ','.join(
        [f'Exon {exon_count + 1}/{num_ref_exons} skipped: {(t1, t2)}' for exon_count, (t1, t2) in enumerate(ref_exons)
         if t1 not in var.acceptors and t2 not in var.donors])

    novel_exons = ','.join([f'Novel Exon: {(t1, t2)}' for (t1, t2) in var_exons if
                            t1 not in ref.acceptors and t2 not in ref.donors])

    intron_retention = ','.join(
        [f'Intron {intron_count + 1}/{num_ref_introns} retained: {(t1, t2)}' for intron_count, (t1, t2) in
         enumerate(ref_introns)
         if t1 not in var.donors and t2 not in var.acceptors])

    return partial_exon_skipping, partial_intron_retention, exon_skipping, novel_exons, intron_retention


def summarize_missplicing_event(pes, pir, es, ne, ir):
    event = []
    if pes:
        event.append('PES')
    if es:
        event.append('ES')
    if pir:
        event.append('PIR')
    if ir:
        event.append('IR')
    if ne:
        event.append('NE')
    if len(event) >= 1:
        return ','.join(event)
    # elif len(event) == 1:
    #     return event[0]
    else:
        return '-'


# Annotating
def OncospliceAnnotator(reference_transcript, variant_transcript, mut):
    affected_exon, affected_intron, distance_from_5, distance_from_3 = find_splice_site_proximity(np.floor(mut.indices[0]),
                                                                                                  reference_transcript)

    report = {}

    report['primary_transcript'] = reference_transcript.primary_transcript
    report['transcript_id'] = reference_transcript.transcript_id
    # report['mut_id'] = mut.mut_id
    # report['cons_available'] = int(reference_transcript.cons_available)
    # report['protein_coding'] = reference_transcript.transcript_biotype

    # report['reference_mrna'] = reference_transcript.transcript_seq
    # report['reference_cds_start'] = reference_transcript.TIS
    # report['reference_pre_mrna'] = reference_transcript.pre_mrna
    # report[
    #     'reference_orf'] = reference_transcript.orf  # pre_mrna[reference_transcript.transcript_indices.index(reference_transcript.TIS):reference_transcript.transcript_indices.index(reference_transcript.TTS)]
    report['reference_protein'] = reference_transcript.protein
    # report['reference_protein_length'] = len(reference_transcript.protein)

    # report['variant_mrna'] = variant_transcript.transcript_seq
    # report['variant_cds_start'] = variant_transcript.TIS
    # report[
    #     'variant_pre_mrna'] = variant_transcript.pre_mrna  # pre_mrna[variant_transcript.transcript_indices.index(variant_transcript.TIS):variant_transcript.transcript_indices.index(variant_transcript.TTS)]
    # report['variant_orf'] = variant_transcript.orf
    report['variant_protein'] = variant_transcript.protein
    report['variant_protein_length'] = len(variant_transcript.protein)

    descriptions = define_missplicing_events(reference_transcript, variant_transcript)
    # print(descriptions)
    report['exon_changes'] = '|'.join([v for v in descriptions if v])
    report['splicing_codes'] = summarize_missplicing_event(*descriptions)
    report['affected_exon'] = affected_exon
    report['affected_intron'] = affected_intron
    report['mutation_distance_from_5'] = distance_from_5
    report['mutation_distance_from_3'] = distance_from_3
    return report


def oncosplice(mut_id, splicing_threshold=0.5, protein_coding=True, cons_required=False, primary_transcript=False, window_length=13, organism='hg38', engine='spliceai', domains=None):
    gene = Gene(mut_id.split(':')[0], organism=organism)
    reference_gene_proteins = {tid: transcript.generate_pre_mrna().generate_mature_mrna().generate_protein() for tid, transcript in gene.run_transcripts(protein_coding=True)}
    mutations = [get_mutation(m, rev=gene.rev) for m in mut_id.split('|')]

    results = []
    for tid, transcript in gene.run_transcripts(protein_coding=protein_coding, primary_transcript=primary_transcript):
        if cons_required and not transcript.cons_available:
            continue

        if all(mutation not in transcript for mutation in mutations):
            continue

        transcript.generate_pre_mrna()
        transcript.cons_vector = transform_conservation_vector(transcript.cons_vector, window=window_length)
        transcript.generate_mature_mrna().generate_protein(inplace=True, domains=domains)
        ref_protein, cons_vector = transcript.protein, transcript.cons_vector
        reference_transcript = copy.deepcopy(transcript)

        assert len(ref_protein) == len(cons_vector), f"Protein ({len(ref_protein)}) and conservation vector ({len(cons_vector)}) must be same length. {ref_protein}, \n>{cons_vector}\n>{transcript.cons_seq}"

        missplicing = Missplicing(find_transcript_missplicing(transcript, mutations, engine=engine, threshold=splicing_threshold), threshold=splicing_threshold)
        for mutation in mutations:
            transcript.pre_mrna += mutation

        for i, new_boundaries in enumerate(develop_aberrant_splicing(transcript, missplicing.aberrant_splicing)):
            transcript.acceptors = new_boundaries['acceptors']
            transcript.donors = new_boundaries['donors']
            transcript.generate_mature_mrna().generate_protein()

            alignment = get_logical_alignment(reference_transcript.protein, transcript.protein)
            deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
            modified_positions = find_modified_positions(len(ref_protein), deleted, inserted)
            temp_cons = np.convolve(cons_vector * modified_positions, np.ones(window_length)) / window_length
            affected_cons_scores = max(temp_cons)
            percentile = (
                        sorted(cons_vector).index(next(x for x in sorted(cons_vector) if x >= affected_cons_scores)) / len(
                    cons_vector))

            report = OncospliceAnnotator(reference_transcript, transcript, mutation)
            report['mut_id'] = mut_id
            report['oncosplice_score'] = affected_cons_scores
            report['percentile'] = percentile
            report['isoform_id'] = i
            report['isoform_prevalence'] = new_boundaries['path_weight']
            report['full_missplicing'] = missplicing.aberrant_splicing
            report['missplicing'] = max(missplicing)
            report['reference_resemblance'] = reference_gene_proteins.get(transcript.protein, None)
            results.append(report)

    if len(results) == 0:
        return None

    return pd.DataFrame(results)


import asyncio
async def oncosplice_prototype(mut_id, splicing_threshold=0.5, protein_coding=True, primary_transcript=False,
                               window_length=13, organism='hg38', engine='spliceai', use_cons=True, require_cons=False):
    import sys, os
    needed_file1 = config[organism]['yoram_path'] / 'rest_api_utils.py'
    needed_file2 = config[organism]['yoram_path'] / 'uniprot_utils.py'

    if sys.platform == 'linux' and (needed_file1.is_file() and os.access(needed_file1, os.R_OK)) and (
            needed_file2.is_file() and os.access(needed_file2, os.R_OK)):
        sys.path.append(str(config[organism]['yoram_path']))
        import uniprot_utils as uput

    else:
        raise SystemError(
            "Oncosplice Prototype can only be run on Power with access to the /tamir2/yoramzar/Projects/Cancer_mut/Utils folder.")

    from .tis_utils import find_tis

    # Define async functions
    async def background_request(ensb_id, Uniprot_features=["Topological domain", "Transmembrane", "Domain"]):
        return uput.retrieve_protein_data_features_subset(uput.ensembl_id2uniprot_id(ensb_id), Uniprot_features)

    def inspect_domain(row, modified_vector, conservation_vector):
        v1, v2 = modified_vector[row.start:row.end], conservation_vector[row.start:row.end]
        if sum(v2) == 0:
            return pd.Series([f'{row.type}|{row.start}|{row.end}|{row.description}', 0],
                             index=['domain_identifier', 'score'])

        return pd.Series([f'{row.type}|{row.start}|{row.end}|{row.description}', sum(v1 * v2) / sum(v2)],
                         index=['domain_identifier', 'score'])

    gene = Gene(mut_id.split(':')[0], organism=organism)
    reference_gene_proteins = {tid: transcript.generate_pre_mrna().generate_mature_mrna().generate_protein() for tid, transcript in gene.run_transcripts(protein_coding=True)}
    mutations = [get_mutation(mut_id, rev=gene.rev) for mut_id in mut_id.split('|')]
    results = []
    for tid, transcript in gene.run_transcripts(protein_coding=protein_coding, primary_transcript=primary_transcript):
        if require_cons and not transcript.cons_available:
            continue

        if all(mutation not in transcript for mutation in mutations):
            # results.append({'transcript_id': transcript.transcript_id})
            continue

        task1 = asyncio.create_task(background_request(tid))
        transcript.generate_pre_mrna()
        transcript.cons_vector = transform_conservation_vector(transcript.cons_vector, window=window_length)
        transcript.generate_mature_mrna().generate_protein(inplace=True)
        ref_protein, cons_vector = transcript.protein, transcript.cons_vector

        if not use_cons:
            cons_vector = np.ones(len(ref_protein))

        if sum(cons_vector) == 0:
            cons_vector = np.ones(len(ref_protein)) #/len(ref_protein)

        reference_transcript = copy.deepcopy(transcript)

        assert len(ref_protein) == len(
            cons_vector), f"Protein ({len(ref_protein)}) and conservation vector ({len(cons_vector)} must be same length."

        missplicing = Missplicing(find_transcript_missplicing(transcript, mutations, engine=engine, threshold=splicing_threshold),
                                  threshold=splicing_threshold)
        for mutation in mutations:
            transcript.pre_mrna += mutation

        domains_df = await task1
        for i, new_boundaries in enumerate(develop_aberrant_splicing(transcript, missplicing.aberrant_splicing)):
            transcript.acceptors = new_boundaries['acceptors']
            transcript.donors = new_boundaries['donors']
            transcript.generate_mature_mrna()
            transcript.TIS = find_tis(ref_seq=reference_transcript, mut_seq=transcript)
            transcript.generate_protein()

            alignment = get_logical_alignment(reference_transcript.protein, transcript.protein)
            deleted, inserted = find_indels_with_mismatches_as_deletions(alignment.seqA, alignment.seqB)
            modified_positions = find_modified_positions(len(ref_protein), deleted, inserted)
            temp_cons = np.convolve(cons_vector * modified_positions, np.ones(window_length)) / window_length
            affected_cons_scores = max(temp_cons)
            percentile = (
                    sorted(cons_vector).index(next(x for x in sorted(cons_vector) if x >= affected_cons_scores)) / len(
                cons_vector))

            out = domains_df.apply(lambda row: inspect_domain(row, modified_positions, cons_vector), axis=1)
            domains_affected = '+'.join([f'{a}:{round(b, 3)}' for a, b in list(zip(out.domain_identifier, out.score))])

            report = OncospliceAnnotator(reference_transcript, transcript, mutation)
            report['mut_id'] = mut_id
            report['oncosplice_score'] = affected_cons_scores
            report['cons_available'] = transcript.cons_available
            report['transcript_id'] = transcript.transcript_id
            report['percentile'] = percentile
            report['isoform_id'] = i
            report['isoform_prevalence'] = new_boundaries['path_weight']
            report['full_missplicing'] = missplicing.aberrant_splicing
            report['missplicing'] = max(missplicing)
            report['domains'] = domains_affected
            report['max_domain_score'] = out.score.max()

            report['reference_resemblance'] = reference_gene_proteins.get(transcript.protein, None)
            results.append(pd.Series(report))

    report = pd.concat(results, axis=1).T
    return report


if __name__ == '__main__':
    pass