import numpy as np
from .mutation_utils import get_mutation
from .seqmat_utils import Gene

from collections import defaultdict


def generate_adjacency_list(acceptors, donors, transcript_start, transcript_end, max_distance=50, rev=False):
    # Append the transcript end to donors to allow connection to the end point
    donors.append((transcript_end, 1))
    acceptors = sorted(acceptors, key=lambda x: (x[0], x[1] if not rev else -x[1]), reverse=rev)
    donors = sorted(donors, key=lambda x: (x[0], x[1] if not rev else -x[1]), reverse=rev)

    # Initialize adjacency list to store downstream connections
    adjacency_list = defaultdict(list)

    # Connect each donor to the nearest acceptor(s) within the distance threshold
    for d_pos, d_prob in donors:
        running_prob = 1
        for a_pos, a_prob in acceptors:
            correct_orientation = (a_pos > d_pos and not rev) or (a_pos < d_pos and rev)
            distance_valid = abs(a_pos - d_pos) <= max_distance
            if correct_orientation and distance_valid:
                in_between_acceptors = sum([d_pos < a < a_pos for a, _ in acceptors]) if not rev else sum([a_pos < a < d_pos for a, _ in acceptors])
                in_between_donors = sum([d_pos < d < a_pos for d, _ in donors]) if not rev else sum([a_pos < d < d_pos for d, _ in donors])
                in_between_naturals = 0
                if in_between_donors == 0 or in_between_acceptors == 0:
                    adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob))
                    running_prob -= a_prob

                else:
                    if running_prob > 0:
                        adjacency_list[(d_pos, 'donor')].append((a_pos, 'acceptor', a_prob*running_prob))
                        running_prob -= a_prob
                    else:
                        break

    # Connect each acceptor to the nearest donor(s) within the distance threshold
    for a_pos, a_prob in acceptors:
        running_prob = 1
        for d_pos, d_prob in donors:
            correct_orientation = (d_pos > a_pos and not rev) or (d_pos < a_pos and rev)
            distance_valid = abs(d_pos - a_pos) <= max_distance
            if correct_orientation and distance_valid:
                in_between_acceptors = sum([a_pos < a < d_pos for a, _ in acceptors]) if not rev else sum([d_pos < a < a_pos for a, _ in acceptors])
                in_between_donors = sum([a_pos < d < d_pos for d, _ in donors]) if not rev else sum([d_pos < d < a_pos for d, _ in donors])
                in_between_naturals = 0
                tag = 'donor' if d_pos != transcript_end else 'transcript_end'

                if in_between_acceptors == 0:
                    adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob))
                    running_prob -= d_prob
                else:
                    if running_prob > 0:
                        adjacency_list[(a_pos, 'acceptor')].append((d_pos, tag, d_prob*running_prob))
                        running_prob -= d_prob
                    else:
                        break

    # Connect the transcript start to the nearest donor(s) within the distance threshold
    running_prob = 1
    for d_pos, d_prob in donors:
        if ((d_pos > transcript_start and not rev) or (d_pos < transcript_start and rev)) and abs(
                d_pos - transcript_start) <= max_distance:
            adjacency_list[(transcript_start, 'transcript_start')].append((d_pos, 'donor', d_prob))
            running_prob -= d_prob
            if running_prob <= 0:
                break

    # Normalize probabilities to ensure they sum up to 1 for each list of connections
    for k, next_nodes in adjacency_list.items():
        prob_sum = sum([c for a, b, c in next_nodes])
        adjacency_list[k] = [(a, b, round(c / prob_sum, 3)) for a, b, c in next_nodes] if prob_sum > 0 else next_nodes

    return adjacency_list


def find_all_paths(graph, start, end, path=[], probability=1.0):
    path = path + [start]  # Add current node to the path
    if start == end:
        yield path, probability  # If end is reached, yield the path and its cumulative probability
        return
    if start not in graph:
        return  # If the start node has no outgoing edges, return

    for (next_node, node_type, prob) in graph[start]:
        # Recur for each connected node, updating the probability
        yield from find_all_paths(graph, (next_node, node_type), end, path, probability * prob)


