import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy import stats
import random
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn import decomposition
from sklearn import preprocessing
import math
import string
import random
import re


# Fonctions de base

def info_data(df,subset=None):
    """
    Return number of lines, columns and size of a dataframe. 
    Gives also number of duplicated data on subset (default=None).
    """
    print(f"Nombre de lignes : {df.shape[0]}")
    print(f"Nombre de colonnes : {df.shape[1]}")
    print(f"Nombre de données : {df.size}")
    print(f"Il y a {df.duplicated(subset=[subset]).sum()} données dupliquées.")


def nan_col(df):
    """
    Return the pourcentage of NaN for each column of a dataframe.
    """
    nan = df.isnull().sum() * 100 / df.shape[0]
    not_nan = 100 - nan
    df = pd.DataFrame({"% NaN": nan, "% dispo": not_nan})
    return df

def prct_cat(df, col_cat, col_100p):
    """
    Calculate percentage of data grouped by a column (col_cat) assuming that
    the column col_100p contains 100% of data in each group.
    """
    prct = df.groupby(col_cat).count() / df.shape[0] *100
    prct = prct[col_100p]
    prct.rename("% données", inplace=True)
    prct_final = prct.sort_values(ascending=False)
    return prct_final

def more_stats(df, liste_col):
    """
    Calculate mode, skewness and kurtosis for the variables 
    given in liste_col in the dataframe df.
    """
    df_sel = df[liste_col]
    mod = df_sel.mode()
    skw = df_sel.skew()
    kurt = df_sel.kurtosis()
    mod = mod.T
    stats = mod.rename(columns={0:"mode"})
    stats["skewness"] = skw
    stats["kurtosis"] = kurt
    return stats



# Fonctions de plots ACP

def display_eigenvalues(cpa):
    """
    Display a graph with % of variance explained by each axe of a CPA and cumulated variance.
    """
    scree = cpa.explained_variance_ratio_*100
    plt.rcParams.update({"figure.titlesize":16, "axes.titlesize":16, "axes.labelsize":14, "xtick.labelsize":13, "ytick.labelsize":13})
    
    fig, ax = plt.subplots(figsize=(7, 7))
    
    x = np.arange(len(scree))+1
    y1 = scree
    y2 = scree.cumsum()

    p1 = ax.bar(x, y1, label="% pour l'axe")
    p2 = ax.plot(x, y2,c="red",marker='o', label="% cumulé")
    
    ax.bar_label(p1, fmt='%.1f', size=13)          

    for i,j in zip(x, y2):
        ax.annotate(f"{j:.1f}", xy=(i,j), ha="center", size=13, xytext=(-7, 9), textcoords='offset points')
    
    ax.set_xlabel("Rang de l'axe d'inertie", fontsize=14)
    ax.set_ylabel("Pourcentage d'inertie expliqué", fontsize=14)
    ax.legend(fontsize=13)
    ax.set_title("Eboulis des valeurs propres", fontsize=16, pad=20)
    
    #fig.savefig("eigenvalues_plot.png", bbox_inches="tight", dpi=150)

def display_circles(pcs, n_comp, pca, axis_ranks, labels=None, label_rotation=0, lims=None):
    """
    Display the correlation circle of a CPA.
    """
    sns.set_theme(style="whitegrid")
    
    for d1, d2 in axis_ranks: # On affiche les 3 premiers plans factoriels, donc les 6 premières composantes
        if d2 < n_comp:

            # initialisation de la figure
            fig, ax = plt.subplots(figsize=(7,7))

            # détermination des limites du graphique
            if lims is not None :
                xmin, xmax, ymin, ymax = lims
            elif pcs.shape[1] < 30 :
                xmin, xmax, ymin, ymax = -1, 1, -1, 1
            else :
                xmin, xmax, ymin, ymax = min(pcs[d1,:]), max(pcs[d1,:]), min(pcs[d2,:]), max(pcs[d2,:])

            # affichage des flèches
            # s'il y a plus de 30 flèches, on n'affiche pas le triangle à leur extrémité
            if pcs.shape[1] < 30 :
                plt.quiver(np.zeros(pcs.shape[1]), np.zeros(pcs.shape[1]),
                    pcs[d1,:], pcs[d2,:], 
                    angles='xy', scale_units='xy', scale=1, color="grey")
            # (voir la doc : https://matplotlib.org/api/_as_gen/matplotlib.pyplot.quiver.html)
            else:
                lines = [[[0,0],[x,y]] for x,y in pcs[[d1,d2]].T]
                ax.add_collection(LineCollection(lines, axes=ax, alpha=.1, color='black'))
            
            # affichage du cercle
            circle = plt.Circle((0,0), 1, facecolor="lightyellow", edgecolor="darkorange", alpha=0.5)
            plt.gca().add_artist(circle)

            # définition des limites du graphique
            plt.xlim(xmin, xmax)
            plt.ylim(ymin, ymax)
        
            # affichage des lignes horizontales et verticales
            plt.plot([-1, 1], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-1, 1], color='grey', ls='--')
            
            # affichage des noms des variables  
            if labels is not None:  
                for i,(x, y) in enumerate(pcs[[d1,d2]].T):
                    if x < 0:
                        dg="right"
                    else:
                        dg="left"
                    if y < 0:
                        hb="top"
                    else:
                        hb="bottom"
                    if x >= xmin and x <= xmax and y >= ymin and y <= ymax :
                        plt.text(x, y, labels[i], fontsize='14', ha=dg, va=hb, rotation=label_rotation, color="indigo")

            # nom des axes, avec le pourcentage d'inertie expliqué
            plt.xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            plt.ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            plt.title("Cercle des corrélations (F{} et F{})".format(d1+1, d2+1))
            plt.show(block=False)
            
    #fig.savefig("circles_variables.png", bbox_inches="tight", dpi=150)


