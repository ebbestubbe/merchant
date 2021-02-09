import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    def get_total_crafting_requirements(item_name):
        if(item_name not in craftables.index):
            return {
            "craft_cost": 0,
            "resources": {
                    item_name: 1
                }
            }
        else:
            item_craft_cost = craftables.loc[item_name]['craft_cost']
            total_cost = {
                "craft_cost": item_craft_cost,
                "resources": {

                }
            }
            items_needed = requires.loc[item_name].dropna()

            for item, amount in items_needed.iteritems():
                sub_cost = get_total_crafting_requirements(item)
                sub_craft_cost = sub_cost['craft_cost']
                sub_resources = sub_cost['resources']
                total_cost['craft_cost'] = (
                    total_cost['craft_cost']
                    + amount*sub_craft_cost
                )
                for r, i in sub_resources.items():
                    if r in total_cost['resources']:
                        total_cost['resources'][r] = total_cost['resources'][r] + amount*i
                    else:
                        total_cost['resources'][r] = amount*i


            return total_cost

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

    def get_sell_price_of_items(item_dict):
        # Takes list of item names and quantities, returns the sell price
        per_item_type = {}
        for item, amount in item_dict.items():
            per_item_type[item] = amount*all_items.loc[item]['sell_price']

        return {
            "per_item_type": per_item_type,
            "total": float(np.sum(list(per_item_type.values())))
            }
    def get_base_profit(item):
        requirements = get_total_crafting_requirements(item)
        craft_cost = requirements['craft_cost']
        resources = requirements['resources']
        price_of_items = get_sell_price_of_items(resources)
        opportunity_cost = price_of_items['total']
        profit = (
            all_items.loc[item]['sell_price']
            - (opportunity_cost + craft_cost)
        )
        return profit
    # print(get_total_crafting_requirements('darksteel_platemail'))
    # print(get_total_crafting_requirements('scorpion_platemail'))
    # print(get_total_crafting_requirements('lesser_potion'))
    # print(get_total_crafting_requirements('xp_boost'))
    # print(get_total_crafting_requirements('ashe_root'))

    print(get_base_profit('darksteel_sheet'))
    print(get_base_profit("darksteel_greaves"))
    print(get_base_profit("darksteel_platemail"))
    print(get_base_profit("scorpion_platemail"))
    print(get_base_profit("ashe_root"))
    print(get_total_crafting_requirements("ashe_root"))
    print(all_items)
    all_items['profit'] = all_items.apply(lambda x: get_base_profit(x.name), axis=1)
    print(all_items)
    print(get_total_crafting_requirements("scorpion_platemail"))

if __name__ == "__main__":
    main()
