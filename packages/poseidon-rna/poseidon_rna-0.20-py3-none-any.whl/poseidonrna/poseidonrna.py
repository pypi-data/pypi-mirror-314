'''
2024-12-01 AS v0.19
Import json package to write json
Fix issue with folder/out adding '/' only sometimes

2024-11-26 AS v0.18
Added WL1 vector analysis functions
vectorize() = read in kernel vectors
entropyTrim() = remove dimnesions that provide less the ethresh information
focusDim() = remove dimensions to desired number by cutting lowest entropy dimensions first
normalizeArray() = nomalized array setting max value to 1
'''
import os
import sys
import json
import glob
import time
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx
from scipy import stats
import matplotlib.pyplot as plt
from progress.bar import ChargingBar
from scipy.cluster.hierarchy import dendrogram, linkage


################################################################################
'''
Graph and Graph3D auxillary/support functions
'''
def read_db_structures(filename):
    #only reads first structure
    # Open the .db file
    with open(filename, 'r') as file:
        # Read the lines
        lines = file.readlines()

    names = []
    seqs = []
    pairs = []
    for line in lines:
        if line[0] == '>':
            names.append(line[1:])
        elif line[0] in ['A','C','G','U','a','c','g','u']:
            seq = list(line)[:-1]
        elif line[0] in ['.','(',')']:
            seqs.append(seq)
            pairs.append(list(line)[:-1])

    return names,seqs,pairs

def read_ct_structures(file,prefix):

    # Open the .ctfile
    with open(file, 'r') as file:
        # Read the lines
        lines = file.readlines()

    #Make list of structures with each structure being a list of lines split into the CT columns.
    S= []
    Stemp = ['Null']
    names = []
    for line in lines:

        #separate structures based on some notable "prefix" that appears in each structre title ('#' in Seismic)
        if prefix in line:

            S.append(Stemp)
            Stemp = []
            names.append(line.split()[1])

        else:
            Stemp.append(line.split())

    S.append(Stemp)
    file.close()

    S = S[1:]

    return(names,S)

def create_db_graph(seq,pair,colors):
    #generate empty graph
    G = nx.Graph()

    #create node at infinity
    G.add_node(0,base='N',label='O',color = colors[0])

    #add nodes for each base
    for x in range(len(seq)):

        G.add_node(x+1,base=seq[x],color = colors[x+1])

    #create "pending" list to pair appropriately.
    pending=[]

    for x in range(len(pair)):
        G.add_edge(x,x+1,color='#642FDB') #from 0 at infinity to 1, then 1 to 2 etc. up to last base

        #Adds a connection point is open brackett
        if pair[x] == '(':
            pending.append(x+1)

        #Connects node to last open brackett from the pending list. 
        elif pair[x] == ')':
            G.add_edge(pending[-1],x+1,color = '#E9913F')
            pending = pending[:-1]

        #ignores if not a brackett i.e. a dot
        else:
            pass

    #G.add_edge(x+1,0)
        
    return G

def conGraphStep(G,line, ROCAUC, color):

    G.add_node(int(line[0]), base = line[1], label = ROCAUC, color = color)

    G.add_edge(int(line[0]),int(line[2]),color = '#642FDB')

    if int(line[0]) < int(line[4]):

        G.add_edge(int(line[0]),int(line[4]), color = '#E9913F')

    return

def create_ct_graph(struc,AUC,colors):
    #generate empty graph
    G = nx.Graph()

    #create node at infinity
    G.add_node(0,base='N',label = 'O',color = colors[0])


    if isinstance(AUC, np.ndarray):# == False:
        for x in range(len(struc)):

            #Adds new node for each base and relevant connected edges
            conGraphStep(G,struc[x],AUC[x],colors[x+1])


    else:
        for x in range(len(struc)):

            #Adds new node for each base and relevant connected edges
            conGraphStep(G,struc[x],'',colors[x+1])

        
    return G

