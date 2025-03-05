import pandas as pd
import numpy as np

champion = 'phoveus'
pd.set_option('mode.chained_assignment',None)
df = pd.read_json("data.json")
it = pd.read_json("items.json")

champ = df.set_index('id#')
ch = champ[champ['hero']==champion]

ch['weight'] = (ch['matches'] * ch['win_rate'])/100
ch['first'] = 1
ch['second'] = 2
ch['third'] = 3
ch['fourth'] = 4
ch['fifth'] = 5
ch['sixth'] = 6

#df for most bought item
first_item = ch.pivot_table(values='weight',index='item1',aggfunc='sum').reset_index()
second_item = ch.pivot_table(values='weight',index='item2',aggfunc='sum').reset_index()
third_item = ch.pivot_table(values='weight',index='item3',aggfunc='sum').reset_index()
fourth_item = ch.pivot_table(values='weight',index='item4',aggfunc='sum').reset_index()
fifth_item = ch.pivot_table(values='weight',index='item5',aggfunc='sum').reset_index()
sixth_item = ch.pivot_table(values='weight',index='item6',aggfunc='sum').reset_index()

all = it \
.merge(first_item,how='left',left_on='shortname',right_on='item1',suffixes=('','_1')) \
.merge(second_item,how='left',left_on='shortname',right_on='item2',suffixes=('','_2')) \
.merge(third_item,how='left',left_on='shortname',right_on='item3',suffixes=('','_3')) \
.merge(fourth_item,how='left',left_on='shortname',right_on='item4',suffixes=('','_4')) \
.merge(fifth_item,how='left',left_on='shortname',right_on='item5',suffixes=('','_5')) \
.merge(sixth_item,how='left',left_on='shortname',right_on='item6',suffixes=('','_6'))
all_item = all[['item','shortname','type','weight','weight_2', \
                'weight_3','weight_4','weight_5','weight_6']].fillna(0)
all_item['total_score'] = all_item[['weight','weight_2','weight_3','weight_4','weight_5','weight_6']] \
    .sum(axis = 1)
all_item['weight_rank'] = all_item['total_score'].rank(method='max',ascending=False)

#df for most common order of items
p1 = ch[['item1','first']].rename(columns={'item1': 'shortname', 'first': 'rank_order'})
p2 = ch[['item2','second']].rename(columns={'item2': 'shortname', 'second': 'rank_order'})
p3 = ch[['item3','third']].rename(columns={'item3': 'shortname', 'third': 'rank_order'})
p4 = ch[['item4','fourth']].rename(columns={'item4': 'shortname', 'fourth': 'rank_order'})
p5 = ch[['item5','fifth']].rename(columns={'item5': 'shortname', 'fifth': 'rank_order'})
p6 = ch[['item6','sixth']].rename(columns={'item6': 'shortname', 'sixth': 'rank_order'})

common_item = pd.concat([p1,p2,p3,p4,p5,p6])
common_order = common_item.pivot_table(values='rank_order',index='shortname',aggfunc='mean').reset_index()
common_order['final_rank_order'] = common_order['rank_order'].rank(method='first')

summary = all_item.merge(common_order,how='left',on='shortname')
summary= summary[['item','shortname','type','total_score','weight_rank','final_rank_order']].sort_values('total_score',ascending=False)
summary.to_excel(champion + ".xlsx",sheet_name = champion,index=False)