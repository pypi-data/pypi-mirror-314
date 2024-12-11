
import pandas as pd
import random
from pathlib import Path
from tqdm import tqdm

class TCGACase:
    def __init__(self, df):
        # Here we get a dataframe of mutations within a gene
        self.df = df
        self.calculate_vaf()
        self.space_variants(spacer_size=50)
        self.case_id = df.case_id.tolist()[0]

    def space_variants(self, spacer_size=100, group_likelihood_threshold=0):
        df = self.df
        if df.empty:
            df['group'] = 0
            return self
        values = sorted(df.Start_Position.unique().tolist())
        # groups = [list(group) for key, group in groupby(values, key=lambda x: (x - values[values.index(x) - 1] >
        # spacer_size) if values.index(x) > 0 else False)] Initialize variables
        groups = []
        current_group = []

        # Iterate through the values
        for i in range(len(values)):
            if i == 0:
                current_group.append(values[i])
            else:
                if values[i] - values[i - 1] <= spacer_size:
                    current_group.append(values[i])
                else:
                    groups.append(current_group)
                    current_group = [values[i]]

        # Append the last group if it's not empty
        if current_group:
            groups.append(current_group)

        df.loc[:, 'group'] = 0
        for i, g in enumerate(groups):
            df.loc[df.Start_Position.isin(g), 'group'] = i
        self.df = df
        return self

    def calculate_vaf(self):
        df = self.df
        df = df[df.t_depth > 0]
        df.loc[:, 'vaf'] = df.apply(lambda row: row.t_alt_count / row.t_depth, axis=1)
        self.df = df
        return self

    def find_overlayed_variants(self):
        df = self.df
        mut_counts = df.mut_id.value_counts()
        mut_counts = mut_counts[mut_counts > 1].index

        small_df = df.groupby('mut_id', as_index=False).agg({
            't_depth': 'sum',
            't_alt_count': 'sum',
            't_ref_count': 'sum',
        })

        df = df.drop_duplicates(subset='mut_id', keep='first')

        small_df = small_df[small_df.t_depth > 0]
        small_df['vaf'] = small_df.t_alt_count / small_df.t_depth

        small_df = small_df.set_index('mut_id')
        df.set_index('mut_id', inplace=True)
        df.update(small_df)
        df.reset_index(inplace=True)
        self.df = df
        return self

    def find_epistasis(self, pth=3, rth=0):
        df = self.df
        if df.empty:
            return None
        # df = df[df.t_alt_count > rth].sort_values('Start_Position', ascending=True)
        df = df[(df.t_alt_count > df.t_ref_count / pth) & (df.t_alt_count >= rth)].sort_values('Start_Position',
                                                                                               ascending=True)

        # display(df[['mut_id', 't_alt_count', 't_ref_count']])

        # Group by the group_key
        grouped = df.groupby('group').agg({
            'mut_id': lambda x: '|'.join(x),
            't_alt_count': 'mean',
            't_ref_count': 'mean',
            'case_id': 'first'
        }).reset_index(drop=True)

        # Drop the group_key column
        return grouped[grouped.mut_id.str.contains('\|')][['mut_id', 't_alt_count', 't_ref_count', 'case_id']]