def plotGraph(G,name,color,node_size,bases,view,edge_color,**kwargs):

    args = dict(kwargs.items())

    plt.rcParams["figure.figsize"] = (15,15)

    try:
        pos = args['pos']
        
    except:
        pos = nx.kamada_kawai_layout(G)

    if edge_color == True:
        edge_colors = [G.edges[n]['color'] for n in G.edges]
    else:
        edge_colors = ['black' for n in G.edges]

    if color == None:
        
        nx.draw(G,pos,with_labels=False,node_size = node_size, edge_color = edge_colors)

    else:
        node_colors = [G.nodes[n]['color'] for n in G.nodes]
        nx.draw(G,pos,with_labels=False,node_size = node_size,node_color=node_colors,cmap=sns.color_palette("viridis", as_cmap=True), edge_color = edge_colors)

    if bases == True:
        #Label nodes with base
        labels = nx.get_node_attributes(G, 'base')
        nx.draw_networkx_labels(G, pos, labels)

    plt.savefig('Structures/'+name+'.svg')
    plt.savefig('Structures/'+name+'.png')

    if view == True:
        plt.show()

    plt.close()

    return(pos)

def plotGraph3D(G,name,view,**kwargs):

    args = dict(kwargs.items())

    try:
        pos = args['pos']
        
    except:
        pos = nx.kamada_kawai_layout(G,dim = 3)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for node, coords in pos.items():
        ax.scatter(coords[0], coords[1], coords[2], label=node,color = 'black')

    for edge in G.edges():
        node1 = edge[0]
        node2 = edge[1]
        x = [pos[node1][0], pos[node2][0]]
        y = [pos[node1][1], pos[node2][1]]
        z = [pos[node1][2], pos[node2][2]]
        ax.plot(x, y, z, color='gray')

    #for node, coords in pos.items():
        #ax.text(coords[0], coords[1], coords[2], node, color='red')

    plt.savefig('Structures/3D_'+name+'.svg')
    plt.savefig('Structures/3D_'+name+'.png')

    if view == True:
        plt.show()

    plt.close()

    return(pos)

    


################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
'''
Cloning Calc
'''
def Cloning():
    vol=float(input("Volume to fill: "))

    x=0

    while x==0:
        ins=input("Number of inserts: ")

        try:
            ins=int(ins)
            x=1

        except:
            pass


    C=[]
    M=[]
    C.append(float(input("Concentration of Vector: ")))
    M.append(float(input("Bp of Vector: ")))

    for x in range(0,ins):
        st1="Concentration of Insert "+str(x+1)+": "
        st2="Bp of Insert "+str(x+1)+": "

        C.append(float(input(st1)))
        M.append(float(input(st2)))


    V=[1]

    for x in range(1,ins+1):

        V.append(3*C[0]*M[x]/M[0]/C[x])

    tot=0
    for x in V:
        tot+=x

    rat=vol/tot

    print("\n\n\n\n\n")

    print("Vector: ",rat*V[0])
    for x in range(1,ins+1):
        print("Insert ",x,": ",rat*V[x])


    return()

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
'''
ddPCR Plotting
'''
def PlotAmp(files,output):

    bar = ChargingBar('Processing', max=len(files)+3, suffix = '%(percent).1f%% - %(eta)ds')

    df = pd.DataFrame(columns = ['Ch1 Amplitude','Ch2 Amplitude','Cluster','Well'])
    for file in files:

        bar.next()

        well = file.split('_')[-2]

        dfTemp = pd.read_csv(file)

        dfTemp['Well'] = well       

        df = pd.concat([df,dfTemp],ignore_index = True)

        sns.scatterplot(data = dfTemp, x = 'Ch1 Amplitude', y = 'Ch2 Amplitude', hue =  'Cluster',edgecolor = None,palette = 'viridis')
        plt.xlim(0,12000)
        plt.ylim(0,10000)
        plt.savefig(output+'/Amplitude/'+well+'_2D_Amp.png')
        plt.savefig(output+'/Amplitude/'+well+'_2D_Amp.svg')
        plt.close()

    bar.next()

    category_positions = {category: i for i, category in enumerate(df['Well'].unique())}

    ax = sns.stripplot(data = df, x = 'Well', y = 'Ch1 Amplitude',hue = 'Cluster',jitter = 0.5,legend = False,palette = 'viridis')
    for category, position in category_positions.items():
        ax.axvline(x=position+0.5, color='red', linestyle='--')
    plt.savefig(output+'/Amplitude/1D_Ch1_Amp.png')
    plt.savefig(output+'/Amplitude/1D_Ch1_Amp.svg')
    plt.close()

    bar.next()

    ax = sns.stripplot(data = df, x = 'Well', y = 'Ch2 Amplitude',hue = 'Cluster',jitter = 0.5,legend = False,palette = 'viridis')
    for category, position in category_positions.items():
        ax.axvline(x=position+0.5, color='red', linestyle='--')
    plt.savefig(output+'/Amplitude/1D_Ch2_Amp.png')
    plt.savefig(output+'/Amplitude/1D_Ch2_Amp.svg')
    plt.close()

    bar.next()
    bar.finish()

    
    
    return


