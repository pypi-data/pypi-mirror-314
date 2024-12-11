import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from collections import namedtuple
from geney.utils import unload_pickle, contains, unload_json, dump_json


### Graphical Stuff
def create_figure_story(epistasis, to_file=None):
    g = epistasis.split(':')[0]
    out = oncosplice(epistasis, annotate=True)
    out = out[out.cons_available==1]

    for _, row in out.iterrows():
        max_length = 0
        pos = 0
        for i, k in row.deletions.items():
            if len(k) > max_length:
                pos = i
                max_length = len(k)

        if max_length > 5:
            del_reg = [pos, pos + max_length]
        else:
            del_reg = None

        if row.oncosplice_score == 0:
            mutation_loc = None
        else:
            mutation_loc = pos

        plot_conservation(tid=row.transcript_id,
                          gene=f'{g}, {row.transcript_id}.{row.isoform}',
                          mutation_loc=mutation_loc,
                          target_region=del_reg, mut_name='Epistasis',
                          domain_annotations=get_annotations(row.transcript_id, 300),
                          to_file=to_file)



def plot_conservation(gene_name, tid, gene='', mutation_loc=None, target_region=None, mut_name='Mutation', domain_annotations=[]):
    """
    Plots conservation vectors with protein domain visualization and Rate4Site scores.

    Parameters:
    tid (str): Transcript identifier.
    gene (str): Gene name.
    mutation_loc (int): Position of the mutation.
    target_region (tuple): Start and end positions of the target region.
    mut_name (str): Name of the mutation.
    domain_annotations (list): List of tuples for domain annotations (start, end, label).
    """
    # Access conservation data
    _, cons_vec = unload_pickle(gene_name)['tid']['cons_vector']

    if not cons_vec:
        raise ValueError("The conservation vector is empty.")

    sns.set_theme(style="white")
    fig, ax = plt.subplots(figsize=(max(15, len(cons_vec)/10), 3))  # Dynamic figure size

    # Plotting the conservation vectors in the main plot
    plot_conservation_vectors(ax, cons_vec)

    # Setting up primary axis for the main plot
    setup_primary_axis(ax, gene, len(cons_vec))

    # Create a separate axes for protein domain visualization
    domain_ax = create_domain_axes(fig, len(cons_vec))

    # Draw protein domains
    plot_protein_domains(domain_ax, domain_annotations, len(cons_vec))

    # Plotting Rate4Site scores on secondary y-axis
    plot_rate4site_scores(ax, cons_vec)

    # Plotting mutation location and target region, if provided
    plot_mutation_and_target_region(ax, mutation_loc, target_region, mut_name)

    plt.show()

def plot_conservation_vectors(ax, cons_vec):
    """Plots transformed conservation vectors."""
    temp = transform_conservation_vector(cons_vec, 76)  # Larger window
    temp /= max(temp)
    ax.plot(list(range(len(temp))), temp, c='b', label='Estimated Functional Residues')

    temp = transform_conservation_vector(cons_vec, 6)   # Smaller window
    temp /= max(temp)
    ax.plot(list(range(len(temp))), temp, c='k', label='Estimated Functional Domains')

def setup_primary_axis(ax, gene, length):
    """Configures the primary axis of the plot."""
    ax.set_xlabel(f'AA Position - {gene}', weight='bold')
    ax.set_xlim(0, length)
    ax.set_ylim(0, 1)
    ax.set_ylabel('Relative Importance', weight='bold')
    ax.tick_params(axis='y')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def create_domain_axes(fig, length):
    """Creates an axis for protein domain visualization."""
    domain_ax_height = 0.06
    domain_ax = fig.add_axes([0.125, 0.95, 0.775, domain_ax_height])
    domain_ax.set_xlim(0, length)
    domain_ax.set_xticks([])
    domain_ax.set_yticks([])
    for spine in domain_ax.spines.values():
        spine.set_visible(False)
    return domain_ax

def plot_protein_domains(ax, domain_annotations, length):
    """Plots protein domain annotations."""
    ax.add_patch(Rectangle((0, 0), length, 0.9, facecolor='lightgray', edgecolor='none'))
    for domain in domain_annotations:
        start, end, label = domain
        ax.add_patch(Rectangle((start, 0), end - start, 0.9, facecolor='orange', edgecolor='none', alpha=0.5))
        ax.text((start + end) / 2, 2.1, label, ha='center', va='center', color='black', size=8)

def plot_rate4site_scores(ax, cons_vec):
    """Plots Rate4Site scores on a secondary y-axis."""
    ax2 = ax.twinx()
    c = np.array(cons_vec)
    c = c + abs(min(c))
    c = c/max(c)
    ax2.set_ylim(min(c), max(c)*1.1)
    ax2.scatter(list(range(len(c))), c, color='green', label='Rate4Site Scores', alpha=0.4)
    ax2.set_ylabel('Rate4Site Normalized', color='green', weight='bold')
    ax2.tick_params(axis='y', labelcolor='green')
    ax2.spines['right'].set_visible(True)
    ax2.spines['top'].set_visible(False)

def plot_mutation_and_target_region(ax, mutation_loc, target_region, mut_name):
    """Highlights mutation location and target region, if provided."""
    if mutation_loc is not None:
        ax.axvline(x=mutation_loc, ymax=1, color='r', linestyle='--', alpha=0.7)
        ax.text(mutation_loc, 1.04, mut_name, color='r', weight='bold', ha='center')

    if target_region is not None:
        ax.add_patch(Rectangle((target_region[0], 0), target_region[1] - target_region[0], 1, alpha=0.25, facecolor='gray'))
        center_loc = target_region[0] + 0.5 * (target_region[1] - target_region[0])
        ax.text(center_loc, 1.04, 'Deleted Region', ha='center', va='center', color='gray', weight='bold')


