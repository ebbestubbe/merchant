import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():

    def get_requirements(df_in):
        reqs = pd.DataFrame(df_in['requires'].values.tolist(), index=df_in.index)
        return reqs

    with open('items.json') as json_file:
        data = json.load(json_file)
    categories = data.keys()

    dfs_all_items = []
    dfs_craftable = []
    for c in categories:
        df = pd.DataFrame.from_dict(
            data=data[c],
            orient="index")

        df.index.name = "name"
        df['category'] = c
        dfs_all_items.append(df)
        if("requires" in df.columns):
            dfs_craftable.append(df)
    all_items = pd.concat(dfs_all_items)
    craftables = pd.concat(dfs_craftable)

    requires = get_requirements(craftables)
    print(all_items)
    print(craftables)
    print(requires)

    requires[]


if __name__ == "__main__":
    main()