def ddPCR_amp(folder, output):

    output = output+'/Figures'

    if not os.path.exists(output):
        os.makedirs(output)
        os.makedirs(output+'/Amplitude')
        os.makedirs(output+'/Ratios')
        
    files = glob.glob(folder+'/*Amplitude.csv')

    PlotAmp(files,output)
    

    return


###############################################################################


def convert(df):

    columns = list(df.columns)[2:]

    df = df.set_index('Cycle')

    df_long = df.reset_index().melt(id_vars='Cycle', var_name='Well', value_name='Value')

    return(df_long)

#plot the quantification curves for FAM and HEX
def plotFamHex(inputfolder,meta,hueval,styleval,sizeval,filtered,fval):

    metaFile = glob.glob(inputfolder+"/*meta.xlsx")[0]

    dfMeta = readMeta(metaFile)

    filesFAM = glob.glob(inputfolder+"/*Quantification Amplification Results_FAM.csv")
    filesHEX = glob.glob(inputfolder+"/*Quantification Amplification Results_HEX.csv")

    dfFAM = pd.read_csv(filesFAM[0])
    dfHEX = pd.read_csv(filesHEX[0])


    dfFAM = convert(dfFAM)
    dfHEX = convert(dfHEX)
    dfFAM['Fluor']='FAM'
    dfHEX['Fluor']='HEX'

    df = pd.merge(dfMeta, dfFAM, on='Well')
    dfTemp = pd.merge(dfMeta, dfHEX, on='Well')

    df = pd.concat([df,dfTemp])

    cols = list(df.columns)[1:]
    cols.remove('Value')

    df = df.groupby(cols).mean('Value').reset_index()

    sns.lineplot(data = df, x = 'Cycle', y = 'Value',hue = hueval,style = styleval,size = 'RT')
    plt.savefig(inputfolder+'/RTcurves.png')
    plt.savefig(inputfolder+'/RTcurves.svg')
    plt.close()

    df = df[df[filtered]==fval]
    sns.lineplot(data = df, x = 'Cycle', y = 'Value',hue = 'Sample',style = 'Fluor',palette = 'viridis')
    plt.savefig(inputfolder+'/PrimaryCurves.png')
    plt.savefig(inputfolder+'/PrimaryCurves.svg')
    plt.close()
    
    return(dfMeta)

def normalize_to_reference(row, df,col,val,matches):
    # Find the reference row where Sample == 0.1 and RT/Fluor match
    condition = (df[col] == val)
    for column in matches:
        if column == col:
            pass
        else:
            print(column,row[column])
            condition &= (df[column] == row[column]) 

    refRow = df[condition]

    if not refRow.empty:
        # Extract the Cq_mean from the reference row
        reference_Cq = refRow['Cq_mean'].values
        # Normalize the Cq_mean of the current row by subtracting the reference Cq
        return ((row['Cq_mean'] - reference_Cq))
    else:
        # If no matching reference row is found (it should exist in this case)
        return None