def prepare_splice_sites(acceptors, donors, aberrant_splicing):
    acceptors = {p: 1 for p in acceptors}
    donors = {p: 1 for p in donors}

    for p, v in aberrant_splicing[f'missed_donors'].items():
        donors[p] = v['absolute']

    for p, v in aberrant_splicing[f'discovered_donors'].items():
        donors[p] = v['absolute']

    for p, v in aberrant_splicing[f'missed_acceptors'].items():
        acceptors[p] = v['absolute']

    for p, v in aberrant_splicing[f'discovered_acceptors'].items():
        acceptors[p] = v['absolute']

    acceptors = {int(k): v for k, v in acceptors.items()}
    donors = {int(k): v for k, v in donors.items()}
    return list(acceptors.items()), list(donors.items())


def develop_aberrant_splicing(transcript, aberrant_splicing):
    all_acceptors, all_donors = prepare_splice_sites(transcript.acceptors, transcript.donors, aberrant_splicing)
    adj_list = generate_adjacency_list(all_acceptors, all_donors, transcript_start=transcript.transcript_start,
                                       transcript_end=transcript.transcript_end, rev=transcript.rev,
                                       max_distance=100000)
    end_node = (transcript.transcript_end, 'transcript_end')
    start_node = (transcript.transcript_start, 'transcript_start')
    for path, prob in find_all_paths(adj_list, start_node, end_node):
        yield {'acceptors': [p[0] for p in path if p[1] == 'acceptor'],
               'donors': [p[0] for p in path if p[1] == 'donor'], 'path_weight': prob}



# Missplicing Detection
def find_ss_changes(ref_dct, mut_dct, known_splice_sites, threshold=0.5):
    '''
    :param ref_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the reference sequence
    :param mut_dct:  the spliceai probabilities for each nucleotide (by genomic position) as a dictionary for the mutated sequence
    :param known_splice_sites: the indices (by genomic position) that serve as known splice sites
    :param threshold: the threshold for detection (difference between reference and mutated probabilities)
    :return: two dictionaries; discovered_pos is a dictionary containing all the positions that meat the threshold for discovery
            and deleted_pos containing all the positions that meet the threshold for missing and the condition for missing
    '''

    new_dict = {v: mut_dct.get(v, 0) - ref_dct.get(v, 0) for v in
                list(set(list(ref_dct.keys()) + list(mut_dct.keys())))}

    discovered_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct[k]), 3), 'reference': round(ref_dct[k], 3)} for k, v in
                      new_dict.items() if v >= threshold} # and k not in known_splice_sites}   # if (k not in known_splice_sites and v >= threshold) or (v > 0.45)}

    deleted_pos = {k: {'delta': round(float(v), 3), 'absolute': round(float(mut_dct.get(k, 0)), 3), 'reference': round(ref_dct[k], 3)} for k, v in
                   new_dict.items() if -v >= threshold} # and k in known_splice_sites}      #if k in known_splice_sites and v <= -threshold}

    return discovered_pos, deleted_pos