class TCGAGene:
    def __init__(self, gene, cancer_path=Path('/tamir2/cancer_proj/gdc_db/data/filtered_feb_2021/AllGenes/'),
                 valid_cases=None, extra_cols=[], exclude_filters=None, include_filter=None):
        file_path = cancer_path / gene / 'GeneMutTble.txt'
        if not file_path.exists():
            self.df = pd.DataFrame()

        else:
            df = pd.read_csv(file_path,
                             usecols=['Variant_Type', 'FILTER', 'vcf_tumor_gt', 'vcf_normal_gt',
                                      'COSMIC', 't_depth', 't_ref_count', 't_alt_count', 'Proj_name',
                                      'HGVSc', 'Chromosome', 'Start_Position', 'Reference_Allele',
                                      'Tumor_Seq_Allele2', 'case_id', 'Gene_name', 'Variant_Type',
                                      'Variant_Classification'] + extra_cols,
                             low_memory=False).sort_values('Start_Position', ascending=True)

            df['attention'] = True

            if df.empty:
                self.df = df

            else:
                df = df[df.Variant_Type.isin(['SNP', 'INS', 'DEL'])]
                df = df.astype({'Start_Position': int})

                if include_filter is not None:
                    # df = df[df.FILTER == include_filter]
                    df.loc[~df['FILTER'].str.contains(include_filter), 'attention'] = False

                elif exclude_filters is not None:
                    for exclude_filter in exclude_filters:
                        # df = df[~df.FILTER.str.contains(exclude_filter)]
                        df.loc[df['FILTER'].str.contains(exclude_filter), 'attention'] = False

                if valid_cases is not None:
                    # df = df[df.case_id.isin(valid_cases)]
                    df.loc[~df.case_id.isin(valid_cases), 'attention'] = False

                df['mut_id'] = df.apply(lambda
                                            row: f"{row.Gene_name}:{row.Chromosome.replace('chr', '')}:{row.Start_Position}:{row.Reference_Allele}:{row.Tumor_Seq_Allele2}",
                                        axis=1)
                df['mut_id_yoram'] = df.apply(lambda
                                                  row: f"{row.Gene_name}:{row.Chromosome}:{row.Variant_Classification}:{row.Start_Position}:{row.Reference_Allele}:{row.Tumor_Seq_Allele2}",
                                              axis=1)
                silent_mut_classes = ["3'Flank", "3'UTR", "Silent", "Splice_Site", "Splice_Region", "Intron", "5'Flank",
                                      "3'Flank"]
                df['silent'] = df.apply(lambda row: row.Variant_Classification in silent_mut_classes, axis=1)
                df['ratio'] = df.t_alt_count + df.t_ref_count
                df = df[df.ratio > 0]
                df['ratio'] = df.t_alt_count / df.ratio
                self.df = df

    def __repr__(self):
        return repr(self.df[self.df.attention])

    @property
    def data(self):
        return self.df[self.df.attention]

    def affected_cases(self, mut_id=None, read_ratio=0, filters=[]):
        if mut_id is None:
            return self.df.case_id.unique().tolist()
        df = self.df
        df = df[(df.mut_id == mut_id) & (df.ratio >= read_ratio)]
        for filter in filters:
            df = df[~df.FILTER.str.contains(filter)]
        return df.case_id.unique().tolist()

    def get_patient_muts(self, case_id=None, read_ratio=0, exclude_filters=None):
        if case_id is None:
            case_id = random.choice(self.affected_cases())
        return self.df[self.df.case_id == case_id]

    def get_patients_affected(self, mut_id, read_ratio=0, exclude_filters=None):
        return self.data[self.data.mut_id == mut_id].case_id.unique().tolist()


    def get_patients_unaffected(self, mut_id, must_contain_all=False, read_ratio=0, exclude_filters=None):
        # returns all patients not affected by ALL the mutation in mut id (patients containg individual mutations only allowed) unless must_contain_all= True
        pass

    def split_patients(self, mut_id, strict=True):
        # returns two lists: all patients affected by a mutation and all patients with none of the mutations (or the mutations but not togehter)
        pass

    def arrange_patients_by_project(self, mut_id):
        # returns all the patients affected by a mutation grouped by cancer project
        pass

    def total_prevalence(self, mut_id):
        pass

    def project_prevalence(self, mut_id, df_p_proc):
        mut_prevalence = {}
        for i, g in tqdm(self.data.groupby(['mut_id', 'Transcript_ID'])):
            mut_prevalence[i] = series_to_pretty_string((df_p_proc[g.case_id].value_counts() / project_counts).dropna())
        return pd.Series(mut_prevalence)

    def project_counts(self, mut_id):
        pass

    def filter_silent_muts(self):
        self.df.loc[self.df.silent, 'attention'] = False
        return self


def series_to_pretty_string(series):
    # Format each index-value pair, applying scientific notation to floats with 3 significant figures
    pretty_str = "\n".join([
        f"{index}: {value:.3e}" if isinstance(value, float) else f"{index}: {value}"
        for index, value in series.items()
    ])
    return pretty_str


# CLINICAL_DATA_FILE = Path('/tamir2/nicolaslynn/data/TCGA/cancer_reports/new_df_p_proc.pkl')
# CLINICAL_DATA_FILE = Path('/tamir2/yoramzar/Projects/Cancer_mut/Explore_data/reports/df_p_all.pkl')
# CANCER_DATA_PATH = Path('/tamir2/cancer_proj/gdc_db/data/filtered_feb_2021/AllGenes')
# MAF_FILE_NAME = 'GeneMutTble.txt'
# CASE_TRACKER = pd.read_csv('/tamir2/nicolaslynn/projects/TCGAParsed/case2proj.csv', index_col=0)
# PROJ_COUNTS = CASE_TRACKER.proj.value_counts()
# OKGP_DATA_FILE = Path('/tamir2/nicolaslynn/projects/1000GenomesProjMutations/parsed_1kgp_mutations_in_target_genes.csv')
# MUTATION_FREQ_DF = pd.read_csv(OKGP_DATA_FILE, index_col=0)
# PROTEIN_ANNOTATIONS = pd.read_csv('/tamir2/nicolaslynn/data/BioMart/protein_annotations.csv').rename(columns={'Interpro start': 'start', 'Interpro end': 'end', 'Interpro Short Description': 'name'})[['Gene stable ID', 'Transcript stable ID', 'start', 'end', 'name']]
# PROTEIN_ANNOTATIONS['length'] = PROTEIN_ANNOTATIONS.apply(lambda row: abs(row.start - row.end), axis=1)