def std_to_reference(row, df,col,val,matches):
    # Find the reference row where Sample == 0.1 and RT/Fluor match
    condition = (df[col] == val)
    for column in matches:
        if column == col:
            pass
        else:
            print(column,row[column])
            condition &= (df[column] == row[column]) 

    refRow = df[condition]

    if not refRow.empty:
        # Extract the Cq_std from the reference row
        reference_std = refRow['Cq_std'].values
        # Normalize the Cq_mean of the current row by subtracting the reference Cq
        return (np.sqrt(row['Cq_std']*row['Cq_std'] + reference_std**2))
    else:
        # If no matching reference row is found (it should exist in this case)
        return None

def plotCq(dfMeta,inputfolder,col,val,xval,hueval,filtered,fval):

    col+='_'
    try:
        xval+='_'
    except:
        xval = None
    try:
        hueval+='_'
    except:
        hueval = None

    try:
        filtered+='_'
    except:
        filtered = None
    
    filesCq = glob.glob(inputfolder+"/*Quantification Cq Results.csv")

    dfCq = pd.read_csv(filesCq[0])
    for x in ['A','B','C','D','E','F','G','H']:
        dfCq['Well'] = dfCq['Well'].str.replace(x+'0',x)

    dfCq = dfCq[['Well','Fluor','Cq']]

    dfCq = pd.merge(dfMeta, dfCq, on='Well')

    cols = list(dfCq.columns)[1:-1]

    dfCq = dfCq.groupby(cols).agg({'Cq':['mean','std']}).reset_index()
    dfCq.columns = ['_'.join(col1).strip() for col1 in dfCq.columns.values]
    print(dfCq)

    cols = list(dfCq.columns)[1:-2]

    dfCq['delCq'] = dfCq.apply(lambda row: normalize_to_reference(row, dfCq,col,val,cols), axis=1)
    dfCq['delStd'] = dfCq.apply(lambda row: std_to_reference(row, dfCq,col,val,cols), axis=1)

    for row in range(len(dfCq['delCq'])):


        dfCq['delCq'][row] = dfCq['delCq'][row][0]
        dfCq['delStd'][row] = dfCq['delStd'][row][0]

    dfCq['FC1'] = np.power(2,-dfCq['delCq'])
    dfCq['FC1std'] = np.abs(dfCq['FC1'])*np.abs(-np.log(2)*dfCq['delStd'])

    if filtered == None:
        dfCqTemp = dfCq
    else:
        dfCqTemp = dfCq[dfCq[filtered] == fval]

    duplicates=1000
    #duplicate observations to get good std bars
    dfCopy = dfCqTemp.loc[dfCqTemp.index.repeat(duplicates)].copy()
    dfCopy['FC1'] = np.random.normal(dfCopy['FC1'].astype('float').values,dfCopy['FC1std'].astype('float').values)

    sns.barplot(data = dfCopy, x = xval, y='FC1',hue = hueval,errorbar='sd')
    
    plt.savefig(inputfolder+'/delCq.png')
    plt.savefig(inputfolder+'/delCq.svg')
    plt.close()

    return(dfCq)


################################################################################
#WL1 analysis functions

def vectorize(folder,lb,cap):

    files = glob.glob(folder+'Kernels/*_Kernel.csv')

    kMax = 0


    if cap == None:
        for file in files:

            kMaxT = int(file.split('/')[1].split('_')[0])

            if kMaxT>kMax:

                kMax = kMaxT

    elif cap != None:
        kMax = cap-1
        
    dfTemp = pd.read_csv(folder+'Kernels/'+str(kMax)+'_Kernel.csv')

    dim = max(dfTemp['Label']+1)

    strucs = dfTemp['Structure'].unique()

    vectors = {}

    ranges = []

    for struc in strucs:

        vectors[struc] = np.zeros(shape=dim)

    bar = ChargingBar('Vectorizing Kernels', max=kMax, suffix = '%(percent).1f%% - %(eta)ds')
    for file in range(lb,kMax):
        
        df = pd.read_csv(folder+'Kernels/'+str(file)+'_Kernel.csv')

        values = df.to_numpy()

        ranges.append(max(df['Label']))

        for row in values:

            vectors[row[1]][row[2]] = row[3]

        bar.next()

    bar.finish()

    return(vectors)

