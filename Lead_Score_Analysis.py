#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


sys.executable


df = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Work/Data/Leads_001.csv')


df.shape


df.columns.values


df['Campaign Status'].fillna('None', inplace=True)


tier1campaign = (df['Enter Workflow'] == 'Tier 1 Generic')


# # Leads who have entered Tier 1 Generic Email Campaign

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
plt.title('Industries of Tier 1 Generic Leads')


c = dict(Counter(tier1_df['Lead Source']))
label = [key for key, value in c.items()]
count = [value for key, value in c.items()]
plt.figure(figsize=(20,10))
plt.pie(count, labels=label)
plt.title('Lead Sources of Tier 1 Generic Leads')


# # Analysis of Leads who have completed the entire Tier 1 Generic Email Campaign

tier1done = (df['Tag from Campaign'] == 'Exited Tier 1 Generic')
tier1done_df = df[tier1done]
c = dict(Counter(tier1done_df['Industry']))
label = [key for key, value in c.items()]
count = [value for key, value in c.items()]
plt.figure(figsize=(20,10))
plt.pie(count, labels=label)
plt.title('Industries of Leads that completed Tier 1 Generic')


tier1done_df.shape


### Negative Score Leads

negative_filt = tier1done_df['Score from Campaign'] < 0


Negscore_df = tier1done_df[negative_filt]


Negscore_df[['Industry', 'Lead Source', 'Lead Status', 'Created Time']].head()


c = dict(Counter(Negscore_df['Industry']))
label = [key for key, value in c.items()]
count = [value for key, value in c.items()]
plt.figure(figsize=(20,10))
plt.pie(count, labels=label)
plt.title('Industries of Negative Score')


Negscore_df.shape


### Leads with Positive Score (>20)

high_filt = tier1done_df['Score from Campaign'] > 20
high_df = tier1done_df[high_filt]
c = dict(Counter(high_df['Industry']))
label = [key for key, value in c.items()]
count = [value for key, value in c.items()]
plt.figure(figsize=(20,10))
plt.pie(count, labels=label)
plt.title('Industries of Positive Score')


high_df.shape




