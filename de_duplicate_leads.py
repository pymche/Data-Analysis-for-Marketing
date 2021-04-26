#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import csv


leads_df = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/Data/Leads_001.csv')
contacts_df = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/Data/Contacts_001.csv')
accounts_df = pd.read_csv('/Users/melaniecheung/Desktop/Coding_Projects/Rightcheck/Data/Accounts_001.csv')


leads_df.head(3)


contacts_df.shape


accounts_df.shape


emails = [email for email in contacts_df['Email']]
# print(len(emails))


accounts = [company for company in accounts_df['Account Name']]
accounts.append('Atlas Hotels')
# print(accounts)


filt = leads_df['Tag from Campaign'] == 'Removed from Camps'
filt2 = leads_df['Created By Id'] == 'zcrm_2095940000021810125'


target = leads_df[filt & filt2]


target['Company'].fillna('None', inplace = True)


leads_email = [email for email in target['Email']]
# print(len(leads_email))


with open('contacts.csv', 'w') as csv_file:
    
    csv_writer = csv.writer(csv_file)
    
    csv_writer.writerow(['Record Id', 'Email', 'Company', 'Tag'])
    for email in leads_email:
        company = target[target['Email']==email]['Company'].values[0]
        if email in emails or company in accounts:
            id = target[target['Email'] == email]['Record Id'].values[0]
            csv_writer.writerow([id, email, company, 'contact/account'])







