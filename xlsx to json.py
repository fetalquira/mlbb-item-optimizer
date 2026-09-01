import pandas as pd
import json

def xlsx_to_json(input,output):
    df = pd.read_excel("D:\Documents\Programming\Python\MLBB Item Optimizer\{i}.xlsx".format(i = input))

    json_data = df.to_dict()
    with open("D:\Documents\Programming\Python\MLBB Item Optimizer\{o}.json".format(o = output),"w",encoding="utf-8") as f:
        json.dump(json_data,f,indent=4,ensure_ascii=False)

xlsx_to_json('data','data')