def entropyTrim(folder,vectors,ethresh):

    #read in Entropies
    dfTemp = pd.read_csv(folder+'VectorData/Entropy.csv')
    dfTemp = dfTemp[dfTemp['Entropy']<=ethresh]

    #make list of dimensions that do not benefit from additional data
    old = list(dfTemp['Old'].unique())

    dfTemp = pd.read_csv(folder+'VectorData/Transformations.csv')

    #gather list of uninformative dimensions (i.e. dimensions that low entropy dimensions transform into)
    dfTemp2 = dfTemp[dfTemp['Old'].isin(old)]
    new = list(dfTemp2['New'].unique())
    
    #trim values in new that spill into the itteration above max itteration considered
    new = np.array(new)
    new = new[new<vectors.shape[1]]
    dimsKept = np.arange(vectors.shape[1])

    vectors = np.delete(vectors, new, axis = 1)

    dimsKept = np.delete(dimsKept, new)

    return(vectors,dimsKept)

def focusDim(folder,arrays,target,dimsKept):

    vecCount = np.count_nonzero(arrays, axis=0)

    entropy = np.divide(vecCount,len(arrays))
    
    #convert fraction to entropy
    entropy = np.nan_to_num(-np.multiply(entropy,np.log2(entropy)))

    x = 0

    while len(entropy[entropy>=x]) > target:

        x+=0.0001


    print('Entropy Limit: ',x)
    rem = np.flatnonzero(entropy < x)

    arrays = np.delete(arrays, rem, axis = 1)
    dimsKept = np.delete(dimsKept, rem)

    X=np.arange(len(arrays))
    Y=-X/len(arrays)*np.log2(X/len(arrays))

    fig, ax1 = plt.subplots()

    sns.histplot(x = vecCount, binwidth = 1, color = '#A6A6A6')
    ax1.set_xlabel('Number of Structures Containing Subtree')
    ax1.set_ylabel('Number of Subtrees')

    ax2 = ax1.twinx()

    sns.lineplot(x=X,y=Y, color = 'k')
    sns.lineplot(x=X,y=x, color = 'orange')
    ax2.set_ylabel('Entropy Contribution')

    ax1.set_yscale('log')

    plt.savefig(folder+'VectorData/EntropyThreshold.png')
    plt.savefig(folder+'VectorData/EntropyThreshold.svg')
    plt.close()

    return(arrays, dimsKept,x)


#Set each dimension to set max value = 1
def normalizeArray(array,norm):

    if norm == 'max':

        array = np.divide(array,np.max(array,axis=0))

    elif norm == 'none':
        pass

    elif norm == 'minmax':
        pass

    elif norm == 'robust':
        array = np.divide(np.subtract(array,np.median(array,axis = 0)),np.subtract(*np.percentile(array, [75, 25], axis = 0)))

    elif norm == 'unit':
        array = array * np.divide(1,np.linalg.norm(array,axis = 1)).reshape(-1,1)

    elif norm == 'z-score':
        array = np.divide(np.subtract(array,np.mean(array, axis = 0)),np.std(array, axis = 0))
    
    else:
        pass

    array = np.nan_to_num(array)

    return(array)

#calculate shannon entropy for each subtree dimension
def Shannon(series):

    value_counts = np.divide(series,series.sum())
    entropy = -np.sum(value_counts * np.log2(value_counts))

    return(entropy)

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
'''
Core Functions for calling directly. 
Graph()
Graph3D()
readMeta()
WL1vectors()
'''

################################################################################
#import human readable plate map and convert into computer readable df
def readMeta(file):

    df = pd.DataFrame()

    df['Well'] = ['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12',
                  'B1','B2','B3','B4','B5','B6','B7','B8','B9','B10','B11','B12',
                  'C1','C2','C3','C4','C5','C6','C7','C8','C9','C10','C11','C12',
                  'D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12',
                  'E1','E2','E3','E4','E5','E6','E7','E8','E9','E10','E11','E12',
                  'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
                  'G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12',
                  'H1','H2','H3','H4','H5','H6','H7','H8','H9','H10','H11','H12']

    xls = pd.ExcelFile(file)

    sheets = xls.sheet_names

    for sheet in sheets:

        with pd.ExcelFile(file) as xls:
            dfTemp = pd.read_excel(xls,sheet)

            dfTemp = dfTemp.set_index('Unnamed: 0')
            dfTemp = dfTemp.reset_index().melt(id_vars='Unnamed: 0', var_name='Column', value_name=sheet)
            dfTemp['Well'] = dfTemp['Unnamed: 0']+dfTemp['Column'].astype(str)

            dfTemp = dfTemp.drop(columns=['Unnamed: 0','Column'])

            df = pd.merge(df, dfTemp, on='Well')

    return(df)