def display_factorial_planes(X_projected, n_comp, pca, axis_ranks, labels=None, alpha=1, illustrative_var=None):
    """
    Display the factorial planes of a CPA for the individuals.
    """
    sns.set_theme(style="whitegrid")
    
    for d1,d2 in axis_ranks:
        if d2 < n_comp:
 
            # initialisation de la figure       
            fig, ax = plt.subplots(figsize=(7,7))
        
            # affichage des points
            if illustrative_var is None:
                ax.scatter(X_projected[:, d1], X_projected[:, d2], marker="*", alpha=alpha, s=50)
            else:
                illustrative_var = np.array(illustrative_var)
                for value in np.unique(illustrative_var):
                    selected = np.where(illustrative_var == value)
                    ax.scatter(X_projected[selected, d1], X_projected[selected, d2], alpha=alpha, marker="*", 
                                s=50, label=value)
                ax.legend()
                       
            # affichage des labels et masquer ceux qui se superposent
            ann = []
            for i in range(len(labels)):
                # détermine le décalage des labels par rapport à la position du point
                if X_projected[i, d1] < 0:
                    dg=-15
                else:
                    dg=5
                if X_projected[i, d2] < 0:
                    hb=-15
                else:
                    hb=5
                # créé la liste de labels et leur caractéristiques
                ann.append(ax.annotate(labels[i], xy = (X_projected[i, d1], X_projected[i, d2]), xytext = (dg, hb), 
                                       fontsize=14, textcoords="offset points", color="chocolate"))
            
            # évite l'overlap entre les labels
            mask = np.zeros(fig.canvas.get_width_height(), bool)           
            fig.canvas.draw()
            for a in ann:
                bbox = a.get_window_extent()
                x0 = int(bbox.x0)
                x1 = int(math.ceil(bbox.x1))
                y0 = int(bbox.y0)
                y1 = int(math.ceil(bbox.y1))

                s = np.s_[x0:x1+1, y0:y1+1]
                if np.any(mask[s]):
                    a.set_visible(False)
                else:
                    mask[s] = True
            
            # détermination des limites du graphique
            boundary = np.max(np.abs(X_projected[:, [d1,d2]])) * 1.1
            ax.set_xlim([-boundary,boundary])
            ax.set_ylim([-boundary,boundary])
        
            # affichage des lignes horizontales et verticales
            plt.plot([-100, 100], [0, 0], color='grey', ls='--')
            plt.plot([0, 0], [-100, 100], color='grey', ls='--')

            # nom des axes, avec le pourcentage d'inertie expliqué
            ax.set_xlabel('F{} ({}%)'.format(d1+1, round(100*pca.explained_variance_ratio_[d1],1)))
            ax.set_ylabel('F{} ({}%)'.format(d2+1, round(100*pca.explained_variance_ratio_[d2],1)))

            ax.set_title("Projection des individus (sur F{} et F{})".format(d1+1, d2+1))

    #fig.savefig("graph_ind.png", bbox_inches="tight", dpi=150)


def quality_proj(cpa, n_axes, list_variables):
    """
    Take in input the result of the CPA, the number of CPA axes and the list of varaibles, return the quality of 
    projection for each variable on each axis (cos(angle btween variable and its projection)**2).
    """
    #Création des labels pour les axes
    labels_axes=[]
    numbers=list(range(1,n_axes+1))
    for i in numbers:
        labels_axes.append("F"+str(i))
        
    # Récupération des coordonnées des variables sur les axes, calcul du cos**2
    loadings = cpa.components_[:n_axes].T * np.sqrt(cpa.explained_variance_[:n_axes])
    loading_matrix = pd.DataFrame(loadings, columns=labels_axes, index=list_variables)
    quality_variables = loading_matrix * loading_matrix
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(6,6))
    sns.heatmap(quality_variables, annot=True, cmap="YlGn", vmin=0, vmax=1)
    ax.set_title("Indices de la qualité de la représentation des variables selon les axes de l'ACP", pad=20)
    ax.set_xlabel("Axes de l'ACP", fontsize=15)
    ax.set_ylabel("Variables", fontsize=15)
    
    #fig.savefig("quality_proj.png", bbox_inches="tight", dpi=150)