def find_transcript_missplicing(transcript, mutations, context=5000, window=2500, threshold=0.5, engine='spliceai', just_ss=False):
    from functools import reduce
    ref = transcript.pre_mrna
    var = reduce(lambda acc, mutation: acc + mutation, mutations, ref)
    center = int(np.mean([mutation.position for mutation in mutations]) // 1)
    total_context = context + window
    length = ref.seqmat.shape[-1]
    center_index = ref.rel_pos(center)
    ref_start_pad = max(0, total_context - center_index)
    ref_end_pad = max(0, total_context - (length - center_index))

    length = var.seqmat.shape[-1]
    center_index = var.rel_pos(center)
    var_start_pad = max(0, total_context - center_index)
    var_end_pad = max(0, total_context - (length - center_index))

    ref = ref.inspect(center, context=total_context)
    var = var.inspect(center, context=total_context)

    ref_indices = np.concatenate([np.zeros(ref_start_pad), ref.indices, np.zeros(ref_end_pad)])
    mut_indices = np.concatenate([np.zeros(var_start_pad),  var.indices, np.zeros(var_end_pad)])

    ref_indices = ref_indices[context:-context]
    mut_indices = mut_indices[context:-context]

    ref_seq = 'N'*ref_start_pad + ref.seq + 'N'*ref_end_pad
    var_seq = 'N'*var_start_pad + var.seq + 'N'*var_end_pad

    print(len(ref_seq))

    if engine == 'spliceai':
        from .spliceai_utils import sai_predict_probs, sai_models
        ref_seq_acceptor_probs, ref_seq_donor_probs = sai_predict_probs(ref_seq, models=sai_models)
        mut_seq_acceptor_probs, mut_seq_donor_probs = sai_predict_probs(var_seq, models=sai_models)

    elif engine == 'pangolin':
        from .pangolin_utils import pangolin_predict_probs, pang_models
        ref_seq_donor_probs, ref_seq_acceptor_probs = pangolin_predict_probs(ref_seq, models=pang_models, just_ss=just_ss)
        mut_seq_donor_probs, mut_seq_acceptor_probs = pangolin_predict_probs(var_seq, models=pang_models, just_ss=just_ss)

    else:
        raise ValueError(f"{engine} not implemented")

    visible_donors = np.intersect1d(transcript.donors, ref_indices)
    visible_acceptors = np.intersect1d(transcript.acceptors, ref_indices)

    assert len(ref_indices) == len(ref_seq_acceptor_probs), f'Reference pos ({len(ref_indices)}) not the same as probs ({len(ref_seq_acceptor_probs)})'
    assert len(mut_indices) == len(mut_seq_acceptor_probs), f'Mut pos ({len(mut_indices)}) not the same as probs ({len(mut_seq_acceptor_probs)})'

    iap, dap = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_acceptor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_acceptor_probs))},
                               visible_acceptors,
                               threshold=threshold)

    assert len(ref_indices) == len(ref_seq_donor_probs), 'Reference pos not the same'
    assert len(mut_indices) == len(mut_seq_donor_probs), 'Mut pos not the same'

    idp, ddp = find_ss_changes({p: v for p, v in list(zip(ref_indices, ref_seq_donor_probs))},
                               {p: v for p, v in list(zip(mut_indices, mut_seq_donor_probs))},
                               visible_donors,
                               threshold=threshold)

    ref_acceptors = {a: b for a, b in list(zip(ref_indices, ref_seq_acceptor_probs))}
    ref_donors = {a: b for a, b in list(zip(ref_indices, ref_seq_donor_probs))}

    lost_acceptors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_acceptors[p]), 3)} for p in
                      visible_acceptors if p not in mut_indices and p not in dap}
    lost_donors = {int(p): {'absolute': np.float64(0), 'delta': round(float(-ref_donors[p]), 3)} for p in visible_donors
                   if p not in mut_indices and p not in ddp}
    dap.update(lost_acceptors)
    ddp.update(lost_donors)

    missplicing = {'missed_acceptors': dap, 'missed_donors': ddp, 'discovered_acceptors': iap, 'discovered_donors': idp}
    missplicing = {outk: {float(k): v for k, v in outv.items()} for outk, outv in missplicing.items()}
    temp =  {outk: {int(k) if k.is_integer() else k: v for k, v in outv.items()} for outk, outv in missplicing.items()}
    return temp


class Missplicing:
    def __init__(self, splicing_dict, threshold=0.5):
        self.missplicing = splicing_dict
        self.threshold = threshold

    # def __repr__(self):
    #     return f'Missplicing({self.modification.mut_id}) --> {self.missplicing}'

    def __str__(self):
        return self.aberrant_splicing

    def __bool__(self):
        if self.apply_sai_threshold_alt() is not None:
            return True
        return False

    def __iter__(self):
        vals = [0]
        for event, details in self.missplicing.items():
            for e, d in details.items():
                vals.append(d['delta'])
        return iter(vals)

    # def __eq__(self, alt_splicing):
    #     flag, _ = self.check_splicing_difference(self.missplicing, alt_splicing, self.threshold)
    #     return not flag

    @property
    def aberrant_splicing(self):
        return self.apply_sai_threshold(self.threshold)

    def apply_sai_threshold(self, threshold=None):
        splicing_dict = self.missplicing
        if not threshold:
            threshold = self.threshold

        new_dict = {}
        for event, details in self.missplicing.items():
            in_dict = {}
            for e, d in details.items():
                if abs(d['delta']) >= threshold:
                    in_dict[e] = d
                    # return splicing_dict
            new_dict[event] = in_dict
        return new_dict

    def apply_sai_threshold_alt(self, splicing_dict=None, threshold=None):
        splicing_dict = self.missplicing if not splicing_dict else splicing_dict
        threshold = self.threshold if not threshold else threshold
        for event, details in splicing_dict.items():
            for e, d in details.items():
                if abs(d['delta']) >= threshold:
                    return splicing_dict
        return None

    def get_max_missplicing_delta(self):
        max_delta = 0
        for event, details in self.missplicing.items():
            for e, d in details.items():
                if abs(d['delta']) > max_delta:
                    max_delta = abs(d['delta'])
        return max_delta


