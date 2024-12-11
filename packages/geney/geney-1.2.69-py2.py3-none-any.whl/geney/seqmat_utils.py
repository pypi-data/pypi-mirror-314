from . import unload_pickle, Fasta_segment, config
import numpy as np
import copy
from Bio.Seq import Seq

NT_ALPHABET = ['A', 'T', 'G', 'C', 'N']


'''
for DNAseq
    character track
    position1 track
    position2 track
    transcript track
    orf track
    
for AAseq
    character track
    position track
    conservation track
    domain track
'''
class SeqMat:
    ROW_SEQ = 0
    ROW_INDS = 1
    ROW_SUPERINDS = 2

    def __init__(self, seq='-', inds=None, superinds=None, alphabet=NT_ALPHABET, ref=False):
        seq = list(seq)
        if inds is None:
            inds = np.arange(0, len(seq), dtype=np.int32)

        if superinds is None:
            superinds = np.zeros(len(seq), dtype=np.int32)

        else:
            assert len(seq) == len(inds), f'Sequence length {len(seq)} must be equal to indices length {len(inds)}'
            assert self._is_monotonic(inds), f'Sequence indices must be monotonic, got {inds}'

        self.char_to_value = {c: i + 1 for i, c in enumerate(alphabet)}
        self.value_to_char = {i: c for c, i in self.char_to_value.items()}
        self.complement_char = {1: 2, 2: 1, 3: 4, 4: 3}

        self.vectorized_map_c2v = np.vectorize(self.map_char_to_value)
        self.vectorized_map_v2c = np.vectorize(self.map_value_to_char)
        self.vectorized_map_v2v = np.vectorize(self.map_values_to_complement)
        self.seqmat = np.vstack([self.vectorized_map_c2v(seq), inds, superinds], dtype=np.int32)
        self.rev = ref
        if self.rev:
            self.reverse_complement()

    def __repr__(self):
        return self.seq

    def __str__(self):
        return self.seq

    def __len__(self):
        return len(self.seq)

    def _is_monotonic(self, inds):
        # return all(x <= y for x, y in zip(inds, inds[1:])) or all(x >= y for x, y in zip(inds, inds[1:]))
        return True  # np.all(np.diff(inds) >= 0) or np.all(np.diff(inds) <= 0)

    def map_char_to_value(self, char):
        return self.char_to_value.get(char, 0)  # Return 0 if character not found

    def map_value_to_char(self, val):
        return self.value_to_char.get(val, '-')  # Return 0 if character not found

    def map_values_to_complement(self, val):
        return self.complement_char.get(val, 0)

    def mutate(self, mut, return_seqmat=False):
        ref_seqmat = self.seqmat.copy()
        mut_seqmat = mut.seqmat
        # assert ref_seqmat[self.ROW_INDS, :].min() <= mut_seqmat[self.ROW_INDS, :].min() and ref_seqmat[self.ROW_INDS,
        #                                                                                     :].max() >= mut_seqmat[
        #                                                                                                 self.ROW_INDS,
        #                                                                                                 :].max(), 'Mutation outside sequence'
        # assert np.all(np.isin(mut_seqmat[1, :], ref_seqmat[1, :])), "Mutation not in sequence"
        if not np.all(np.isin(mut_seqmat[1, :], ref_seqmat[1, :])):
            if return_seqmat:
                return ref_seqmat

            return ''.join(self.vectorized_map_v2c(ref_seqmat[self.ROW_SEQ, :])), ref_seqmat[self.ROW_INDS,
                                                                                  :], ref_seqmat[
                                                                                      self.ROW_SUPERINDS,
                                                                                      :]

        if np.any(mut_seqmat[self.ROW_SUPERINDS, :] > 0):
            insertions = np.where(mut_seqmat[self.ROW_SUPERINDS, :] > 0)[0][0]
            mut_seqmat, ins_seqmat = mut_seqmat[:, :insertions], mut_seqmat[:, insertions:]
            ins_loc = np.where(ref_seqmat[1, :] == ins_seqmat[1, 0])[0][0] + 1
            ref_seqmat = np.insert(ref_seqmat, ins_loc, ins_seqmat.T, axis=1)

        condition = np.logical_and(np.isin(ref_seqmat[self.ROW_INDS, :], mut_seqmat[self.ROW_INDS, :]),
                                   ref_seqmat[self.ROW_SUPERINDS, :] == 0)
        indices = np.where(condition)[0]
        ref_seqmat[:, indices] = mut_seqmat
        if return_seqmat:
            return ref_seqmat

        return ''.join(self.vectorized_map_v2c(ref_seqmat[self.ROW_SEQ, :])), ref_seqmat[self.ROW_INDS, :], ref_seqmat[
                                                                                                            self.ROW_SUPERINDS,
                                                                                                            :]

    def reverse_complement(self):
        self.seqmat = self.seqmat[:, ::-1]
        self.seqmat[0, :] = self.vectorized_map_v2v(self.seqmat[0, :])

    def pull_region(self, inds1, inds2=None):
        start_pos = np.where(self.seqmat[self.ROW_INDS] == inds1[0])[0][0]
        end_pos = np.where(self.seqmat[self.ROW_INDS] == inds1[1])[0][0] + 1
        return self.seqmat[:, start_pos:end_pos]

    def set_seqmat(self, mat):
        self.seqmat = mat
        return self

    def __add__(self, mut):
        return SeqMat(*self.mutate(mut))

    def __iadd__(self, mut):
        self.seqmat = self.mutate(mut, return_seqmat=True)
        return self

    @property
    def seq(self):
        return ''.join(self.vectorized_map_v2c(self.seqmat[self.ROW_SEQ, :])).replace('-', '')

    @property
    def indices(self):
        return self.seqmat[self.ROW_INDS, self.seqmat[self.ROW_SEQ, :] != 0] + (self.seqmat[self.ROW_SUPERINDS, self.seqmat[self.ROW_SEQ, :] != 0] / 10)

    @property
    def rawseq(self):
        return ''.join(self.vectorized_map_v2c(self.seqmat[self.ROW_SEQ, :]))

    def subseq(self, start, end):
        start_pos = np.where(self.seqmat[self.ROW_INDS] == start)[0][0]
        end_pos = np.where(self.seqmat[self.ROW_INDS] == end)[0][0] + 1
        return self.seq[start_pos:end_pos]

    def raw_subseq(self, start, end):
        start_pos = np.where(self.seqmat[self.ROW_INDS] == start)[0][0]
        end_pos = np.where(self.seqmat[self.ROW_INDS] == end)[0][0] + 1
        return self.seqmat[:, start_pos:end_pos]

    def asymmetric_subseq(self, center, left_context, right_context, padding='$'):
        center_idx = np.where(self.seqmat[self.ROW_INDS] == center)[0][0]
        start_idx = center_idx - left_context
        end_idx = center_idx + right_context + 1  # +1 because end index in slicing is exclusive
        left_padding = max(0, -start_idx)
        right_padding = max(0, end_idx - len(self.seqmat[self.ROW_INDS]))
        valid_start_idx = max(0, start_idx)
        valid_end_idx = min(len(self.seqmat[self.ROW_INDS]), end_idx)
        valid_subseq = self.seq[valid_start_idx:valid_end_idx]
        padded_subseq = (padding * left_padding) + valid_subseq + (padding * right_padding)
        return padded_subseq

    def asymmetric_indices(self, center, left_context, right_context):
        center_idx = np.where(self.seqmat[self.ROW_INDS] == center)[0][0]
        start_idx = center_idx - left_context
        end_idx = center_idx + right_context + 1  # +1 because end index in slicing is exclusive
        left_padding = max(0, -start_idx)
        right_padding = max(0, end_idx - len(self.seqmat[self.ROW_INDS]))
        valid_start_idx = max(0, start_idx)
        valid_end_idx = min(len(self.seqmat[self.ROW_INDS]), end_idx)
        valid_subseq = self.indices[valid_start_idx:valid_end_idx]
        return valid_subseq

    def subseq_suffix(self, start):
        start_pos = np.where(self.seqmat[self.ROW_INDS] == start)[0][0]
        return self.seqmat[:, start_pos:]

    def subseq_prefix(self, end):
        end_pos = np.where(self.seqmat[self.ROW_INDS] == end)[0][0]
        return self.seqmat[:, :end_pos]

    def inspect(self, pos, context=500):
        condition = np.where(self.seqmat[1, :] == pos)[0][0]
        return SeqMat().set_seqmat(self.seqmat[:, max(0, condition - context):min(self.seqmat.shape[-1], condition + context + 1)])

    def rel_pos(self, pos):
        if pos in self.indices:
            return np.where(self.seqmat[1, :] == pos)[0][0]
        else:
            return None

    def orf_seqmat(self, tis_index):
        if tis_index not in self.seqmat[1, :]:
            return SeqMat('ATG')

        temp = SeqMat().set_seqmat(self.subseq_suffix(tis_index))
        # Ensure the sequence length is divisible by 3
        # seq_length = len(temp.seq)

        # if seq_length % 3 != 0:
        #     temp.seqmat = temp.seqmat[:, :-(seq_length % 3)]  # Trim the extra nucleotides

        if temp.seq[1:3] == 'TG':
            for i in range(3, len(temp.seq), 3):
                codon = temp.seq[i:i + 3]
                if codon in ['TAA', 'TAG', 'TGA']:
                    index = temp.seqmat[1, i]
                    return SeqMat().set_seqmat(temp.subseq_prefix(index))  # Not include the stop codon

            # If no stop codon is found, return the full sequence
            return temp

        else:
            return SeqMat('ATG')

    def translate(self, tis_index):
        from Bio.Seq import Seq
        return Seq(self.orf_seqmat(tis_index).seq).translate()


