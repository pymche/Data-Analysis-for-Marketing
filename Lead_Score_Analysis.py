#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


sys.executable


df = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/Data/Leads_001.csv')


df.shape


df.columns.values


df['Campaign Status'].fillna('None', inplace=True)


tier1campaign = (df['Enter Workflow'] == 'Tier 1 Generic')


# # Leads who have entered Tier 1 Generic Analysis

tier1campaign = df['Enter Workflow'] == 'Tier 1 Generic'


df.loc[tier1campaign].shape


tier1_df = df.loc[tier1campaign]


fig, ax = plt.subplots(figsize=(20, 5))
sns.histplot(tier1_df, x="Score from Campaign", kde=True, bins=50, ax=ax)


c = dict(Counter(tier1_df['Industry']))
label = [key for key, value in c.items()]
count = [value for key, value in c.items()]
plt.figure(figsize=(20,10))
plt.pie(count, labels=label)
plt.title('Industries of leads who have entered Tier 1 Generic')


c = dict(Counter(tier1_df['Lead Source']))
label = [key for key, value in c.items()]
count = [value for key, value in c.items()]
plt.figure(figsize=(20,10))
plt.pie(count, labels=label)
plt.title('Lead Sources of Tier 1 Generic Leads')


# # Analysis of Leads who have completed the entire Tier 1 Generic

## New dataframe of those that have completed Tier 1 Generic

tier1done = (df['Tag from Campaign'] == 'Exited Tier 1 Generic')
tier1done_df = df[tier1done]


c_all = dict(Counter(tier1done_df['Industry']))
label_all = [key for key, value in c_all.items()]
count_all = [value for key, value in c_all.items()]
plt.figure(figsize=(20,10))
plt.pie(count_all, labels=label_all)
plt.title('Industries of Leads that completed Tier 1 Generic')


tier1done_df.shape


# ### Score Distribution of leads who have completed Tier 1 Generic

plt.figure(figsize=(30,8))
ax = sns.displot(data=tier1done_df, x="Score from Campaign", kde=True, binwidth=5)


tier1done_df['Score from Campaign'].quantile([.25, 0.95])


tier1done_df.shape[0]*(1-0.95)


# ## Negative Score (of those that have entered (instead of completed) Tier 1 Campaign

negative_filt = tier1_df['Score from Campaign'] < 0


Negscore_df = tier1_df[negative_filt]


Negscore_df[['Industry', 'Lead Source', 'Lead Status', 'Created Time']].head()


c = dict(Counter(Negscore_df['Industry']))
label = [key for key, value in c.items()]
count = [value for key, value in c.items()]
plt.figure(figsize=(20,10))
plt.pie(count, labels=label)
plt.title('Industries with Negative Score')


Negscore_df.shape


# ## Positive Score (>25)

high_filt = tier1done_df['Score from Campaign'] >= 25
high_df = tier1done_df[high_filt]

c_pos = dict(Counter(high_df['Industry']))
label_pos = [key for key, value in c_pos.items()]
count_pos = [value for key, value in c_pos.items()]
plt.figure(figsize=(20,10))
plt.pie(count_pos, labels=label_pos)
plt.title('Industries of Top 5% leads (Score > 25)')


high_df.shape


# ## Which industry performs best in Tier 1 Generic Campaign?
# 
# Out of the leads that have completed Tier 1 Generic, which industry performs best in terms of scoring high i.e. >25?

def percentage(x, y):
    value = x/y*100
    return value

score_dict={}

for lab in label_all:
    for lab2 in label_pos:
        if lab == lab2:
            score_dict[lab] = percentage(c_pos[lab], c_all[lab])

keys = [key for key, value in score_dict.items()]
vals = [value for key, value in score_dict.items()]

# Percentage of leads of each industry that have scored higher than 25%

plt.figure(figsize=(20,10))
plt.title('Percentage of each industry with Score > 25')
plt.xticks(rotation=70)
sns.barplot(x=keys, y=vals)




