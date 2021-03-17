#!/usr/bin/env python
# coding: utf-8

# # B2B Company CRM Database Analysis

# This report is conducted to analyse the 10,000+ contacts in the CRM of a B2B Software company. From 2016 when the CRM was created, new lead contacts (potential customers) have been added to the CRM from a wide range of sources. There has not been a consistent process to organise the CRM. It has become difficult to maintain and many emails have since become outdated in 2021 without being noticed. This analysis is an attempt to understand the nature of these contacts, i.e. when they have been added, their sources, as well as their engagement with the company's CRM throughout the years. This will allow the company to make better decisions on how to clean the CRM based on the quality of existing contacts.

import pandas as pd
import collections
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


df = pd.read_csv('/Users/melaniecheung/Desktop/Code/Work/latest_crm_data/Leads_001.csv')


df['Enter Workflow'].unique()


df.shape


# Columns of metrics available in the CRM Dataset for analysis

df.columns.values


# Fill in missing values in columns that will certainly be used

# ### Data Cleaning and creating custom plotting functions for later use

for col in ['Enter Workflow', 'Lead Status', 'Lead Source', 'Campaign Status']:
    df[col].fillna('None', inplace=True)


# This analysis is only restricted to contacts that have not been reached out by the company's email marketing campaigns in 2021.

df.drop(index=df[df['Enter Workflow'] != 'None'].index, inplace=True)


# Dropping columns / metrics that have more than 50% missing values

df['Tag'].isna().sum()
leads_no = df.shape[0]
print('Total number of leads that have not entered any 2021 email marketing campaigns:', leads_no)


def percent(x):
    per = df[x].isna().sum() / leads_no * 100
    return per

percent('Tag')


for x in df.columns:
    if x not in ['Lead Source', 'Lead Status', 'Lead Notes', 'Campaign Status', 'Tag']:
        if percent(x) > 50 or len(Counter(df[x].values)) < 3:
            df.drop(columns=x, inplace=True)


# Rearrange remaining useful columns / metrics

df = df[['Record Id', 'Company', 'First Name', 'Last Name',
       'Title', 'Email', 'Phone', 'Industry', 'Lead Source', 'Lead Status', 'Lead Notes', 'Tag', 'Score', 'Campaign Status',
       'Created Time', 'Modified Time', 'Last Activity Time','LAST_SENT_TIME']]


def graph(dataframe, graph_title):
    plt.figure(figsize=(15,5))
    plt.xticks(rotation=45)
    plt.title(graph_title)
    sns.histplot(dataframe, bins=40)
    
def pie(dataframe, pie_title):
    c = dict(Counter(dataframe.values))
    labels = [key for key, value in c.items()]
    data = [value for key, value in c.items()]
    plt.figure(figsize=(8,8))
    plt.title(pie_title)
    plt.pie(data, labels=labels)


# ### Check which time metric best represents 'Date added to CRM' and 'Last Activity in CRM'

time = [x for x in df.columns.values if 'time' in x.lower()]


time


df[time].head(10)


time = ['Modified Time', 'LAST_SENT_TIME']


df.drop(columns=time, inplace=True)


print(type(df['Created Time'][5]))

df['Created Time'] = pd.to_datetime(df['Created Time'], format='%Y-%m-%d %H:%M:%S')
df['Last Activity Time'] = pd.to_datetime(df['Last Activity Time'], format='%Y-%m-%d %H:%M:%S')

print(type(df['Created Time'][5]))

df['Created Month'] = df['Created Time'].dt.to_period('M')
df['Last Activity Month'] = df['Last Activity Time'].dt.to_period('M')

print(type(df['Created Month'][5]))

df['Created Month'] = df['Created Month'].dt.strftime('%Y-%m')
df['Last Activity Month'] = df['Last Activity Month'].dt.strftime('%Y-%m')

print(type(df['Created Month'][5]))


df['Last Activity Month'].fillna(pd.to_datetime('1900-01', format='%Y-%m').to_period('M').strftime('%Y-%m'), inplace=True)
print(type(df['Last Activity Month'][5]))


df[['Created Month', 'Last Activity Month']].isna().sum()


# ### Cleaned Dataframe

df.shape


# ### Year/Month of leads added to CRM (all leads)

graph(df['Created Month'], 'Year/Month added to CRM (all leads)')


# ### Year/Month of Last Activity from CRM

graph(df.sort_values(by="Last Activity Month", ascending=False)['Last Activity Month'], 'Year/Month of Last Activity (all leads) e.g. Emails/Campaigns have been sent from CRM')