################################################################################
#read in list of files or list of dot-bracket (string,string) tuples
#convert to list of networkX graphs
def convert(files,**kwargs):

    args = dict(kwargs.items())

    try:
        form = args['format']
        
    except:
        form = 'auto'

    try:
        prefix = args['prefix']
        
    except:
        prefix = '#'


    G = []
    names = []
    if form == 'db':
        for file in files:

            name,seqs,pairs = read_db_structures(file)

            names.append(name)

            G.append(create_db_graph(seq,pairs,np.zeros(len(seq))))

    elif form == 'ct':
        for file in files:

            name, struc = read_ct_structures(file,prefix)

            names.append(name)

            G.append(create_ct_graph(struc[0],'',np.zeros(len(seq))))

    elif form == 'tuple':
        name = file[2]

        seq = list(file[1])

        pairs = list(file[0])

        names.append(name)
        G.append(create_db_graph(seq,pairs,np.zeros(len(seq)+1)))

    elif form == 'auto':
        for file in files:

            if file[-2:] =='db':

                name,seqs,pairs = read_db_structures(file)

                names.append(name)

                G.append(create_db_graph(seq,pairs,np.zeros(len(seq))))

            elif file[-2:] == 'ct':
                name, struc = read_ct_structures(file,prefix)

                names.append(name)

                G.append(create_ct_graph(struc[0],'',np.zeros(len(seq))))

            else:
                name = file[2]

                seq = list(file[1])

                pairs = list(file[0])

                names.append(name)
                G.append(create_db_graph(seq,pairs,np.zeros(len(seq)+1)))
                

    else:
        pass

    return(G,names)

#Create Graph from file
def graph(filename,**kwargs):

    newpath = r'Structures' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    args = dict(kwargs.items())

    try:
        num_strucs = args['num_strucs']
        
    except:
        num_strucs = 1

    try:
        prefix = args['prefix']
        
    except:
        prefix = '#'

    #plot color default:none
    try:
        color = args['color']
        color_type = 'varna'
    except:
        color = None
        color_type = None

    #plot bases default:false
    try:
        bases = args['bases']
    except:
        bases = False

    #node size default:10
    try:
        node_size = args['node_size']
    except:
        node_size = 10

    #view graph default:False
    try:
        view = args['view']
    except:
        view = False

    #view graph default:10
    try:
        edge_color = args['edge_color']
    except:
        edge_color = True

    try:
        dim = args['dim']
        
    except:
        dim = 2



    #read in file if dot-bracket
    if filename[-2:]=='db':
    
        names,seqs,pairs = read_db_structures(filename)

    #read in file if connectivity table
    elif filename[-2:] == 'ct':
        
        names, seqs = read_ct_structures(filename,prefix)

    #read in colors from varna file
    if color_type == 'varna':
        with open(color, 'r') as file:
            # Read the lines
            colors = file.readlines()
        newcolors = [0.25]
        for x in range(len(colors)):
            newcolors.append((float(colors[x][:-2])+1)/2)
        file.close()

    else:
        newcolors = np.zeros(len(seqs[0])+1)


    graphs = []
    
    if filename[-2:]=='db':
        
        if num_strucs == 'all':
            num_strucs = len(pairs)
            
        for x in range(num_strucs):
            try:
                G = create_db_graph(seqs[x],pairs[x],newcolors)
                graphs.append(G)
            except:
                break


    elif filename[-2:] == 'ct':

        if num_strucs == 'all':
            num_strucs = len(seqs)
        
        for x in range(num_strucs):

            try:
                G = create_ct_graph(seqs[x],'',newcolors)
                graphs.append(G)

            except:
                break

    
    positions = []
    for x in range(len(graphs)):

        pos = plotGraph(graphs[x],names[x],color,node_size,bases,view,edge_color)
        
        positions.append(pos)

    return

