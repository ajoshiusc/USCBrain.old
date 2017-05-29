import sys
import itertools
import numpy as np
from mayavi import mlab
import scipy as sp
from scipy import stats
#import seaborn as sns
from sklearn.decomposition import PCA

def modified_find_centroid(c):
    sx = sy = sL = sz = 0
    index=-1
    min=np.Inf
    for i in range(c.shape[0]):  # counts from 0 to len(points)-1
       x0, y0, z0 = c[i]  # in Python points[-1] is last element of points
       sL=0
       for j in range(c.shape[0]):
           x1, y1, z1 = c[j]
           L = ((x1 - x0) ** 2 + (y1 - y0) ** 2 + (z1 - z0) ** 2) ** 0.5
           sL += L
       if min>sL :
           min=sL
           index=i
    return c[index]

def search(vertices,centroid):
    for i in range(vertices.shape[0]):
        if vertices[i][0] == centroid[0]:
            if vertices[i][1] == centroid[1]:
                if vertices[i][2] == centroid[2]:
                    return i
    return -1

def find_location_smallmask(vertices,centroid,mask):
    index = search(vertices, centroid)
    #print vertices[index]
    #remember to reconsider here about the range
    count=0
    for i in range(index):
        if mask[i]==True:
            count+=1;
    return count

def merge(s1,s2):
    s=[]
    s=sp.array(s1)
    s=sp.vstack([s,s2])
    return s

def choose_best(subject,reference_subject,nCluster):
    min=np.Inf
    save=np.array([])
    #change
    per=np.arange(nCluster)
    for j in list(itertools.permutations(per, nCluster)):
        sum=0
        #change
        for k in range(0, nCluster):
            sum += np.sum(np.abs(subject[k]-reference_subject[j[k]])**2)
            #sum += np.sum(subject[k] - reference_subject[j[k]])
            #print  sum, j
        if min > sum:
            min = sum
            save = np.array(j)
    #print save
    return save

def replot(r_labels,r_vertices,r_faces,label_matrix,reference_label,nCluster):
    for i in range(r_labels.shape[0]):
        for j in range(nCluster):
            if r_labels[i] == (j+1):
                r_labels[i]=label_matrix[j]+1
    '''mlab.triangular_mesh(r_vertices[:, 0], r_vertices[:, 1], r_vertices[:, 2], r_faces,representation='surface',opacity=1, scalars=np.float64(r_labels))
    mlab.gcf().scene.parallel_projection = True
    mlab.view(azimuth=0, elevation=90)
    mlab.colorbar(orientation='horizontal')
    mlab.close()'''
    return r_labels

def avgplot(r_labels,nSubjects,r_vertices,r_faces,nCluster,hemi):
    labels = np.zeros(r_labels.shape[0],dtype=float)
    for i in range(r_labels.shape[0]):
        labels[i] = np.sum(r_labels[i])/nSubjects
    mlab.figure(size=(1024, 768), \
                bgcolor=(1, 1, 1),fgcolor=(0.5,0.5,0.5))
    mlab.triangular_mesh(r_vertices[:, 0], r_vertices[:, 1], r_vertices[:, 2], r_faces, representation='surface',
                         opacity=1, scalars=np.float64(labels))
    mlab.gcf().scene.parallel_projection = True
    mlab.view(azimuth=0, elevation=270)
    mlab.colorbar(orientation='vertical')
    #mlab.show()
    #mlab.close()
    mlab.options.offscreen = True
    mlab.savefig('precentral_mean_r'+hemi + '.png')
    mlab.close()
    labels = np.zeros(r_labels.shape[0], dtype=float)
    freq = np.zeros(r_labels.shape[0], dtype=float)
    for i in range(r_labels.shape[0]):
        mode,count=stats.mode(r_labels[i])
        labels[i] = mode[0]
        freq[i]=count
    mlab.figure(size=(1024, 768), \
                bgcolor=(1, 1, 1),fgcolor=(0.5,0.5,0.5))
    mlab.triangular_mesh(r_vertices[:, 0], r_vertices[:, 1], r_vertices[:, 2], r_faces, representation='surface',
                             opacity=1, scalars=np.float64(labels))
    mlab.gcf().scene.parallel_projection = True
    mlab.view(azimuth=0, elevation=90)
    mlab.colorbar(orientation='vertical')
    #mlab.show()
    #mlab.close()
    mlab.options.offscreen = True
    mlab.savefig('precentral-mode' + hemi+ '.png')
    mlab.close()
    return labels,freq


def rand_indices_within_subjects(nSession,list_all,nSubjects,mask):
    from sklearn.metrics import adjusted_rand_score
    sum=0
    temp=[]
    for i in range(nSubjects):
        for j in range(0,nSession):
            for k in range(j+1,nSession):
                temp.append(adjusted_rand_score( list_all[j][i][mask],list_all[k][i][mask] ))
                sum += adjusted_rand_score( list_all[j][i][mask],list_all[k][i][mask] )
    temp=np.array(temp)
    return sum/(40.0*6)

