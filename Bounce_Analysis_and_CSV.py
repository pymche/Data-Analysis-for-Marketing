#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter
import seaborn as sns
import csv


bounce = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Work/Analysis/Bounce/campaign_bounces_20200315.csv')
crm = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Work/Data/Leads_001.csv')


print(bounce.shape, crm.shape)


bounce['Company'] = bounce['Company Name']


df = pd.merge(bounce, crm, how="inner", left_on="Contact Email", right_on="Email", sort=False)


df.columns.values


df = df[['Record Id', 'Company_x', 'First Name_x',
       'Last Name_x', 'Title_x', 'Email', 'Lead Source', 'Lead Status_y', 'Industry_y', 'Created Time', 'Tag', 'Enter Workflow_y']]


df.loc[:, 'Created Time']


df['Created Time'] = pd.to_datetime(df['Created Time'], format='%Y-%m-%d %H:%M:%S')


df['Created Time'] = df['Created Time'].dt.to_period('M')
df['Created Time'] = df['Created Time'].dt.strftime('%Y-%m')


df['Created Time']


sns.set_style("whitegrid")

def pie(dataframe, pie_title):
    c = dict(Counter(dataframe.values))
    labels = [key for key, value in c.items()]
    data = [value for key, value in c.items()]
    plt.figure(figsize=(8,8))
    plt.title(pie_title)
    plt.pie(data, labels=labels)
    
def graph(dataframe, graph_title):
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=45)
    plt.title(graph_title)
    sns.histplot(dataframe, bins=40)


plt.figure(figsize=(8,8))
graph(df.sort_values(by="Created Time", ascending=True)['Created Time'], 'Created Time of Bounces in CRM 9th March 2021')


pie(df['Lead Status_y'], 'Bounce Lead Status 9th March 2021')


pie(df['Lead Source'], 'Bounce Lead Source 9th March 2021')


# ### Splitting data into two CSV Files
# 
# * One with the lead contacts themselves, with first name, last name, email, record ID, need to find out their new company, email and title
# 
# * Another one with the company, title, need to find out the replacement of that position - their first name, last name, title, email

print('Number of bounces in total (active contacts)')
df.shape[0]


### Excluding the ones that have entered Tier 1 Generic
tier1 = df['Enter Workflow_y'] != 'Tier 1 Generic'


print('Number of bounces that have not entered Tier 1 Generic')
df[tier1].shape[0]


df[['Record Id', 'First Name_x', 'Last Name_x', 'Email']].iloc[[1]]


with open('Bounced_Leads.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    cols = ['Record Id', 'First Name_x', 'Last Name_x', 'Company_x']
    
    writer.writerow(['Record Id', 'First Name', 'Last Name', 'Old Company', 'Tag from Campaign', 'New Company', 'New Email', 'New Title'])

    for x in range(df.shape[0]):
        content = list(df[cols].iloc[x])
        content.append('bounce')
        writer.writerow(content)


with open('Bounced_Company_Title.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    cols = ['Company_x', 'Title_x', 'Email']
    
    writer.writerow(['Company', 'Title', 'Email Sample', 'First Name', 'Last Name', 'Title', 'Email'])

    for x in range(df.shape[0]):
        writer.writerow(list(df[cols].iloc[x]))


# ### Tag == 'bounce'

df[['Record Id', 'First Name_x', 'Last Name_x', 'Company_x', 'Tag']]


filt = df['Tag'] == 'bounce'
print(df[filt].shape[0])




