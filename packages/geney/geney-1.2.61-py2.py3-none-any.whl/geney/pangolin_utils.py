# Load models
import torch
from pkg_resources import resource_filename
from pangolin.model import *
import numpy as np
import sys

pang_model_nums = [0, 1, 2, 3, 4, 5, 6, 7]
pang_models = []

device = torch.device('cpu')
if sys.platform == 'darwin':
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

if sys.platform == 'linux':
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


for i in pang_model_nums:
    for j in range(1, 6):
        model = Pangolin(L, W, AR).to(device)
        if torch.cuda.is_available():
            model.cuda()
            # weights = torch.load(resource_filename("pangolin","models/final.%s.%s.3" % (j, i)))
            weights = torch.load(resource_filename("pangolin", "models/final.%s.%s.3" % (j, i)), weights_only=True)

        else:
            weights = torch.load(resource_filename("pangolin","models/final.%s.%s.3" % (j, i)), weights_only=True,
                                 map_location=device)

        model.load_state_dict(weights)
        model.eval()
        pang_models.append(model)


def pang_one_hot_encode(seq):
    IN_MAP = np.asarray([[0, 0, 0, 0],
                         [1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    seq = seq.upper().replace('A', '1').replace('C', '2')
    seq = seq.replace('G', '3').replace('T', '4').replace('N', '0')
    seq = np.asarray(list(map(int, list(seq))))
    return IN_MAP[seq.astype('int8')]



def pangolin_predict_probs(true_seq, models, just_ss=False):
    # print(f"Running pangolin on: {true_seq}")
    if just_ss:
        model_nums = [0, 2, 4, 6]
    else:
        model_nums = [0, 1, 2, 3, 4, 5, 6, 7]

    INDEX_MAP = {0: 1, 1: 2, 2: 4, 3: 5, 4: 7, 5: 8, 6: 10, 7: 11}

    seq = true_seq
    true_seq = true_seq[5000:-5000]
    acceptor_dinucleotide = np.array([true_seq[i - 2:i] == 'AG' for i in range(len(true_seq))]) # np.ones(len(true_seq)) #
    donor_dinucleotide = np.array([true_seq[i+1:i+3] == 'GT' for i in range(len(true_seq))]) #np.ones(len(true_seq)) #

    seq = pang_one_hot_encode(seq).T
    seq = torch.from_numpy(np.expand_dims(seq, axis=0)).float()

    # if torch.cuda.is_available():
    seq = seq.to(torch.device(device))

    scores = []
    for j, model_num in enumerate(model_nums):
        score = []
        # Average across 5 models
        for model in models[5 * j:5 * j + 5]:
            with torch.no_grad():
                score.append(model(seq.to(device))[0][INDEX_MAP[model_num], :].cpu().numpy())

        scores.append(np.mean(score, axis=0))

    splicing_pred = np.array(scores).max(axis=0)
    donor_probs = [splicing_pred[i] * donor_dinucleotide[i] for i in range(len(true_seq))]
    acceptor_probs = [splicing_pred[i] * acceptor_dinucleotide[i] for i in range(len(true_seq))]
    return donor_probs, acceptor_probs