class Gene:
    def __init__(self, gene_name='KRAS', variation=None, organism='hg38'):
        gene_files = list((config[organism]['MRNA_PATH'] / 'protein_coding').glob(f'*_{gene_name}.pkl'))
        if not gene_files:
            raise FileNotFoundError(f"No files available for gene {gene_name}.")

        data = unload_pickle(gene_files[0])
        for k, v in data.items():
            setattr(self, k, v)

        self.organism = organism
        needed_attributes = ['organism', 'transcripts', 'gene_name']
        assert all(hasattr(self, attr) for attr in needed_attributes), \
            f"Transcript is missing required attributes: {[attr for attr in needed_attributes if not hasattr(self, attr)]}"


    def __repr__(self):
        return f'Gene({self.gene_name})'

    def __len__(self):
        return len(self.transcripts)

    def __str__(self):
        return f"Gene: {self.gene_name}, ID: {self.gene_id}, Chr: {self.chrm}, Transcripts: {len(self.transcripts)}"

    def __copy__(self):
        return copy.copy(self)

    def __deepcopy__(self, memo):
        return copy.deepcopy(self, memo)

    def __getitem__(self, index):
        key = list(self.transcripts.keys())[index]
        return Transcript(self.transcripts[key])

    def splice_sites(self):
        from collections import Counter
        acceptors, donors = [], []
        for transcript in self.transcripts.values():
            acceptors.extend(transcript['acceptors'])
            donors.extend(transcript['donors'])
        return Counter(acceptors), Counter(donors)

    def transcript(self, tid=None):
        if tid is None:
            tid = self.primary_transcript

        if tid not in self.transcripts:
            raise AttributeError(f"Transcript '{tid}' not found in gene '{self.gene_name}'.")

        return Transcript(self.transcripts[tid], organism=self.organism)

    def run_transcripts(self, primary_transcript=False, protein_coding=False):
        for tid, annotations in self.transcripts.items():
            if (primary_transcript and not annotations.get('primary_transcript')) or \
                    (protein_coding and annotations.get('transcript_biotype') != 'protein_coding'):
                continue
            yield tid, Transcript(annotations, organism=self.organism)

    @property
    def primary_transcript(self):
        if not hasattr(self, '_primary_transcript'):
            primary_transcripts = [k for k, v in self.transcripts.items() if v.get('primary_transcript')]
            if len(primary_transcripts) > 0:
                self._primary_transcript = primary_transcripts[0]
                return self._primary_transcript

            primary_transcripts = [k for k, v in self.transcripts.items() if v.get('transcript_biotype') == 'protein_coding']
            if len(primary_transcripts) > 0:
                self._primary_transcript = primary_transcripts[0]
                return self._primary_transcript

            self._primar_transcript = None

        return self._primary_transcript


