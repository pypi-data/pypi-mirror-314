import numpy as np
import pandas as pd
import os
from scipy.stats import percentileofscore
import shelve
from Bio.Align import PairwiseAligner
from geney import config

p = PairwiseAligner()


def find_tis(ref_seq, mut_seq, left_context=100, right_context=102):
    tis_coords = ref_seq.mature_mrna.asymmetric_indices(ref_seq.TIS, left_context=0, right_context=3)
    ref_seq, mut_seq = ref_seq.mature_mrna, mut_seq.mature_mrna

    # 1. Is the start codon (the indices) conserved in the mut sequence?
    assert all(a in ref_seq.seqmat[1, :] for a in
               tis_coords), f"Start codon indices specified not found in the reference sequence."
    tis_conserved = all(a in mut_seq.seqmat[1, :] for a in tis_coords)

    # 2. If condition 1 is passed, is the context around that start codon the same in both the reference and the mutated?
    context_conserved = False
    if tis_conserved:
        context_conserved = ref_seq.asymmetric_subseq(tis_coords[0], left_context=left_context,
                                                      right_context=right_context,
                                                      padding='$') == mut_seq.asymmetric_subseq(tis_coords[0],
                                                                                                left_context=left_context,
                                                                                                right_context=right_context,
                                                                                                padding='$')

    if context_conserved:
        return [(tis_coords[0], 1, 'canonical')]

    sc_table = pd.read_pickle(config['titer_path'] / 'titer_tis_scores.pickle')
    ref_seq_tis_context = ref_seq.asymmetric_subseq(tis_coords[0], left_context=left_context,
                                                    right_context=right_context, padding='$')

    ref_titer_score = retrieve_titer_score(ref_seq_tis_context)
    ref_titer_rank = percentileofscore(sc_table['tis_score'], ref_titer_score)
    ref_protein = ref_seq.translate(tis_coords[0])

    candidate_positions = np.array([mut_seq.seq[i:i + 3] in TITER_acceptable_TISs for i in range(len(mut_seq.seq))])
    candidate_positions = np.array(
        [p.align(ref_protein, mut_seq.translate(mut_seq.seqmat[1, i])).score if candidate_positions[i] == True else 0
         for i in range(len(ref_seq.seq))])

    candidate_positions = candidate_positions > sorted(candidate_positions)[-5] # implement correct logic
    candidate_positions = np.array([retrieve_titer_score(
        mut_seq.asymmetric_subseq(tis_coords[0], left_context=left_context, right_context=right_context,
                                  padding='$')) if candidate_positions[i] > 0 else False for i in
                                    range(len(ref_seq.seq))])
    candidate_positions = np.array(
        [percentileofscore(sc_table.tis_score, candidate_positions[i]) if candidate_positions[i] != False else 100 for i
         in range(len(ref_seq.seq))])
    best_position = np.where(candidate_positions == min(candidate_positions))[0][0]
    out = mut_seq.seqmat[1, best_position]
    return out  #output: [(genomic_coord1, probability, filter_tag), (genomic_coord2, probability, filter_tag)]


def seq_matrix(seq_list):
    tensor = np.zeros((len(seq_list), 203, 8))
    for i in range(len(seq_list)):
        seq = seq_list[i]
        j = 0
        for s in seq:
            if s == 'A' and (j < 100 or j > 102):
                tensor[i][j] = [1, 0, 0, 0, 0, 0, 0, 0]
            if s == 'T' and (j < 100 or j > 102):
                tensor[i][j] = [0, 1, 0, 0, 0, 0, 0, 0]
            if s == 'C' and (j < 100 or j > 102):
                tensor[i][j] = [0, 0, 1, 0, 0, 0, 0, 0]
            if s == 'G' and (j < 100 or j > 102):
                tensor[i][j] = [0, 0, 0, 1, 0, 0, 0, 0]
            if s == '$':
                tensor[i][j] = [0, 0, 0, 0, 0, 0, 0, 0]
            if s == 'A' and (j >= 100 and j <= 102):
                tensor[i][j] = [0, 0, 0, 0, 1, 0, 0, 0]
            if s == 'T' and (j >= 100 and j <= 102):
                tensor[i][j] = [0, 0, 0, 0, 0, 1, 0, 0]
            if s == 'C' and (j >= 100 and j <= 102):
                tensor[i][j] = [0, 0, 0, 0, 0, 0, 1, 0]
            if s == 'G' and (j >= 100 and j <= 102):
                tensor[i][j] = [0, 0, 0, 0, 0, 0, 0, 1]
            j += 1
    return tensor


def build_titer_model(TITER_path=config['hg38']['titer_path']):
    print('Building TITER model...')
    from tensorflow.keras.constraints import MaxNorm
    from tensorflow.keras.layers import Conv1D, MaxPool1D, LSTM, Dropout, Flatten, Dense, Activation
    from tensorflow.keras import Sequential, Input

    model = Sequential()
    model.add(Input(shape=(203, 8)))
    model.add(Conv1D(filters=128,
                     kernel_size=3,
                     padding='valid',
                     kernel_constraint=MaxNorm(3),
                     activation='relu'))
    model.add(MaxPool1D(3))
    model.add(Dropout(rate=0.21370950078747658))
    model.add(LSTM(units=256,
                   return_sequences=True))
    model.add(Dropout(rate=0.7238091317104384))
    model.add(Flatten())
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='nadam',
                  metrics=['accuracy'])

    models = []

    # Load weights into multiple instances of the model
    for i in range(32):
        model_copy = Sequential(model.layers)  # Create a new model instance with the same architecture
        weights_path = os.path.join(TITER_path, f"bestmodel_{i}.hdf5")

        if os.path.exists(weights_path):
            model_copy.load_weights(weights_path)  # Load weights into the new model instance
            models.append(model_copy)
            # print(f"Loaded model {i} with weights from {weights_path}")
        else:
            print(f"Warning: Weights file {weights_path} not found")

    return models


def calculate_titer_score(candidate_seq, titer_model=None):  # , prior):
    if titer_model is None:
        titer_model = TITER_MODEL
    processed_seq = seq_matrix([candidate_seq])  # Wrap in list to keep dimensions consistent
    # prior = np.array([prior]).reshape(1, 1)
    analyzed_score = np.zeros((1, 1))

    # Iterate through the models (assuming 32 models) and calculate the score
    for i in range(32):
        y_pred = titer_model[i].predict(processed_seq, verbose=0)
        analyzed_score += y_pred  # * prior
    print(analyzed_score)
    return analyzed_score[0][0]


def retrieve_titer_score(sequence, filename='sequences_shelve.db'):
    # Open the shelf (acts like a dictionary, stored in a file)
    with shelve.open(filename) as db:
        # Check if sequence is already in the shelf
        if sequence in db:
            return db[sequence]
        else:
            # If not, run the function, store the result, and return it
            value = calculate_titer_score(sequence, TITER_MODEL)
            db[sequence] = value
            return value


TITER_acceptable_TISs = ['ATG', 'CTG', 'ACG', 'TTG', 'GTG']
codon_tis_prior = {'ATG': 3.5287101354987644, 'CTG': 1.746859242328512, 'ACG': 1.3535552403706805,
                   'TTG': 1.1364995562364615, 'GTG': 1.218573747658257}
stop_codons = ['TAA', 'TAG', 'TGA']
TITER_MODEL = build_titer_model()