# ### Overall Lead Source

pie(df['Lead Source'], 'Overall Lead Sources')


# ### Lead Source by Year

for year in range(df['Created Time'].dt.year.min(), df['Created Time'].dt.year.max() + 1):
    year_filt = df['Created Time'].dt.year == year
    df_year = df[year_filt]
    pie(df_year['Lead Source'], 'Lead Source in ' + str(year))


# ### Active Leads (Last Activity Time later than Feb 2020)

active = df[df['Last Activity Time'] > '2020-02']
print('Number of Active Leads in CRM:', active.shape[0])


pie(active['Lead Source'], 'Lead Source of Active Leads')


# ### Empty Emails

no_emails = df['Email'].isnull() == True


emails_df = df[no_emails]
print('Number of leads without email:', emails_df.shape[0])


pie(emails_df['Lead Source'], 'Sources of Leads with empty emails')


graph(emails_df['Created Month'], 'Year/Month added to CRM (leads w/ empty emails)')


# ### Lead Status - None, Suspects
# 
# With the little organisation existing in the CRM database, our best assumption is that leads with Lead Status equals to 'None' or 'Suspects' are the leads that we would like to focus on

df['Lead Status'].unique()


c = Counter(df['Lead Status'])
print(c)


ax = plt.figure(figsize=(15, 5))
plt.xticks(rotation=45)
plt.title('Lead Status Counts')
g = sns.countplot(data=df, x="Lead Status")


# ### Analysis of Lead Status = Suspect

suspect_filt = df['Lead Status'] == '3. Suspect (NDMC)'
suspect_df = df[suspect_filt]
print('Number of leads with Lead Status: 3.Suspect (NDMC) - potential customers:', suspect_df.shape[0])

graph(suspect_df['Created Month'], 'Suspects Time added to CRM')


# ### Analysis of Lead Status = None

none_filt = df['Lead Status'] == 'None'
none_df = df[none_filt].sort_values(by="Created Time", ascending=True)
print('Number of leads with Lead Status = None:', none_df.shape[0])

graph(none_df['Created Month'], 'Lead Status = None - Time added to CRM')


# ### Time added to CRM vs Last Activity Time

g = sns.relplot(x='Created Month', y='Last Activity Month', data=df[df['Last Activity Month'] > '1990-01'], palette="viridis", size = 12,aspect =3)
plt.xticks(rotation=45)
plt.title("Lead's Time Added to CRM and Last Activity Time from CRM")


# ### Time in CRM

# The longer the duration a lead has been in the CRM and receiving our company's email campaign, the more valuable the lead is - we want to keep them in the CRM and engage with them in the future. The duration of their time spent in the CRM is calculated by Last Activity Time minus Created Time. We will have a look at the leads that have been in our CRM and have been engaging with us, either through email campaigns or emails, for more than two years, regardless of the time since they have been added to the CRM.

df['CRM time'] = df['Last Activity Time'] - df['Created Time']
df['Days in CRM'] = df['CRM time'].dt.days


df['Days in CRM'].fillna(-100, inplace=True)


# 'Campaigns Index' is generated by the following custom function, as an indication of how many campaigns have been sent out to a particular lead. The more letters there is within 'Campaign Status', the higher engaged the company CRM is with that particular lead. The following example shows how the 'Campaign Status' from the original database is formatted.

df['Campaign Status'][583]


def check_len(x):
    if x != 'None':
        x = len(x)
        return x
    elif x == 'None':
        x = 0
        return x
    
df['Campaigns Index'] = df['Campaign Status'].apply(check_len)


# Now, we will find out the Campaigns Index of our leads, who have been interacting with our CRM for at least two years.

long = df['Days in CRM'] > 365*2
long_df = df[long].sort_values(by='Campaigns Index', ascending=False)


graph(long_df[['Days in CRM', 'Campaigns Index']], 'Leads that have been in CRM >2 year and their Campaigns Index')


# The higher the Campaigns Index is, the more email campaigns have been sent to the leads. However it is no indication of their reactions to the company's email campaigns.

# We will also find out when exactly these leads were added to the CRM, and the relationship of the date that they were added and the Campaigns Index.

sns.relplot(x="Created Month", y="Campaigns Index", data=long_df.sort_values(by="Created Month"), aspect=3, size=2)
plt.xticks(rotation=45)
plt.title('Campaigns Index of Leads (been in CRM > 2 year) - by Year/Month that Leads are added to CRM')
plt.xlabel('Year/Month added to the CRM')

