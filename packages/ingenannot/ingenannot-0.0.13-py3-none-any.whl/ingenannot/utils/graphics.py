#!/usr/bin/env python3
'''
Graphics

shared graphics methods
'''
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from upsetplot import plot as upplot
import matplotlib

matplotlib.use('agg')

#from matplotlib import gridspec


class Graphics():
    '''
    Graphics
    '''

    lColors = ['palevioletred','darkorchid','royalblue',
            'darkturquoise','mediumspringgreen','olivedrab',
            'gold','sandybrown','red','silver','m','blue',
            'lightseagreen','chartreuse','darkkhaki','bisque',
            'sienna','firebrick','gray','plum','darkcyan',
            'darkgreen','orange','lightcoral','yellow']



    @staticmethod
    def get_values_for_aed_scatter_hist(transcripts, use_ev_lg):
        """format values for AED scatter hist"""

        l_aed_tr = []
        l_aed_tr_no_penalty = []
        l_aed_pr = []
        l_aed_pr_no_penalty = []

        for tr in transcripts:
            l_aed_pr.append(tr.best_bx_evidence[1])
            if use_ev_lg:
                l_aed_tr.append(min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]))
            else:
                l_aed_tr.append(tr.best_tr_evidence[1])

            if not tr.is_penalized(): 
                l_aed_pr_no_penalty.append(tr.best_bx_evidence[1])
                if use_ev_lg:
                    l_aed_tr_no_penalty.append(min(tr.best_tr_evidence[1],tr.best_lg_evidence[1]))
                else:
                    l_aed_tr_no_penalty.append(tr.best_tr_evidence[1])

        return l_aed_tr, l_aed_tr_no_penalty, l_aed_pr, l_aed_pr_no_penalty


    @staticmethod
    def plot_cumulative_aed(sources, genes, evidence="tr",out="plotCumulativeAED.png", ncol=4):

        colors=["green","red","blue","black","orange","salmon","purple","grey","pink","yellow","brown","beige"]

        plt.style.use('bmh')

        fig = plt.Figure(figsize=(20,20))
        gs = fig.add_gridspec(3,1, height_ratios=(7,7,1),left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.05, hspace=0.1)

        ax_histraw = fig.add_subplot(gs[0, 0])
        ax_histdensity = fig.add_subplot(gs[1, 0], sharex=ax_histraw)
        ax_legend = fig.add_subplot(gs[2, 0])
        ax_histraw.set_title("Cumulative distribution of AED with transcript evidence, with nb of transcripts [a] or density of transcripts [b]",fontsize=20)
        if evidence == "pr":
            ax_histraw.set_title("Cumulative distribution of AED with protein evidence, with nb of transcripts [a] or density of transcripts [b]",fontsize=20)
        if evidence == "best":
            ax_histraw.set_title("Cumulative distribution of AED with best evidence (transcript or protein), with nb of transcripts [a] or density of transcripts [b]",fontsize=20)

        ax_histraw.set_xlim(0.0,1.0)
        ax_histdensity.set_xlabel("AED", fontsize=20)
        ax_histraw.set_ylabel("Nb of transcripts", fontsize=20)
        ax_histdensity.set_ylabel("Normalized Nb of transcripts", fontsize=20)
        ax_histraw.tick_params(labelsize=15)
        ax_histdensity.tick_params(labelsize=15)
        ax_histraw.text(0.05,0.95,"a",transform=ax_histraw.get_xaxis_transform(),size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax_histdensity.text(0.05,0.95,"b",transform=ax_histdensity.get_xaxis_transform(),size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))

        for i,src in enumerate(sources):
            laed = []
            for g in [x for x in genes if x.source == src]:
                for tr in g.lTranscripts:
                    if evidence == "tr":
                        laed.append(tr.best_tr_evidence[1])
                    if evidence == "pr":
                        laed.append(tr.best_bx_evidence[1])
                    if evidence == "best":
                        laed.append(min(tr.best_tr_evidence[1],tr.best_bx_evidence[1]))
            bins = np.arange(0.0,1.001,0.001)
            ax_histraw.hist(laed, bins=bins, cumulative=True, histtype="step", color = colors[i], label=src, linewidth=1.5)
            u = ax_histdensity.hist(laed, bins=bins, cumulative=True, histtype="step", density=True, color = colors[i], label=src, linewidth=1.5)
            logging.info("{} with {} evidence, value at 0.5 AED: {}".format(src, evidence, u[0][500]))

        h,l=ax_histraw.get_legend_handles_labels() # get labels and handles from histx  
        ax_legend.legend(h,l, fontsize=20, ncol=ncol, mode="expand", loc="lower center")
        ax_legend.grid(False)
        ax_legend.set_facecolor('w')
        ax_legend.axis('off')
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)


    @staticmethod
    def plot_distribution(lxs, lys, out="", title="", xax="", yax="",
            color="blue", legend="", grid=None):
        """Draw a simple Distribution"""

        fig = plt.Figure(figsize=(20,20))
        fig.suptitle(title, fontsize=32)
        axis = fig.add_subplot(111)
        axis.plot(lxs,lys, color=color)
        if legend:
            axis.legend(legend, fontsize=22)
        for line in grid:
            axis.axvline(x=line, linestyle='dashed', linewidth=1, color='black')
        axis_font = {'size':'28'}
        axis.set_xlabel(xax, **axis_font)
        axis.set_ylabel(yax, **axis_font)
        axis.tick_params(labelsize=20)
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)


    @staticmethod
    def plot_upsetplot(counts,out="",title=""):
        ''' plot UpSet plot'''

        upplot(counts, show_counts=True, subset_size="count")
        plt.title(title, fontsize=10)
        plt.savefig(out)


    @staticmethod
    def plot_aed_scatter_hist(laed, aedtr_filtering, aedpr_filtering, out="", legend="", title=""):
        """scatter plot of AEDs with histograms"""

        plt.style.use('bmh')
        #plt.style.use('seaborn')
        #plt.style.use('ggplot')

        fig = plt.Figure(figsize=(20,20))
        # add gridspec
        gs = fig.add_gridspec(2,2,width_ratios=(7, 2), height_ratios=(2, 7),
                                      left=0.1, right=0.9, bottom=0.1, top=0.9,
                                                            wspace=0.05, hspace=0.05)
        ax = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
        ax_legend = fig.add_subplot(gs[0, 1])

        ax.scatter(laed[0],laed[1], color="#20C2EF")
        # By using ``transform=vax.get_xaxis_transform()`` the y coordinates are scaled
        # such that 0 maps to the bottom of the axes and 1 to the top.
        ax.vlines(aedtr_filtering, 0, 1, transform=ax.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax.text(aedtr_filtering,0.9,aedtr_filtering,size=20,ha="center", va="center", color='r',bbox=dict(boxstyle="round",fc='#EEEEEE'))
        ax.hlines(aedpr_filtering, 0, 1, transform=ax.get_yaxis_transform(), colors='r', linestyle="dashed")
        ax.text(0.9,aedpr_filtering,aedpr_filtering,size=20,ha="center", va="center", color='r', bbox=dict(boxstyle="round",fc='#EEEEEE'))

        lb,rb,lt,rt = 0,0,0,0
        lb_no_penalty,rb_no_penalty,lt_no_penalty,rt_no_penalty = 0,0,0,0

        for i,val in enumerate(laed[0]):
            if laed[0][i] <= aedtr_filtering and laed[1][i] <= aedpr_filtering:
                lb += 1
            if laed[0][i] > aedtr_filtering and laed[1][i] <= aedpr_filtering:
                rb += 1
            if laed[0][i] <= aedtr_filtering and laed[1][i] > aedpr_filtering:
                lt += 1
            if laed[0][i] > aedtr_filtering and laed[1][i] > aedpr_filtering:
                rt += 1
        ax.text(aedtr_filtering/2,aedpr_filtering/2,lb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-aedtr_filtering)/2),aedpr_filtering/2,rb,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(aedtr_filtering/2,1-((1-aedpr_filtering)/2),lt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))
        ax.text(1-((1-aedtr_filtering)/2),1-((1-aedpr_filtering)/2),rt,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(1., 1., 1.)))

        for i,val in enumerate(laed[2]):
            if laed[2][i] <= aedtr_filtering and laed[3][i] <= aedpr_filtering:
                lb_no_penalty += 1
            if laed[2][i] > aedtr_filtering and laed[3][i] <= aedpr_filtering:
                rb_no_penalty += 1
            if laed[2][i] <= aedtr_filtering and laed[3][i] > aedpr_filtering:
                lt_no_penalty += 1
            if laed[2][i] > aedtr_filtering and laed[3][i] > aedpr_filtering:
                rt_no_penalty += 1

            ax.text(aedtr_filtering/2,aedpr_filtering/2-0.05,lb_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(1-((1-aedtr_filtering)/2),aedpr_filtering/2-0.05,rb_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(aedtr_filtering/2,1-((1-aedpr_filtering)/2)-0.05,lt_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0,0,0), fc=(.5, 1., 1.)))
            ax.text(1-((1-aedtr_filtering)/2),1-((1-aedpr_filtering)/2)-0.05,rt_no_penalty,size=20,ha="center", va="center", bbox=dict(boxstyle="round",ec=(0.0,0,0), fc=(.5, 1., 1.)))

        ax.set_xlabel("AED with transcript evidence", fontsize=20)
        ax.set_ylabel("AED with protein evidence", fontsize=20)
        ax.tick_params(labelsize=15)

        bins = np.arange(0.0,1.01,0.01)
        ax_histx.hist(laed[0], bins=bins, color = '#36953a', edgecolor = 'black', label="AED transcripts")
        ax_histx.vlines(aedtr_filtering, 0, 1, transform=ax_histx.get_xaxis_transform(), colors='r', linestyle="dashed")
        ax_histx.tick_params(labelsize=12)
        ax_histx.set_ylabel("Nb. Transcripts (transcript evidence)", fontsize=20)
        ax_histy.hist(laed[1], bins=bins, color = '#fc4b67', edgecolor = 'black', orientation='horizontal', label="AED proteins")
        ax_histy.hlines(aedpr_filtering, 0, 1, transform=ax_histy.get_yaxis_transform(), colors='r', linestyle="dashed")
        ax_histy.tick_params(labelsize=12)
        ax_histy.set_xlabel("Nb. Transcripts (protein evidence)", fontsize=20)

        h,l=ax_histx.get_legend_handles_labels() # get labels and handles from histx  
        hy,ly=ax_histy.get_legend_handles_labels() # get labels and handles from histy
        h.extend(hy)
        l.extend(ly)
        ax_legend.legend(h,l, fontsize=20)
        # Hide grid lines
        ax_legend.grid(False)
        # Hide axes ticks
        #ax_legend.set_xticks([])
        #ax_legend.set_yticks([])
        # change background color
        ax_legend.set_facecolor('w')
        ax_legend.axis('off')

        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)


    @staticmethod
    def plot_curation_scatter_hist(laed, out="", legend="", title=""):
        """scatter plot of AEDs with histograms"""

        plt.style.use('bmh')

        fig = plt.Figure(figsize=(20,20))
        # add gridspec
        gs = fig.add_gridspec(3,2,width_ratios=(7, 2), height_ratios=(2, 7,2),
                                      left=0.06, right=0.96, bottom=0.0, top=0.96,
                                                            wspace=0.1, hspace=0.1)
        ax = fig.add_subplot(gs[1, 0])
        ax_histx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_histy = fig.add_subplot(gs[1, 1], sharey=ax)
        ax_legend = fig.add_subplot(gs[2, 0])

        colors=['blue','red','green','maroon','black','orange','purple']
        for idx,area in enumerate(laed):
            ax.scatter(area[0],area[1], color=colors[idx], alpha=0.5)
        # By using ``transform=vax.get_xaxis_transform()`` the y coordinates are scaled
        ax.set_xlabel("AED with transcript evidence", fontsize=14)
        ax.set_ylabel("AED with protein evidence", fontsize=14)
        ax.tick_params(labelsize=15)

        bins = np.arange(0.0,1.01,0.01)
        colors=['blue','red','green','maroon','black','orange','purple']
        ax_histx.hist([i[0] for i in laed], bins=bins, color = colors, edgecolor = 'black', label=legend, stacked=True)
        ax_histx.tick_params(labelsize=12)
        ax_histx.set_ylabel("Nb. Transcripts (transcript evidence)", fontsize=14)
        ax_histx.set_title(title,fontsize=22)
        ax_histy.hist([i[1] for i in laed], bins=bins, color = colors, edgecolor = 'black',orientation='horizontal', label="AED proteins", stacked=True)
        ax_histy.tick_params(labelsize=12)
        ax_histy.set_xlabel("Nb. Transcripts (protein evidence)", fontsize=14)
        h,l=ax_histx.get_legend_handles_labels() # get labels and handles from histx  
        ax_legend.legend(h,l,fontsize=15, loc='center left')
        # Hide grid lines
        ax_legend.grid(False)
        # change background color
        ax_legend.set_facecolor('w')
        ax_legend.axis('off')
        canvas = FigureCanvasAgg(fig)
        canvas.print_figure(out, dpi=80)
