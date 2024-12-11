import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
# from scipy.integrate import trapezoid
from geney.utils import unload_pickle, unload_json, contains
from lifelines.exceptions import ConvergenceError
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines import CoxPHFitter

pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None


def prepare_clinical_data(df=None):
    if df is None:
        CLINICAL_DATA_FILE = Path('/tamir2/yoramzar/Projects/Cancer_mut/Explore_data/reports/df_p_all.pkl')
        df = unload_pickle(CLINICAL_DATA_FILE)

    df.rename(columns={'patient_uuid': 'case_id'}, inplace=True)
    cols = list(df.columns)
    cols_days_to_followup = [col for col in cols if 'days_to_followup' in col] + [col for col in cols if 'days_to_last_followup' in col]
    cols_days_to_know_alive = [col for col in cols if 'days_to_know_alive' in col] + [col for col in cols if 'days_to_last_known_alive' in col]
    cols_days_to_death = [col for col in cols if 'days_to_death' in col]
    cols_duration = cols_days_to_followup + cols_days_to_know_alive + cols_days_to_death
    col_vital_status = 'days_to_death'
    event_col_label = 'event'
    duration_col_label = 'duration'
    df.insert(1, event_col_label, df.apply(lambda x: int(not np.isnan(x[col_vital_status])), axis=1))
    df.insert(1, duration_col_label, df.apply(lambda x: max([x[col] for col in cols_duration if not np.isnan(x[col])], default=-1), axis=1))
    df[duration_col_label] /= 365
    df = df.query(f"{duration_col_label}>=0.0")[['duration', 'event', 'case_id', 'chemotherapy', 'hormone_therapy', 'immunotherapy', 'targeted_molecular_therapy', 'Proj_name']]
    # df.to_csv('/tamir2/nicolaslynn/data/tcga_metadata/tcga_clinical_data.csv')
    return df


class SurvivalAnalysis:
    def __init__(self, clindf=None):
        self.clindf = prepare_clinical_data(clindf)
        self.treatment_features = ['chemotherapy', 'hormone_therapy', 'immunotherapy', 'targeted_molecular_therapy']
        self.df = self.clindf.copy()
        self.df['group'] = 0
        self.df.fillna(0, inplace=True)
        self.treatment_features = ['chemotherapy', 'hormone_therapy', 'immunotherapy', 'targeted_molecular_therapy']

    def generate_clinical_dataframe(self, target_cases, control_cases=None, inplace=False, features_of_interest=[]):
        df = self.df.copy()
        df.loc[df[df.case_id.isin(target_cases)].index, 'group'] = 2
        if control_cases is not None:
            df.loc[df[df.case_id.isin(control_cases)].index, 'group'] = 1

        df = df[df.group > 0]
        df.group -= 1
        core_features = ['duration', 'event']
        df = df[core_features + features_of_interest]

        for col in self.treatment_features:
            if col not in df:
                continue
            df.loc[df[col] > 0, col] = 1

        df = df[core_features + [col for col in features_of_interest if
                                 df[col].nunique() > 1]]  # and df[col].value_counts(normalize=True).min() >= 0.01]]
        return df

    def kaplan_meier_analysis(self, df, control_label='Unaffected Patients', target_label='Affected Patients', feature='group', plot=False, title=None, time_cap=False, savepath=None, figsize=(7, 3), tmb_p_value=None):
        # Can only be performed on features with two unique values
        cap_time = df.groupby(feature).duration.max().min()
        # df['duration'] = df['duration'].clip(upper=cap_time)
        auc_vals = []
        results = pd.Series()
        count = 0
        for val in [0, 1]:
            g = df[df[feature] == val]
            kmf = KaplanMeierFitter()
            label = f"{control_label} ({len(g)} cases)" if val == 0 else f"{target_label} ({len(g)} cases)"
            if val == 0:
                results[control_label] = len(g)
            else:
                results[target_label] = len(g)

            kmf.fit(g['duration'], g['event'], label=label)
            surv_func = kmf.survival_function_
            filtered_surv_func = surv_func[surv_func.index <= cap_time]
            auc = np.trapz(filtered_surv_func[label], filtered_surv_func.index)
            # auc = trapz(surv_func[label], surv_func.index)
            auc_vals.append(auc)
            if plot:
                if count == 0:
                    fig, ax = plt.subplots(figsize=figsize)
                    kmf.plot_survival_function(ax=ax, ci_show=True, color="#2430e0", lw=2)
                else:
                    kmf.plot_survival_function(ax=ax, ci_show=True, color="#e60215", lw=2)
                count += 1

        p_value = self.log_rank(df[df[feature] == 1], df[df[feature] == 0])

        if plot:
            ax.text(0.6, 0.6, rf'Survival $p{{v}}$: {p_value:.3e}', transform=ax.transAxes, fontsize=10,
                    horizontalalignment='left')
            if tmb_p_value:
                ax.text(0.6, 0.53, rf'TMB $p{{v}}$: {tmb_p_value:.3e}', transform=ax.transAxes, fontsize=10,
                        horizontalalignment='left')
            # Grid and spines
            ax.grid(True, which="major", linestyle="--", linewidth=0.5, color="grey", alpha=0.7)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.tick_params(axis="both", which="major", labelsize=10)
            if title:
                ax.set_title(title, fontsize=12)
            legend = ax.legend(fontsize=9, loc='best', frameon=True)
            legend.get_frame().set_facecolor('white')  # Set the background color to white
            legend.get_frame().set_edgecolor('black')  # Set the edge color to black
            plt.xlabel('Time (years)')
            plt.ylabel('Survival Probability')
            if time_cap:
                plt.xlim([0, cap_time])
            plt.tight_layout()
            if savepath is not None:
                plt.savefig(savepath, bbox_inches='tight', dpi=300)
            plt.show()

        results['p_value'] = p_value
        results['auc_target'] = auc_vals[-1]
        if len(auc_vals) > 1:
            results['auc_delta'] = auc_vals[-1] - auc_vals[0]
            results['auc_control'] = auc_vals[0]

        return results

    def log_rank(self, group1, group2):
        return logrank_test(group1['duration'], group2['duration'],
                            event_observed_A=group1['event'],
                            event_observed_B=group2['event']).p_value

    def perform_cox_analysis(self, df, features_of_interest):
        # Very simple... will return a series with p values for each feature
        try:
            return CoxPHFitter().fit(df[features_of_interest + ['duration', 'event']], 'duration', 'event').summary.p
        except ConvergenceError:
            print("Convergence Error")
            return pd.Series()