def display_intrasubjects(list_all,nSubjects,session_number,nClusters):
    import matplotlib.pyplot as plt
    for i in range(nSubjects):
        count=np.arange(10832)
        plt.axis([7200, 10833, 1, 3])
        plt.plot(count, list_all[session_number][i], 'k')
        plt.show()


def rand_indices_across_subjects(nSession,list_all,nSubjects,mask):
    from sklearn.metrics import adjusted_rand_score
    sum=0
    temp=[]
    for i in range(nSubjects):
        for j in range(i+1,nSubjects):
            for k in range(0,nSession):
                temp.append(adjusted_rand_score( list_all[k][i][mask],list_all[k][j][mask]))
                sum += adjusted_rand_score( list_all[k][i][mask],list_all[k][j][mask])
    temp=np.array(temp)
    return sum/(20.0*39*4)

'''def intersubjects(labels,nSubjects):
    session_num=4
    count=np.array([])
    list_intra=[]
    for i in range(nSubjects):
        list = []
        for j in range(session_num):
            list.append(labels[j][i])
            list_intra.append(labels[j][i])
        mode,count1=stats.mode(list)
        if i == 0:
            count = sp.array(np.extract(mode > 0, count1))
        else:
            count = sp.vstack([count, np.extract(mode > 0, count1)])
    ax = sns.kdeplot(count.flatten(), shade=True, color="r")
    sns.plt.show()
    mode, count1 = stats.mode(list_intra)
    count = sp.array(np.extract(mode > 0,count1))
    ax = sns.kdeplot((count.flatten())/40.0, shade=True, color="g")
    sns.plt.show()
    print

def intrasubjects(labels,nSubjects):
    session_num = 4
    count = np.array([])
    for i in range(session_num):
        list = []
        for j in range(nSubjects):
            list.append(labels[i][j])
        mode, count1 = stats.mode(list)
        count = sp.array(np.extract(mode > 0, count1))
        ax = sns.kdeplot((count.flatten())/10.0, shade=True, color="r")
      sns.plt.show()'''

def spatial_map(vector,r_vertices,r_faces,msk_small_region,labs,val):
    r_labels = np.zeros([r_vertices.shape[0]])
    r_labels[~msk_small_region] = vector
    r_labels[msk_small_region]=labs
    mlab.figure(size=(1024, 768), \
                bgcolor=(1, 1, 1),fgcolor=(0.5,0.5,0.5))
    mlab.triangular_mesh(r_vertices[:, 0], r_vertices[:, 1], r_vertices[:,
                                                             2], r_faces, representation='surface',
                         opacity=1, scalars=np.float64(r_labels))
    mlab.gcf().scene.parallel_projection = True
    mlab.view(azimuth=0, elevation=270)
    mlab.draw()
    mlab.colorbar(orientation='vertical')
    #mlab.show()
    mlab.options.offscreen = True
    mlab.savefig('precentral_back'+str(val)+'.png')
    mlab.close()
    return r_labels



def change_labels(r_labels,order,nCluster):
    #print labels
    for i in range(r_labels.shape[0]):
        for j in range(nCluster):
            if r_labels[i] == (j + 1):
                r_labels[i] = order[j] + 1
                break
    return r_labels


def change_order(order,nCluster):
    save=np.array([0 for x in range(nCluster)])
    for i in range(0,nCluster):
        save[order[i]]=i
    return save

def change_corr_vector(subject,label_matrix):
    return subject[label_matrix[0]],subject[label_matrix[1]],subject[label_matrix[2]]


def initialize():
    R_all = np.load('all_data_file.npz')['R_all']
    mask = np.load('all_data_file.npz')['mask']
    vertices = np.load('all_data_file.npz')['vertices']
    faces = np.load('all_data_file.npz')['faces']
    d = R_all[mask, :]
    rho = np.corrcoef(d)
    rho[~np.isfinite(rho)] = 0
    #rho = np.abs(rho)
    d_corr = R_all[~mask, :]
    rho_1 = np.corrcoef(d, d_corr)
    rho_1 = rho_1[range(d.shape[0]), d.shape[0]:]
    rho_1[~np.isfinite(rho_1)] = 0
    return R_all,vertices,faces,mask,rho,rho_1


def num_of_cluster():
    R_all = np.load('all_data_file.npz')['R_all']
    mask = np.load('all_data_file.npz')['mask']
    d = R_all[mask, :]
    rho = np.corrcoef(d)
    rho[~np.isfinite(rho)] = 0
    rho = np.abs(rho)
    pca = PCA()
    pca.fit_transform(rho)
    store1 = pca.explained_variance_ratio_.cumsum()
    nCluster = plot_graph(store1)
    return nCluster


def all_separate(labels,vertices,nCluster):
    c=[]
    for i in range(nCluster):
        c.append([])
    all_centroid=[]
    for i in range(labels.shape[0]):
        for j in range(nCluster):
            if labels[i] == (j+1):
                c[j].append(vertices[i])
    for i in range(nCluster):
        c[i]=np.array(c[i])
        if i == 0:
            all_centroid = sp.array(modified_find_centroid(c[i]))
        else:
            all_centroid = sp.vstack([all_centroid, modified_find_centroid(c[i])])
    return (all_centroid)