################################################################################

#Create Graph from file
def graph3D(filename,**kwargs):

    newpath = r'Structures' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    args = dict(kwargs.items())

    try:
        num_strucs = args['num_strucs']
        
    except:
        num_strucs = 1

    try:
        prefix = args['prefix']
        
    except:
        prefix = '#'

    #plot color default:none
    try:
        color = args['color']
        color_type = 'varna'
    except:
        color = None
        color_type = None

    #plot bases default:false
    try:
        bases = args['bases']
    except:
        bases = False

    #node size default:10
    try:
        node_size = args['node_size']
    except:
        node_size = 10

    #view graph default:False
    try:
        view = args['view']
    except:
        view = True

    #view graph default:10
    try:
        edge_color = args['edge_color']
    except:
        edge_color = True


    #read in file if dot-bracket
    if filename[-2:]=='db':
    
        names,seqs,pairs = read_db_structures(filename)

    #read in file if connectivity table
    elif filename[-2:] == 'ct':
        
        names, seqs = read_ct_structures(filename,prefix)

    #read in colors from varna file
    if color_type == 'varna':
        with open(color, 'r') as file:
            # Read the lines
            colors = file.readlines()
        newcolors = [0.25]
        for x in range(len(colors)):
            newcolors.append((float(colors[x][:-2])+1)/2)
        file.close()

    else:
        newcolors = np.zeros(len(seqs[0])+1)


    graphs = []
    
    if filename[-2:]=='db':
        
        if num_strucs == 'all':
            num_strucs = len(pairs)
            
        for x in range(num_strucs):
            try:
                G = create_db_graph(seqs[x],pairs[x],newcolors)
                graphs.append(G)
            except:
                break


    elif filename[-2:] == 'ct':

        if num_strucs == 'all':
            num_strucs = len(seqs)
        
        for x in range(num_strucs):

            try:
                G = create_ct_graph(seqs[x],'',newcolors)
                graphs.append(G)

            except:
                break

    
    positions = []
    for x in range(len(graphs)):

        pos = plotGraph3D(graphs[x],names[x],view)
        
        positions.append(pos)

    return