class Transcript:
    def __init__(self, d, organism='hg38'):
        for k, v in d.items():
            if k in ['acceptors', 'donors', 'cons_vector']:
                v = np.array(v)
            setattr(self, k, v)

        self.organism = organism
        needed_attributes = ['transcript_start', 'transcript_end', 'rev', 'chrm']
        assert all(hasattr(self, attr) for attr in needed_attributes), \
            f"Transcript is missing required attributes: {[attr for attr in needed_attributes if not hasattr(self, attr)]}"

        if not hasattr(self, 'donors'):
            self.donors = []

        if not hasattr(self, 'acceptors'):
            self.acceptors = []

        if not hasattr(self, 'cons_available'):
            self.cons_available = False

        if not (hasattr(self, 'TIS') and hasattr(self, 'TTS')):
            self.protein_coding = False
        else:
            self.protein_coding = True

        self.transcript_upper, self.transcript_lower = max(self.transcript_start, self.transcript_end), min(
            self.transcript_start, self.transcript_end)
        self.generate_pre_mrna()

        if self.cons_available:
            if '*' == self.cons_seq[-1] and len(self.cons_seq) == len(self.cons_vector):
                self.cons_vector = self.cons_vector[:-1]
                self.cons_seq = self.cons_seq[:-1]

    def __repr__(self):
        return 'Transcript({tid})'.format(tid=self.transcript_id)

    def __len__(self):
        return len(self.transcript_seq)

    def __str__(self):
        return 'Transcript {tid}, Transcript Type: ' \
               '{protein_coding}, Primary: {primary}'.format(
            tid=self.transcript_id, protein_coding=self.transcript_biotype.replace('_', ' ').title(),
            primary=self.primary_transcript)

    def __eq__(self, other):
        return self.transcript_seq == other.transcript_seq

    def __contains__(self, subvalue:np.array):
        '''
        :param subvalue: the substring to search for in the mature mrna transcript
        :return: wehether or not the substring is seen in the mature transcript or not
        '''
        return np.all(np.isin(subvalue.seqmat[1, :], self.pre_mrna.seqmat[1, :]))


    # def __handle_cons(self):
    # if '*' in self.cons_seq:
    #     self.cons_seq = self.cons_seq.replace('*', '')
    #     self.cons_vector = np.array(self.cons_vector[:-1])

    # if self.cons_seq == self.protein and len(self.cons_vector) == len(self.cons_seq):
    #     self.cons_available = True

    # if self.cons_available == False:
    #     self.cons_vector = np.ones(len(self.protein))

    @property
    def exons(self):
        '''
        :return: a list of tuples where the first position is the acceptor and the second position is the donor
        '''
        acceptors = np.concatenate(([self.transcript_start], self.acceptors))
        donors = np.concatenate((self.donors, [self.transcript_end]))
        return list(zip(acceptors, donors))

    @property
    def exons_pos(self):
        temp = self.exons
        if self.rev:
            # Reverse the order of exons and switch positions of the tuples
            temp = [(b, a) for a, b in temp[::-1]]
        return temp

    @property
    def introns(self):
        donors = self.donors[self.donors != self.transcript_end]
        acceptors = self.acceptors[self.acceptors != self.transcript_start]
        return list(zip(donors, acceptors))

    @property
    def introns_pos(self):
        temp = self.introns
        if self.rev:
            temp = [(b, a) for a, b in temp[::-1]]
        return temp

    def _fix_and_check_introns(self):
        self.acceptors = np.unique(self.acceptors)
        self.donors = np.unique(self.donors)
        self.acceptors = np.sort(self.acceptors)[::-1] if self.rev else np.sort(self.acceptors)
        self.donors = np.sort(self.donors)[::-1] if self.rev else np.sort(self.donors)

        if self.__exon_intron_matchup_flag():
            raise ValueError(f"Unequal number of acceptors and donors.")
        if self.__exon_intron_order_flag():
            raise ValueError(f"Exons / intron order out of position.")
        if self.__transcript_boundary_flag():
            raise ValueError(f"Transcript boundaries must straddle acceptors and donors.")

        return self

    def __exon_coverage_flag(self):
        exon_lengths = np.sum(np.abs(self.acceptors - self.donors) + 1)  # Vectorized calculation
        return exon_lengths != len(self)

    def __exon_intron_matchup_flag(self):
        return len(self.acceptors) != len(self.donors)

    def __exon_intron_order_flag(self):
        exons_pos = self.exons_pos  # Precomputed exons with positions
        return np.any([start > end for start, end in exons_pos])

    def __transcript_boundary_flag(self):
        if len(self.acceptors) == 0 and len(self.donors) == 0:
            return False

        min_boundary = np.min(np.concatenate((self.acceptors, self.donors)))
        max_boundary = np.max(np.concatenate((self.acceptors, self.donors)))
        return self.transcript_lower > min_boundary or self.transcript_upper < max_boundary

    @property
    def exonic_indices(self):
        return np.concatenate([np.arange(a, b + 1) for a, b in self.exons_pos])

    # Related to transcript seq generation
    def pull_pre_mrna_pos(self):
        fasta_obj = Fasta_segment()
        return fasta_obj.read_segment_endpoints(config[self.organism]['CHROM_SOURCE'] / f'chr{self.chrm}.fasta',
                                                self.transcript_lower,
                                                self.transcript_upper)

    def generate_pre_mrna(self):
        pre_mrna = SeqMat(*self.pull_pre_mrna_pos())
        if self.rev:
            pre_mrna.reverse_complement()

        self.pre_mrna = pre_mrna
        return self

    def generate_mature_mrna(self, inplace=True):
        self._fix_and_check_introns()

        exon_regions = []
        for exon in self.exons:
            exon_regions.append(self.pre_mrna.pull_region(exon))
        mature_mrna = np.concatenate(exon_regions, axis=1)
        if inplace:
            self.mature_mrna = SeqMat().set_seqmat(mature_mrna)
            return self

        return mature_mrna

    def find_end_codon(self, orf):
        first_stop_index = next((i for i in range(0, len(orf) - 2, 3) if orf[i:i + 3] in {"TAG", "TAA", "TGA"}),
                                len(orf) - 3)
        return first_stop_index

    @property
    def orf(self):
        if not (hasattr(self, 'TIS') and hasattr(self, 'TTS')):
            print("Cannot create protein without set TIS and TTS values.")
            return self
        #   If self.TIS not in seqmat, then no orf and no protein
        return self.mature_mrna.orf_seqmat(self.TIS)

        # return SeqMat().set_seqmat(self.mature_mrna.raw_subseq(self.TIS, self.TTS))

    def generate_protein(self, inplace=True, domains=None):
        protein = str(Seq(self.orf.seq).translate()).replace('*', '')
        if hasattr(self, 'cons_vector'):
            cons_vector = self.cons_vector
        else:
            cons_vector = np.ones(len(protein))

        if domains is not None and np.all(np.isin(domains, np.arange(0, len(protein)))):
            all_indices = np.arange(cons_vector.size)
            mask = ~np.isin(all_indices, domains)
            cons_vector[mask] = 0

        if inplace:
            self.protein = protein
            if domains is not None:
                self.cons_vector = cons_vector
            return self

        return protein, cons_vector