def find_transcript_splicing(transcript, engine='spliceai'):
    ref = transcript.pre_mrna
    ref_start_pad = 5000
    ref_end_pad = 5000

    ref_indices = ref.indices
    ref_seq = 'N' * ref_start_pad + ref.seq + 'N' * ref_end_pad
    if engine == 'spliceai':
        from .spliceai_utils import sai_predict_probs, sai_models
        ref_seq_acceptor_probs, ref_seq_donor_probs = sai_predict_probs(ref_seq, sai_models)

    elif engine == 'pangolin':
        from .pangolin_utils import pangolin_predict_probs, pang_models
        ref_seq_donor_probs, ref_seq_acceptor_probs = pangolin_predict_probs(ref_seq, models=pang_models)

    else:
        raise ValueError(f"{engine} not implemented")

    assert len(ref_seq_donor_probs) == len(ref_indices), f'{len(ref_seq_donor_probs)}  vs. {len(ref_indices)}'
    donor_probs = {i: p for i, p in list(zip(ref_indices, ref_seq_donor_probs))}
    donor_probs = dict(sorted(donor_probs.items(), key=lambda item: item[1], reverse=True))

    acceptor_probs = {i: p for i, p in list(zip(ref_indices, ref_seq_acceptor_probs))}
    acceptor_probs = dict(sorted(acceptor_probs.items(), key=lambda item: item[1], reverse=True))
    return donor_probs, acceptor_probs


def benchmark_splicing(gene, organism='hg38', engine='spliceai'):
    gene = Gene(gene, organism=organism)
    transcript = gene.transcript()
    if len(transcript.introns) == 0:
        return None, None

    transcript.generate_pre_mrna()
    predicted_donor_sites, predicted_acceptor_sites = find_transcript_splicing(transcript, engine=engine)
    num_introns = len(transcript.introns)
    predicted_donors = list(predicted_donor_sites.keys())[:num_introns]
    predicted_acceptors = list(predicted_acceptor_sites.keys())[:num_introns]
    correct_donor_preds = [v for v in predicted_donors if v in transcript.donors]
    correct_acceptor_preds = [v for v in predicted_acceptors if v in transcript.acceptors]
    return len(correct_donor_preds) / num_introns, len(correct_acceptor_preds) / num_introns, len(transcript.introns)


def missplicing(mut_id, splicing_threshold=0.5, primary_transcript=True, organism='hg38', engine='spliceai'):
    gene = Gene(mut_id.split(':')[0], organism=organism)
    mutation = get_mutation(mut_id, rev=gene.rev)
    results = {}

    for tid, transcript in gene.run_transcripts():
        # if not transcript.primary_transcript and primary_transcript:
        #     continue
        #
        if mutation not in transcript:
            continue

        good_tid = tid

        transcript.generate_pre_mrna()
        results[tid] = Missplicing(find_transcript_missplicing(transcript, mutation, engine=engine),
                                   threshold=splicing_threshold)

    # if len(results) == 0:
    #     return None
    #
    # if primary_transcript and good_tid in results:
    #     return results[good_tid]
    # else:
    #     return None

    return results


import sqlite3
import json

def get_or_compute_splicing(tool, gene, mutation_id, transcript_id, force_recompute=False):
    conn = sqlite3.connect(os.path.join(tool_parameters['splicing_db'], 'mutation_data.db'))
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS mutations (
                         tool TEXT,
                         gene TEXT,
                         mutation_id TEXT, 
                         transcript_id TEXT, 
                         data TEXT,
                         PRIMARY KEY (tool, gene, mutation_id, transcript_id)
                      )''')

    # Look up entry
    cursor.execute('SELECT data FROM mutations WHERE tool=? AND gene=? AND mutation_id=? AND transcript_id=?',
                   (tool, gene, mutation_id, transcript_id))
    row = cursor.fetchone()

    # If entry is found and force_recompute is False, return data
    if row and not force_recompute:
        return json.loads(row[0])

    # Otherwise, compute the dictionary
    computed_data = find_transcript_missplicing(tool, mutation_id, transcript_id)  # Replace with actual function

    # Store in the database
    data_json = json.dumps(computed_data)
    cursor.execute('REPLACE INTO mutations (tool, mutation_id, transcript_id, data) VALUES (?, ?, ?, ?)',
                   (tool, mutation_id, transcript_id, data_json))
    conn.commit()
    conn.close()

    return computed_data