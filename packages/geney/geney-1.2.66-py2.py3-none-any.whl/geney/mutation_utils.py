from .seqmat_utils import *
import numpy as np

class Allele(SeqMat):
    def __init__(self, alt, pos1, pos2, rev):
        super().__init__(alt, pos1, pos2)
        self.position = min(pos1)
        if rev:
            self.reverse_complement()

    # def _continuous(self, ind):
    #     return True


class SNP(Allele):
    def __init__(self, alt, pos1, pos2):
        super().__init__(alt, pos1, pos2)
        pass

class INDEL(Allele):
    def __init__(self, alt, pos):
        super().__init__(alt, pos)
        pass

class INS(Allele):
    def __init__(self, alt, pos):
        super().__init__()
        pass

class DEL(Allele):
    def __init__(self, alt, pos):
        super().__init__()
        pass

def get_mutation(mut_id, rev=False):

    _, _, i, r, a = mut_id.split(':')
    i = int(i)

    if len(a) == len(r) == 1 and a != '-' and r != '-':
        return Allele(a, [i], [0], rev)

    elif a == '-' and r != '-':
        return Allele('-' *len(r), np.arange(i, i+ len(r), dtype=np.int32), [0] * len(r), rev)

    elif r == '-' and a != '-':
        # print(a, np.full(len(a), int(i)), np.arange(1, len(a)+1),)
        return Allele(a, np.full(len(a), int(i)), np.arange(1, len(a)+1), rev)

    elif a != '-' and r != '-':
        ind1 = np.concatenate(
            [np.arange(i, i + len(r), dtype=np.int32), np.full(len(a), len(r) + i - 1, dtype=np.int32)])
        ind2 = np.concatenate([np.zeros(len(r), dtype=np.int32), np.arange(1, len(a) + 1, dtype=np.int32)])
        return Allele('-' * len(r) + a, ind1, ind2, rev)