def merge_overlapping_regions(df):
    """
    Merges overlapping regions in a DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame with columns 'start', 'end', 'name'

    Returns:
    List: List of merged regions as namedtuples (start, end, combined_name)
    """
    if df.empty:
        return []

    Region = namedtuple('Region', ['start', 'end', 'combined_name'])
    df = df.sort_values(by='start')
    merged_regions = []
    current_region = None

    for _, row in df.iterrows():
        start, end, name = row['start'], row['end'], row['name'].replace('_', ' ')
        if current_region is None:
            current_region = Region(start, end, [name])
        elif start <= current_region.end:
            current_region = Region(current_region.start, max(current_region.end, end), current_region.combined_name + [name])
        else:
            merged_regions.append(current_region._replace(combined_name=', '.join(current_region.combined_name)))
            current_region = Region(start, end, [name])

    if current_region:
        merged_regions.append(current_region._replace(combined_name=', '.join(current_region.combined_name)))

    # Assuming split_text is a function that splits the text appropriately.
    merged_regions = [Region(a, b, split_text(c, 35)) for a, b, c in merged_regions]
    return merged_regions


def split_text(text, width):
    """
    Splits a text into lines with a maximum specified width.

    Parameters:
    text (str): The text to be split.
    width (int): Maximum width of each line.

    Returns:
    str: The text split into lines of specified width.
    """
    lines = re.findall('.{1,' + str(width) + '}', text)
    return '\n'.join(lines)

def get_annotations(target_gene, w=500):
    PROTEIN_ANNOTATIONS = {}
    temp = PROTEIN_ANNOTATIONS[(PROTEIN_ANNOTATIONS['Transcript stable ID'] == PROTEIN_ANNOTATIONS[target_gene]) & (PROTEIN_ANNOTATIONS.length < w)].drop_duplicates(subset=['Interpro Short Description'], keep='first')
    return merge_overlapping_regions(temp)


# def plot_conservation(tid, gene='', mutation_loc=None, target_region=None, mut_name='Mutation', domain_annotations=[], to_file=None):
#     _, cons_vec = access_conservation_data(tid)
#
#     sns.set_theme(style="white")
#     fig, ax = plt.subplots(figsize=(15, 3))  # Adjusted figure size for better layout
#
#     # Plotting the conservation vectors in the main plot
#     temp = transform_conservation_vector(cons_vec, 76)
#     temp /= max(temp)
#     ax.plot(list(range(len(temp))), temp, c='b', label='Estimated Functional Residues')
#     temp = transform_conservation_vector(cons_vec, 6)
#     temp /= max(temp)
#     ax.plot(list(range(len(temp))), temp, c='k', label='Estimated Functional Domains')
#
#     # Setting up primary axis for the main plot
#     ax.set_xlabel(f'AA Position - {gene}', weight='bold')
#     ax.set_xlim(0, len(cons_vec))
#     ax.set_ylim(0, 1)  # Set y-limit to end at 1
#     ax.set_ylabel('Relative Importance', weight='bold')
#     ax.tick_params(axis='y')
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#
#     # Create a separate axes for protein domain visualization above the main plot
#     domain_ax_height = 0.06  # Adjust for thinner protein diagram
#     domain_ax = fig.add_axes([0.125, 0.95, 0.775, domain_ax_height])  # Position higher above the main plot
#     domain_ax.set_xlim(0, len(cons_vec))
#     domain_ax.set_xticks([])
#     domain_ax.set_yticks([])
#     domain_ax.spines['top'].set_visible(False)
#     domain_ax.spines['right'].set_visible(False)
#     domain_ax.spines['left'].set_visible(False)
#     domain_ax.spines['bottom'].set_visible(False)
#
#     # Draw the full-length protein as a base rectangle
#     domain_ax.add_patch(Rectangle((0, 0), len(cons_vec), 0.9, facecolor='lightgray', edgecolor='none'))
#
#     # Overlay domain annotations
#     for domain in domain_annotations:
#         start, end, label = domain
#         domain_ax.add_patch(Rectangle((start, 0), end - start, 0.9, facecolor='orange', edgecolor='none', alpha=0.5))
#         domain_ax.text((start + end) / 2, 2.1, label, ha='center', va='center', color='black', size=8)
#
#     # Plotting Rate4Site scores on secondary y-axis
#     ax2 = ax.twinx()
#     c = np.array(cons_vec)
#     c = c + abs(min(c))
#     c = c/max(c)
#     ax2.set_ylim(min(c), max(c)*1.1)
#     ax2.scatter(list(range(len(c))), c, color='green', label='Rate4Site Scores', alpha=0.4)
#     ax2.set_ylabel('Rate4Site Normalized', color='green', weight='bold')
#     ax2.tick_params(axis='y', labelcolor='green')
#     ax2.spines['right'].set_visible(True)
#     ax2.spines['top'].set_visible(False)
#
#     # Plotting mutation location and target region
#     if mutation_loc is not None:
#         ax.axvline(x=mutation_loc, ymax=1,color='r', linestyle='--', alpha=0.7)
#         ax.text(mutation_loc, 1.04, mut_name, color='r', weight='bold', ha='center')
#
#     if target_region is not None:
#         ax.add_patch(Rectangle((target_region[0], 0), target_region[1] - target_region[0], 1, alpha=0.25, facecolor='gray'))
#         center_loc = target_region[0] + 0.5 * (target_region[1] - target_region[0])
#         ax.text(center_loc, 1.04, 'Deleted Region', ha='center', va='center', color='gray', weight='bold')
#
#     plt.show()
#