def plot_graph(store1,roiregion):
    import numpy as np
    import matplotlib.pyplot as plt
    t1 = np.arange(7)
    import matplotlib as mpl
    mpl.use('agg')
    fig = plt.figure(1)

    # Create an axes instance
    ax1 = fig.add_subplot(111)
    plt.subplots_adjust(left=0.12, right=0.90, top=0.83, bottom=0.15)
    #fig.set_size_inches(18, 7)
    ax1.set_xlim([0, 8])
    ax1.set_ylim(0,1)
    ax1.set_title(roiregion)
    ax1.set_xlabel("Number of Cluster")
    #ax1.set_ylabel("Average Silhouette Score")
    ax1.set_ylabel("Explained variance ratio")
    ax1.set_yticks([0,0.2,0.4,0.6,0.8,1.0])  # Clear the yaxis labels / ticks
    ax1.set_xticks([1,2,3,4,5,6,7])
    for item in ([ax1.title, ax1.xaxis.label,ax1.yaxis.label]+ ax1.get_yticklabels()+ax1.get_xticklabels() ):
        item.set_fontsize(20)

    #plt.suptitle(("Average Silhouette Score"),fontsize=53, fontweight='bold')
    plt.suptitle(("PCA EXPLAINED VARIANCE RATIO"), fontsize=30)

    ax1.plot(t1+1,store1[:7],'k')
    ax1.plot(t1 + 1, store1[:7], 'ro')
    #plt.show()
    fig.savefig('PCA' + '.png', bbox_inches='tight')
    diff=np.diff(store1)
    condlist = store1 < .95
    return (np.extract(condlist, store1).size + 1)

def plot_graph_1(store1,roiregion):
    import numpy as np
    import matplotlib.pyplot as plt
    t1 = np.arange(8)
    import matplotlib as mpl
    mpl.use('agg')
    fig = plt.figure(1)

    # Create an axes instance
    ax1 = fig.add_subplot(111)
    #fig.set_size_inches(18, 7)
    plt.subplots_adjust(left=0.12, right=0.90, top=0.83, bottom=0.15)
    ax1.set_xlim([0, 11])
    ax1.set_ylim(0,1)
    ax1.set_title(roiregion)
    ax1.set_xlabel("Number of Cluster")
    ax1.set_ylabel("Average Silhouette Score")
    #ax1.set_ylabel("Explained variance ratio")
    ax1.set_yticks([0,0.2,0.4,0.6,0.8,1.0])  # Clear the yaxis labels / ticks
    ax1.set_xticks([1,2,3,4,5,6,7])
    for item in ([ax1.title, ax1.xaxis.label,ax1.yaxis.label]+ ax1.get_yticklabels()+ax1.get_xticklabels() ):
        item.set_fontsize(20)

    plt.suptitle(("Average Silhouette Score"),fontsize=30)
    #plt.suptitle(("PCA EXPLAINED VARIANCE RATIO"), fontsize=53, fontweight='bold')

    ax1.plot(t1+2,store1[:8],'k')
    ax1.plot(t1 + 2, store1[:8], 'ro')
    #plt.show()
    fig.savefig('silhoutte' + '.png', bbox_inches='tight')
    diff=np.diff(store1)
    condlist = store1 < .95
    return (np.extract(condlist, store1).size + 1)


def neighbour_correlation(rho,faces,r_vertices,msk):
    import networkx as nx
    g = nx.Graph()
    g.add_edges_from(faces[:, (0, 1)])
    g.add_edges_from(faces[:, (1, 2)])
    g.add_edges_from(faces[:, (2, 0)])
    g.add_edges_from(faces[:, (1, 0)])
    g.add_edges_from(faces[:, (2, 1)])
    g.add_edges_from(faces[:, (0, 2)])
    Adj = nx.adjacency_matrix(g)
    AdjS = Adj.todense()
    np.fill_diagonal(AdjS, 1)
    # AdjS.shape
    #AdjS = 1.0 * ((AdjS * AdjS * AdjS) > 0)
    AdjS = np.matrix(AdjS) * np.matrix(AdjS)
    AdjS=AdjS>0
    AdjS=1.0*AdjS

    rho_Thresh = np.multiply(AdjS, rho)
    rho_Thresh = np.mean(rho_Thresh, 1)
    labels = np.zeros([r_vertices.shape[0]])
    labels[msk]=rho_Thresh


    mlab.triangular_mesh(r_vertices[:, 0], r_vertices[:, 1], r_vertices[:, 2], faces, representation='surface',
                         opacity=1, scalars=np.float64(labels))


    mlab.gcf().scene.parallel_projection = True
    mlab.view(azimuth=0, elevation=90)
    mlab.colorbar(orientation='horizontal')
    mlab.close()


def affinity_mat(rho):
    return (np.exp((-2.0*(1-rho))/(.72 ** 2)))

def mapping(refined_roilists,roilist_count,current_label_id,current_color):
    keys = refined_roilists.viewkeys()
    if current_label_id in keys :
        return roilist_count
    refined_roilists[current_label_id]=current_color
    roilist_count = roilist_count + 1
    return roilist_count