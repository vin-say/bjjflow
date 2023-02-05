#%%
import pandas as pd
import numpy as np
import graphviz
import os
from graphviz import Digraph


os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\bin'

#%%
df = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='Flow')
df_tech = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='Techniques')
df_subs = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='Submissions')
states = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='States')['States'].to_list()


font = 'helvetica'
gph = Digraph('G', filename='bjj_flow_vps.gv')

# NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph

# 1/29 turn off techniques list
# techniques = df_tech['Technique'].to_list()
techniques = []

subs = df_subs['Submissions'].to_list()

color_state = 'chartreuse'
color_counter = 'coral'
color_move = 'cadetblue1'
color_sub = 'crimson'

shape_state = 'doubleoctagon'
shape_counter = 'ellipse'
shape_move = 'box'
shape_sub = 'diamond'



for _, row in df.iterrows():
    if isinstance(row['Position'],str) & isinstance(row['Result'],str) & isinstance(row['Move'],str):
        
        if row['Position'] in states:
            gph.attr('node', shape=shape_state, color=color_state, style='filled', fontname=font)
            gph.node(row['Position'])
            position_alias = row['Position']
        else:
            position_alias = row['Dilemma']+row['Position']


        if row['Result'] in states:
            gph.attr('node', shape=shape_state, color=color_state, style='filled', fontname=font)
            gph.node(row['Result'])
            result_alias = row['Result']
        else:
            result_alias = row['Dilemma']+row['Result']


        if row['Result'] in subs:
            shape_result = shape_sub
            color_result = color_sub
        else:
            shape_result = shape_counter
            color_result = color_counter

        with gph.subgraph(name='cluster'+row['Dilemma']) as g:

            g.attr('node', shape='ellipse', color='coral', style='filled', fontname=font)
            # g.node(row['Dilemma']+row['Position'], label=row['Position'])
            


            # g.node(row['Dilemma']+row['Result'], label=row['Result'])
            
            g.attr('node', shape=shape_move, color=color_move, style='filled')

            if row['Move'] in techniques:
                tech_idx = df_tech[df_tech['Technique']==row['Move']].index.item()
                tech_name = df_tech.iloc[tech_idx]['Technique']
                with g.subgraph(name='cluster'+tech_name) as t:
                    # exclude tech name and drop NaNs 
                    steps = [x for x in df_tech.iloc[tech_idx].to_list()[1:] if isinstance(x,str)] 
                    for ii in range(len(steps)-1):
                        t.edge(steps[ii],steps[ii+1])
                        print(steps[ii])
                    
                    t.attr(label=tech_name, fontname=font)
                #permanently replace row value with cluster name
                move_alias = 'cluster'+tech_name# alias of move cell 
                # g.node(row['Dilemma']+row['Move'], label=row['Move'])

            else:
                move_alias = row['Dilemma']+row['Move'] # alias of move cell
            
            g.node(move_alias, label=row['Move'])
            
            gph.attr('node', shape=shape_move, color=color_move, style='filled', fontname=font)
            gph.edge(position_alias, move_alias)

            if row['Result'] in states:
                gph.attr('node', shape=shape_result, color=color_result, style='filled', fontname=font)
                gph.node(result_alias, label=row['Result'])
                gph.edge(move_alias, result_alias)
            else:
                g.attr('node', shape=shape_result, color=color_result, style='filled', fontname=font)
                g.node(result_alias, label=row['Result'])
                g.edge(move_alias, result_alias)

            # gph.edges([(position_alias, move_alias),
            #          (move_alias, row['Dilemma']+row['Result'])])


            g.attr(label=row['Dilemma'], fontname=font)
        # g.attr('node', shape='ellipse', color='coral', style='filled', fontname='helvetica')
        # g.node(row['Position'], label=row['Position'])
        # g.node(row['Result'], label=row['Result'])
        
        # g.attr('node', shape='box', color='cadetblue1', style='filled')
        # g.node(row['Move'], label=row['Move'])
        
        # g.edge(row['Position'], row['Move'])
        # g.edge(row['Move'], row['Result'])
gph
# %%