# def prepare_gene_sets():
#     # gene_annotations_file = Path('/tamir2/nicolaslynn/data/COSMIC/cancer_gene_roles.csv')
#     # GENE_DF = pd.read_csv(gene_annotations_file, index_col=0)
#     # all_oncogenes = GENE_DF[GENE_DF.OG==True].index.tolist()
#     # all_oncogenes = list(set(all_oncogenes))
#     return [], [], []
#
# CLIN_DF = prepare_clinical_data()
# TSGS, ONCOGENES, CANCER_GENES = prepare_gene_sets()
#
#
# def generate_survival_quantitative(affected_df, nonaffected_df):
#     if affected_df.empty or nonaffected_df.empty:
#         return np.nan, np.nan, np.nan
#     results = logrank_test(affected_df['duration'], nonaffected_df['duration'],
#                            event_observed_A=affected_df['event'],
#                            event_observed_B=nonaffected_df['event'])
#     p_value = results.p_value
#     kmf = KaplanMeierFitter()
#     kmf.fit(affected_df['duration'], affected_df['event'], label=f'With Epistasis ({len(affected_df)})')
#     times, surv_probs = kmf.survival_function_.index.values, kmf.survival_function_.values.flatten()
#     auc1 = np.trapz(surv_probs, times)
#     kmf.fit(nonaffected_df['duration'], nonaffected_df['event'], label=f'Without Epistasis ({len(nonaffected_df)})')
#     times, surv_probs = kmf.survival_function_.index.values, kmf.survival_function_.values.flatten()
#     auc2 = np.trapz(surv_probs, times)
#     return p_value, auc1, auc2
#
# def generate_survival_pvalue(affected_df, unaffected_df):
#     results = logrank_test(affected_df['duration'], unaffected_df['duration'],
#                            event_observed_A=affected_df['event'],
#                            event_observed_B=unaffected_df['event'])
#
#     p_value = results.p_value
#     kmf = KaplanMeierFitter()
#     # Fit data
#     kmf.fit(affected_df['duration'], affected_df['event'], label=f'Without Epistasis ({len(affected_df)})')
#     ax = kmf.plot()
#
#     kmf.fit(unaffected_df['duration'], unaffected_df['event'], label=f'With Epistasis ({len(unaffected_df)})')
#     kmf.plot(ax=ax)
#     plt.text(5, 0.95, f'pval: {p_value:.3e}')
#     plt.show()
#     return p_value
#
# def get_project_prevalence(cases_affected):
#     ca = [c for c in cases_affected if c in CASE_TRACKER.index]
#     prevalences = CASE_TRACKER.loc[ca].proj.value_counts() / PROJ_COUNTS
#     prevalences.fillna(0, inplace=True)
#     prevalences = prevalences[[i for i in prevalences.index if 'TCGA' in i]]
#     prevalences.index = [s.replace('TCGA', 'prev') for s in prevalences.index]
#     return prevalences
#
# def get_project_counts(cases_affected):
#     ca = [c for c in cases_affected if c in CASE_TRACKER.index]
#     prevalences = CASE_TRACKER.loc[ca].proj.value_counts()
#     prevalences = prevalences[[i for i in prevalences.index if 'TCGA' in i]]
#     prevalences.index = [s.replace('TCGA_', '') for s in prevalences.index]
#     return prevalences
#
# def get_event_consequence(df):
#     assert df.Transcript_ID.nunique() == 1, 'Too many transcripts to return a single consequenc.'
#     return df.iloc[0].Consequence
#
# def get_dbSNP_id(df):
#     return df.iloc[0].dbSNP_RS
#
# def load_variant_file(gene):
#     df = pd.read_csv(CANCER_DATA_PATH / gene / MAF_FILE_NAME, low_memory=False)
#     df['mut_id'] = df.apply(lambda row: f"{row.Gene_name}:{row.Chromosome.replace('chr', '')}:{row.Start_Position}:{row.Reference_Allele}:{row.Tumor_Seq_Allele2}", axis=1)
#     return df
#
# def find_event_data(event):
#     df = load_variant_file(event.gene)
#     if df.empty:
#         return None
#
#     df = df.query \
#         ('Chromosome == @event.chromosome & Start_Position == @event.start & Reference_Allele == @event.ref & Tumor_Seq_Allele2 == @event.alt')
#
#     if df.empty:
#         return None
#
#     if event.transcript_id is not None:
#         df = df[df.Transcript_ID == event.transcript_id]
#     df['mut_id'] = event.event_id
#     return df
#
#
# class GEvent:
#     def __init__(self, event_id, transcript_id=None):
#         self.gene, self.chromosome, self.start, self.ref, self.alt = event_id.split(':')
#         self.transcript_id = transcript_id
#         self.chromosome = f'chr{self.chromosome}'
#         self.start = int(self.start)
#         self.event_id = event_id
#
#
#
# def get_okgp_mutation_frequency(mut_id):
#     if mut_id in MUTATION_FREQ_DF.index:
#         return MUTATION_FREQ_DF.loc[mut_id].cases_affected
#     else:
#         return 0
#
# def get_df_filter_info(df):
#     filter_artifact_values: list = ["oxog", "bPcr", "bSeq"]
#     MuTect2_filters: list = ['Germline risk', 't_lod_fstar', 'alt_allele_in_normal', 'panel_of_normals', 'clustered_events',
#                              'str_contraction', 'multi_event_alt_allele_in_normal', 'homologous_mapping_event', 'triallelic_site']
#     filter_col_name: str = "FILTER_info"  # column name to add to the dataframe
#     filter_info_list: list = []
#     f_cnr_info = {}
#
#     for j, (prj, df_prj) in enumerate(df.groupby('Proj_name')):
#         filter_vals = list(df_prj['FILTER'])
#         num_pass, num_artifacts, num_mutect2_filters = 0, 0, 0
#         for filter_val in filter_vals:
#             num_pass += ('PASS' in filter_val)
#             num_artifacts += any([x in filter_val for x in filter_artifact_values])
#             num_mutect2_filters += any([x in filter_val for x in MuTect2_filters])
#         num_rest = max(0, (len(filter_vals) - num_pass - num_artifacts - num_mutect2_filters))
#         f_cnr_info[str(prj)[5:]] = (num_pass, num_mutect2_filters, num_artifacts, num_rest)
#     return f_cnr_info
#
# def yoram_mutid(row):
#     return f'{row.Gene_name}:{row.Chromosome}:{row.Consequence}:{row.Start_Position}:{row.Reference_Allele}:{row.Tumor_Seq_Allele2}'
#
#
# def annotate_level_two(mut_id, tid):
#     mut = GEvent(mut_id, tid)
#     df = find_event_data(mut)
#
#     if df.empty or df is None:
#         return None
#
#     patients_affected = df.cases_affected.unique().tolist()
#     p_val, auc_a, auc_n = generate_survival_quantitative(CLIN_DF[CLIN_DF.case_id.isin(patients_affected)], CLIN_DF[~CLIN_DF.case_id.isin(patients_affected)])
#     project_prevalences = get_project_prevalence(patients_affected)
#     prev_dict = project_prevalences.to_dict().sort()
#     project_counts = get_project_counts(patients_affected)
#
#     s = pd.Series({
#         'mut_id': mut_id,
#         'yoram_mut_id': yoram_mutid(df.iloc[0]),
#         'transcript_id': tid,
#         'affected_cases': len(patients_affected),
#         'dbSNP_id': get_dbSNP_id(df),
#         'consequence': get_event_consequence(df),
#         'survival_p_value': p_val,
#         'auc_affected': auc_a,
#         'auc_nonaffected': auc_n,
#         'TSG': contains(TSGS, mut.gene),
#         'oncogene': contains(ONCOGENES, mut.gene),
#         'cases_1kgp': get_okgp_mutation_frequency(mut.event_id),
#         'filter_inf': get_df_filter_info(df),
#         'strand': df.Strand.unique().tolist()[0],
#         'prevalences': prev_dict
#     })
#
#     s['max_prev'] = project_prevalences.max()
#     s['rel_proj'] = ','.join([c.split('_')[-1] for c in project_prevalences[project_prevalences == project_prevalences.max()].index.tolist()])
#     s = pd.concat([s, project_prevalences, project_counts])
#     del df
#     return s
#
# def get_mut_counts():
#     cases = unload_json('/tamir2/nicolaslynn/projects/TCGAParsed/recurring_single_muts_tcga.json')
#     cases = pd.Series(cases)
#     cases.name = 'num_cases'
#     cases.index.name = 'mut_id'
#     cases = cases.to_frame()
#     cases.reset_index(inplace=True)
#     return cases
#
#
def create_mut_id(row):
    return f"{row.Gene_name}:{row['Chromosome']}:{row['Start_Position']}:{row['Reference_Allele']}:{row['Tumor_Seq_Allele2']}"
#
#
# def is_in_exon(mut_id, tid):
#     from geney.Gene import Gene
#     transcript = Gene(mut_id.split(':')[0]).generate_transcript(tid)
#     return int(mut_id.split(':')[2]) in transcript.exonic_indices