################################################################################
#Define the nucleobase agnostic WL1 kernel
def WLkernel(G,**kwargs):

    #read in args
    args = dict(kwargs.items())

    try:
        cap = args['cap']
    except:
        cap = 25

    try:
        out = args['out']
        if out!='':
            if out[-1] != '/':
                out+='/'
    except:
        out = 'out/'

    try:
        names = args['names']
        for i in range(len(G)):
            nx.set_node_attributes(G[i], names[i], "Structure")
        
    except:
        print('Naming Structures Automatically')
        i = 0
        for g in G:
            nx.set_node_attributes(g, i, "Structure")
            i+=1

    newpath = out 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    newpath = out+'Kernels' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    newpath = out+'VectorData' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    #combine all graphs into one giant object
    H = nx.disjoint_union_all(G)

    nx.set_node_attributes(H, 0, "code")

    dfBig = pd.DataFrame(columns = ['Structure','Label','Count'])

    numLabels = 0

    labelCounter = 1

    labels = {}

    old = []
    new = []


    i = 0
    done = False
    ittStart = time.time()
    while not done and cap!=0 and i<cap:

        print("\nItteration: ", i)
        print("Itteration Time: ", time.time()-ittStart)
        ittStart = time.time()

        struc = []
        label = []
        itt = []

        bar = ChargingBar('Collecting Labels', max=len(H.nodes()), suffix = '%(percent).1f%% - %(eta)ds')
        for node in H.nodes():

            struc.append(H.nodes[node]['Structure'])
            label.append(H.nodes[node]['code'])
            itt.append(i)
            bar.next()
        bar.finish()


        print('Labels Collected')


        dicts = {'Structure': struc, 'Label':label}

        df = pd.DataFrame(dicts)

        df = df.groupby(['Structure','Label']).size().reset_index(name = 'Count')


        print('Labels Counted')

        
        #compare to see if the number of labels per itteration changed.
        newLabels = len(df['Label'].unique())
        if newLabels == numLabels:

            print('Complete')

            done = True
            

        else:
            i+=1
            numLabels = newLabels

            df.to_csv(out+'Kernels/'+str(i-1)+'_Kernel.csv')
            del df
            print('Kernel Saved')

            bar = ChargingBar('Renaming Nodes', max=len(H.nodes()), suffix = '%(percent).1f%% - %(eta)ds')
            #make a new code for every node
            for node in H.nodes():

                code = [H.nodes[neighbor]['code'] for neighbor in H.neighbors(node)]

                code.sort()

                newCode = str(H.nodes[node]['code'])

                for x in code:

                    newCode = newCode+'_'+str(x)

                if newCode not in labels:
                    labels[newCode] = labelCounter
                    labelCounter += 1


                H.nodes[node]['newcode'] = labels[newCode]
                bar.next()

            bar.finish()

            bar = ChargingBar('Finalizing Names', max=len(H.nodes()), suffix = '%(percent).1f%% - %(eta)ds')
            for node in H.nodes():

                bar.next()

                old.append(H.nodes[node]['code'])
                new.append(H.nodes[node]['newcode'])

                H.nodes[node]['code'] = H.nodes[node]['newcode']

            bar.finish()

    df2 = pd.DataFrame([labels]).transpose()
    df2.to_csv(out+'VectorData/Label_Decode.csv')

    #track changes from "old" label to "new" label
    #calculate the information gain by including additional dimension. 
    df3 = pd.DataFrame({'Old':old,'New':new})
    df3 = df3.groupby(['Old','New']).size().reset_index(name = 'RenameCount')
    df4 = df3.groupby('Old').agg({'RenameCount':Shannon})
    df4 = df4.rename(columns = {'RenameCount':'Entropy'})
    df3.to_csv(out+'VectorData/Transformations.csv')
    df4.to_csv(out+'VectorData/Entropy.csv')

    del df2,df3,df4
    return()

################################################################################
#Extract the WLkernel subtree vectors.
#return dictionary or arrays and keys
#return dimensions kept as a list
def WLvectors(**kwargs):

    #read in args
    args = dict(kwargs.items())

    try:
        folder = args['folder']
        if folder!='':
            if folder[-1] != '/':
                folder+='/'
    except:
        folder = 'out/'

    try:
        cap = args['upper']
    except:
        cap = 25

    try:
        lb = args['lower']
    except:
        lb = 0

    try:
        ethresh = args['ethresh']
    except:
        ethresh = 0

    try:
        target = args['target']
    except:
        target = 10**12

    try:
        norm = args['norm']
    except:
        norm = 'max'

    dicts = {'Number of WL1 Cycles Processed':cap,
             'Minimal Shannon Entropy to Retain':ethresh,
             'Target Number of Dimensions':target,
             'Normalization Method':norm}

    vectors = vectorize(folder,lb,cap)

    arrays = np.array(list(vectors.values()))
    keys = np.array(list(vectors.keys()))

    dicts['Number of Structures Analyzed'] = len(arrays)
    dicts['Initial Vector Dimension'] = len(arrays[0])

    arraysTrim,dimsKept = entropyTrim(folder,arrays,ethresh)

    dicts['Vector Dimension after Entropy Thresholding'] = len(arraysTrim[0])

    arraysTrim,dimsKept,S = focusDim(folder,arraysTrim, target, dimsKept)

    dicts['Entropy Threshold for Target Thresholding'] = S
    dicts['Vector Dimension after Target Thresholding'] = len(arraysTrim[0])
    
    arraysNorm = normalizeArray(arraysTrim,norm)

    with open(folder+"WLvectors_report.json", "w") as outfile: 
        json.dump(dicts, outfile)
    outfile.close()
    

    return(arraysNorm, keys, dimsKept)
