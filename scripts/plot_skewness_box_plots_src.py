from data_separation import *
#######################################################################################################
# read files with normalised energy anomalies
#######################################################################################################


def dict_norm_anomalies(path_f, norm_en_anom_clim_file, norm_en_anom_extr_file):
    """
    `dict_norm_anomalies(path_f, norm_en_anom_clim_file, norm_en_anom_extr_file) -> dic_clim, dic_extr`

    This function reads txt files as Dataframes and forms dictionaries for further processing.

    :param path_f
    :param norm_en_anom_clim_file
    :param norm_en_anom_extr_file
    :return: dic_clim, dic_extr
    """
    df_clim = pd.read_csv(path_f + norm_en_anom_clim_file, sep='\s+', header=None)
    df_extr = pd.read_csv(path_f + norm_en_anom_extr_file, sep='\s+', header=None)

    dic_clim = df_clim.to_dict(orient='list')
    dic_extr = df_extr.to_dict(orient='list')

    return dic_clim, dic_extr


#######################################################################################################
# visualisation of used statistical tools (PDFs, ECDFs, bootstrapping, etc.)
#######################################################################################################

def pdfs_comparison(big_list, big_list_extr, lbls, save_image, high_res=False):
    """
    `pdfs_comparison(big_list, big_list_extr, lbls, save_image, high_res=False)`

    This function takes two dictionaries as input and
    plot PDFs (Probability Distribution Functions) and KDEs (Kernel Density Estimators).

    :param big_list, big_list_extr: dictionary (one-level or nested)
    :param lbls: label for dictionary
    :param save_image: name of figure (only .eps and .png are available)
    :param high_res: boolean (True if you want to save plot as image, False - if not; False is set by default)

    ## Discussion
    This code keeps the number of bins fixed. In a future, it would be possible to change this number.
    Keep in mind that ("dumb-rule!") the number of bins is defined as 'a_num_bins = sqrt(a)'.

    """
    nrows = 1; # set how you wnt to display datasets (one- or multi-row)
    ncols = len(big_list)  # int(len(big_list)/2)
    # adjust figsize
    if high_res == True:
        f, axes = plt.subplots(nrows, ncols, sharex=True, figsize=(10, 5), dpi=300)  # 9, 2.5
    else:
        f, axes = plt.subplots(nrows, ncols, figsize=(12, 6))

    # plot KDEs over datasets
    idx = 0
    for ax in axes.flat:
        #print(idx)
        sns.kdeplot(big_list[idx],
                    label=r"All days",
                    ax=ax, color='tab:blue', fill=False, linewidth=1.5)
        sns.kdeplot(big_list_extr[idx],
                    label="EHW days",
                    ax=ax, color='crimson', fill=False, linewidth=1.5)
        ax.hist(big_list[idx], bins=20, density=True, color='tab:blue', edgecolor='white')
        ax.hist(big_list_extr[idx], bins=20, density=True, color='crimson', edgecolor='white')

        idx += 1

    # add values of skewness on the plot
    idx = 0
    fsize = 2.5
    for ax in axes.flat:
        # ax.axes.axis('tight')
        ax.tick_params(labelsize=fsize * 2.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlim(-0.4, 1.0)
        ax.set_ylim(0, 4.5)
        ax.set_ylabel('', size=1)
        ax.annotate(lbls[idx], xy=(1, 0), xycoords='axes fraction', fontsize=fsize * 3., xytext=(0.005, 0.925))
        ax.annotate("skew =  {:.2f}".format(skew(np.array(big_list[idx]), bias=True)), xy=(1, 0),
                    xycoords='axes fraction', fontsize=fsize * 3., xytext=(0.475, 0.525))
        ax.annotate("skew_EHW =  {:.2f}".format(skew(np.array(big_list_extr[idx]), bias=True)), xy=(1, 0),
                    xycoords='axes fraction', fontsize=fsize * 3., xytext=(0.475, 0.485))  # xytext=(0.525, 0.45)

        idx += 1

    # add labels and make small tweaks to make nice plot
    axes[0].set_ylabel('PDF', size=fsize * 3.)  # ,  **fig_font)
    axes[3].legend(fontsize=fsize * 2.25, loc=1, framealpha=.0)
    # axes[1].xaxis.set_label_coords(-.2, -.15)
    f.supxlabel('Normalised energy anomalies', x=.5, y=.045, size=fsize * 4.)  # , **fig_font)
    plt.subplots_adjust(wspace=0.25, hspace=0.25, left=0.05, top=0.98, bottom=0.175, right=0.95)
    sns.despine(offset=2, trim=True)

    ## specify formats to save images
    image_format = 'eps'  # e.g .png, .svg, etc.
    image_name = save_image + '.eps'
    # width = 3.487
    # height = width / 1.618
    # f.set_size_inches(width, height)
    image_format1 = 'png'  # e.g .png, .svg, etc.
    image_name1 = save_image + '.png'
    if high_res == True:
        plt.savefig(image_name, format=image_format)
        plt.savefig(image_name1, format=image_format1)
        return print("Figures are saved as: " + save_image)
    else:
        plt.show(block=True)
        print("Figures are displayed, but not saved. To save figures in .eps and .png formats, "
                     "please set savefig as True when calling pdfs_comparison function.")
    return



def box_plots_skew_clim_hws(data_lst, my_labels, my_palette, lbl_y, lbl_a, lbl_b, save_image,
                            clr_a="tab:blue", clr_b="tab:red", savefig=False):
    """
    `box_plots_skew_clim_hws(data_lst, my_labels, my_palette, lbl_y, lbl_a, lbl_b, save_image,
                            clr_a="tab:blue", clr_b="tab:red", savefig=False)`

    This function create one plot with all dataset included, with customised colors and labels.

    :param data_lst: (list) dataset
    :param my_labels: (list) labels on x-axis (should be the same length as dataset)
    :param my_palette: (dict) specified palette (should be the same length as dataset)
    :param lbl_y: (str) label for y-axis
    :param lbl_a: (str) label for legend (one part). Here, matplotlib.patches.Patch is imported
    :param lbl_b: (str) label for legend (another part). Here, matplotlib.patches.Patch is imported
    :param save_image: (str)
    :param clr_a: (str) color for the one of box plot type; set to "tab:blue" by default
    :param clr_b: (str) color for the another of box plot type; set to "tab:red" by default
    :param savefig: (bool) set to False by default
    :return: information about figure
    """
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(figsize=(20, 5))
    width = .5; x = np.arange(len(data_lst))
    sns.boxplot(data=data_lst, width=0.3, linewidth=2, palette=my_palette)
    plt.xticks(x + width, my_labels)

    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=clr_a, edgecolor='k', label=lbl_a),
                         Patch(facecolor=clr_b, edgecolor='k', label=lbl_b)]
    plt.legend(handles=legend_elements, frameon=False, ncol=2, markerfirst=False, loc=2, fontsize=16, bbox_to_anchor=[-0.015, 1.1])

    plt.ylim(-1., 2.0)
    sns.despine(offset=2)
    plt.tick_params(labelsize=14)
    plt.ylabel(lbl_y, size=16)
    plt.tight_layout()

    image_format = 'eps'  # e.g .png, .svg, etc.
    image_name = save_image + '.eps'
    image_format1 = 'png'  # e.g .png, .svg, etc.
    image_name1 = save_image + '.png'

    if savefig == True:
        plt.savefig(image_name, format=image_format)
        plt.savefig(image_name1, format=image_format1)
        return print("Figures are saved as: " + save_image)

    else:
        plt.show(block=True)
        return print("Figures are displayed, but not saved. To save figures in .eps and .png formats, "
                     "please set savefig as True when calling box_plots_skew_clim_hws function.")

