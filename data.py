import pandas as pd
import numpy as np
import datapackage as dp

url = "https://pkgstore.datahub.io/JohnSnowLabs/iso-4217-currency-codes/2/datapackage.json"

package = dp.Package(url)

resources = package.resources

for resource in resources:
    if resource.tabular:
        data = pd.read_csv(resource.descriptor['path'], na_filter=False)
        # print(data)
        # resource_list.append(data['Entity'])
        # resource_list.append(data['Currency'])
        # resource_list.append(data['Alphabetic_Code'])


ent_list = list(data['Entity'])
cur_list = list(data['Currency'])
ac_list = list(data['Alphabetic_Code'])

ent_cur_list = list(zip(ent_list, cur_list))

new_entcur_list = (list(i) for i in zip(ent_list, cur_list))

final_list = map(' '.join, ent_cur_list)

# print(ent_list)
# print(cur_list)
# print(ac_list)

# print(ent_cur_list)
# print(list(final_list))

final_dict = dict(zip(final_list, ac_list))

# print(final_dict)


# print(resource_list)
# print(data)
# print(data['Entity'])

# for row in data:
# resource_list.append(row)

# for row in data:
# resource_list.append(row.T.to_dict('records'))
# print(row)

# for rows in data:
# for row in rows:
# resource_list.append(row['Entity'])
# resource_list.append(row('Currency'))
# resource_list.append(row('Alpabetic_Code'))

#list = [[data['Entity', 'Currency', 'Alphabetic_Code']] for row in data]
#df_specific = data[['Entity', 'Currency', 'Alphabetic_Code']]

# for rows in df_specific:
# resource_list.append(row)

# print(resource_list)
