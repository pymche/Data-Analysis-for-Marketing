#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sys
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


df = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/Data/Leads_001.csv')


df.columns.values


df['Company']


#How many companies we have in CRM

len(df['Company'].unique())


#Name of companies in our CRM

company = df['Company'].sort_values(ascending=True)

for y in company.unique():
    print(y)


# ### Find out whether company CRM already has companies in email list that has been provided to us

# ### List 1

preview = pd.read_excel('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/PreviewRightcheckHRDirectorsAllUK.xls')


preview_comp = preview['Company Name'].unique()


dupe = [a for a in preview_comp if a in company.unique()]


len(dupe)


dupe


# ### List 2 after filtering out unwanted sectors from List 1

preview2 = pd.read_excel('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/PreviewRightCheckHRDirexc.CharitiesUK.xls')


preview_comp2 = preview2['Company Name'].unique()
dupe2 = [a for a in preview_comp2 if a in company.unique()]


# Number of companies in that list that already exist in our CRM

len(dupe2)


# No. of unique companies in that list

len(preview_comp2)


# No. of contacts in that list

preview2.shape[0]


# # Company

print('No. of contacts on CRM Leads:', df.shape[0])

totalcomp = len(df['Company'].unique())
print('No. of unique companies in our CRM:', totalcomp)

df['Enter Workflow'].fillna('None', inplace=True)

reachedcomp = df[(df['Enter Workflow'] == 'Tier 1 Generic') | (df['Enter Workflow'] == 'Blog Subscription')]
reachedcomplen = len(reachedcomp['Company'].unique())
print('No. of contacts that have been reached out by our emails:', reachedcomp.shape[0])
print('No. of unique companies that have been reached out by our emails:', reachedcomplen)

unreached = totalcomp - reachedcomplen
print("No. of unique companies that haven't been reached out by us:", unreached)

slices = [unreached, reachedcomplen]
labels = ['Unreached', 'Reached']
plt.figure(figsize=(5,5))
plt.pie(slices, labels=labels, autopct='%.2f%%')
plt.title('% of Companies in our CRM that have been reached out by our emails')
plt.tight_layout()
plt.show()


# Unique companies that have NOT been reached out by us

unreachedunique = df[df['Company'].isin([x for x in company.unique() if x not in reachedcomp['Company'].unique()])]['Company'].unique()
len(unreachedunique)


# Unique companies that have ALREADY been reached out by us

reachedunique = df[df['Company'].isin([x for x in company.unique() if x in reachedcomp['Company'].unique()])]['Company'].unique()
len(reachedunique)


# Find out how many companies in new email list provided to us are in the list of companies in our CRM that we have NOT reached out to

dupe3 = [a for a in preview_comp2 if a in unreachedunique]
print(len(dupe3))


# Find out how many companies in new email list provided to us are in the list of companies in our CRM that we have ALREADY reached out to

dupe4 = [a for a in preview_comp2 if a in reachedunique]
len(dupe4)


df[df['Company'].isin(unreachedunique.tolist())]['Industry']


c_all = dict(Counter(df[df['Company'].isin(unreachedunique.tolist())]['Industry']))
label_all = [key for key, value in c_all.items()]
count_all = [value for key, value in c_all.items()]
plt.figure(figsize=(8,8))
plt.pie(count_all, labels=label_all)
plt.title('Industries of Companies in CRM that we have not reached out to')




