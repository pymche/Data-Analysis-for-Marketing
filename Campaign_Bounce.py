#!/usr/bin/env python
# coding: utf-8

# Bounces from campaigns: match with record in CRM, add tag 'bounce'

import pandas as pd
import csv


# Importing data

bounce = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/Data/All_Campaign_Bounces.csv')
crm = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/Data/Leads_001.csv')
print(bounce.shape)
df = pd.merge(bounce, crm, how="inner", left_on="Contact Email", right_on="Email", sort=False)
df = df[['Record Id', 'Contact Email']]

print(df.shape)

# duplicateRowsDF = df[df.duplicated(['Record Id'])]
# print(duplicateRowsDF)

# write in CSV


with open('Old_bounces_from_campaigns.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    cols = ['Record Id', 'Contact Email']
    
    writer.writerow(['Record Id', 'Email', 'Tag'])

    for x in range(df.shape[0]):
        content = list(df[cols].iloc[x])
        content.append('Removed from Camps (bounce)')
        writer.writerow(content)
