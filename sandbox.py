#%%
import pandas as pd
import numpy as np
import graphviz
import os
from graphviz import Digraph

# necessary otherwise pkg can't connect with Graphviz software
os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\bin'

#%%
df = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='Flow')
df_tech = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='Techniques')
df_subs = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='Submissions')
states = pd.read_excel('bjj_flow_vps.xlsx',sheet_name='States')['States'].to_list()

# drop rows with special characters indicating headings
df = df[~(df['Position'].str.contains('--') & 
          ~df['Position'].isna())].reset_index(drop=True)

font = 'helvetica'
gph = Digraph('G', filename='bjj_flow_vps.gv', strict=True)

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

for _, row in df.iloc[:].iterrows():

    # Check if row has minimum required columns filled
    if isinstance(row['Position'],str) & isinstance(row['Result'],str):
        
        # reaction_only indicates opponent is proactively making move against you
        reaction_only = False
        if not isinstance(row['Move'],str):
            reaction_only = True

        # 'state' indicates a fundamental position, and thus should be excluded from dilemma subsets
        if row['Position'] in states:
            gph.attr('node', shape=shape_state, color=color_state, style='filled', fontname=font)
            gph.node(row['Position'])
            position_alias = row['Position']
        else:
            # dilemma is appended to alias for edge cases where move is named the same across dilemmas/positions
            position_alias = row['Dilemma']+row['Position'] 

        if row['Result'] in states:
            gph.attr('node', shape=shape_state, color=color_state, style='filled', fontname=font)
            gph.node(row['Result'])
            result_alias = row['Result']
        else:
            result_alias = row['Dilemma']+row['Result']

        # submissions are distinguished so they'll have different appearance
        if row['Result'] in subs:
            shape_result = shape_sub
            color_result = color_sub
        else:
            shape_result = shape_counter
            color_result = color_counter

        # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
        #       so that Graphviz recognizes it as a special cluster subgraph
        with gph.subgraph(name='cluster'+row['Dilemma']) as g:

            if not reaction_only:
                # 1/29 techniques feature isn't operable, techniques list set to empty
                if row['Move'] in techniques:
                    tech_idx = df_tech[df_tech['Technique']==row['Move']].index.item()
                    tech_name = df_tech.iloc[tech_idx]['Technique']
                    with g.subgraph(name='cluster'+tech_name) as t:
                        # exclude tech name and drop NaNs 
                        steps = [x for x in df_tech.iloc[tech_idx].to_list()[1:] if isinstance(x,str)] 
                        for ii in range(len(steps)-1):
                            # if ii == 0:
                            #     g.edge(
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

            else:
                gph.attr('node', shape=shape_counter, color=color_counter, style='filled', fontname=font)
                gph.edge(position_alias, result_alias)

            if row['Result'] in states:
                gph.attr('node', shape=shape_result, color=color_result, style='filled', fontname=font)
                gph.node(result_alias, label=row['Result'])
                if not reaction_only:
                    gph.edge(move_alias, result_alias)
                    
            else:
                g.attr('node', shape=shape_result, color=color_result, style='filled', fontname=font)
                g.node(result_alias, label=row['Result'])
                if not reaction_only:
                    g.edge(move_alias, result_alias)

            # add dilemma name to subset border
            g.attr(label=row['Dilemma'], fontname=font)

gph.view()
# %%
