import pandas as pd
import os

# input logs directory name here.
LOGS_DIR = "logs"

def main():
    print("SELECT:")
    print("free         → 1 ")
    print("docker stats → 2 ")
    select = int(input())
    if select == 1:
        calc_free_log()
    elif select == 2:
        calc_docker_stats_log()

def calc_docker_stats_log():
    logs = next(os.walk(LOGS_DIR))[2]
    logs = sorted(logs)
    for log in logs:
        
        print()
        print("###################################################")
        print(log)
        print("###################################################")
        print()

       
        print("======LOGS_OVERVIEW======")
        df = pd.read_table(LOGS_DIR+"/"+log, header=None, sep=" ")
        print(df)
        print()


        print("======USED_MEMORY_OVERVIEW======")
        used_memory = df.iloc[:,3].dropna().replace(["(.*)MiB","(.*)GiB"], r"\1", regex=True)
        total_memory = df.iloc[:,5].dropna().replace("(.*)GiB", r"\1", regex=True)
        percent_memory = df.iloc[:,8].dropna().replace("(.*)%", r"\1", regex=True).astype(float)
        details = pd.concat([used_memory,total_memory,percent_memory], axis=1)
        details.columns = ['used_memory','total_mamory','used_memory%']
        #details.astype("float64").loc[[details['used_memory'] > 32, 'used_memory']] = details['used_memory'] /1024
        print(details)


        print("======MEAN_USED_MEMORY======")
        print()
        print(details.mean())
        print()


        print("======MAX_USED_MEMORY======")
        print()
        print(details.max())
        print()
    


def calc_free_log():
    logs = next(os.walk(LOGS_DIR))[2]
    logs = sorted(logs)
    for log in logs:
        
        print()
        print("###################################################")
        print(log)
        print("###################################################")
        print()


        print("======LOGS_OVERVIEW======")
        df = pd.read_table(LOGS_DIR+"/"+log, header=None, sep=" ")
        print(df)
        print()


        print("======USED_MEMORY_OVERVIEW======")
        total_memory = df.loc[0,9]
        total_swapmemory = df.loc[0,16]
        used_memory = df.loc[:, [14,17]]
        used_memory.columns = ['main_available','swap_used']
        used_memory["main_used"] = total_memory - used_memory["main_available"]
        used_memory["swap_used"] = used_memory["swap_used"] - used_memory.loc[0, "swap_used"]
        print(used_memory)
        print()


        print("======MEAN_USED_MEMORY======")
        mean_used_memory = used_memory.mean(numeric_only=True)
        print(mean_used_memory)
        print()
        print("main(%)     " + str(mean_used_memory["main_used"]/total_memory*100) + "%")
        print("swap(%)     " + str(mean_used_memory["swap_used"]/total_swapmemory*100)+ "%")
        print()


        print("======MAX_USED_MEMORY======")
        max_used_memory = used_memory.max()
        print(max_used_memory)
        print()
        print("main(%)     " + str(max_used_memory["main_used"]/total_memory*100) + "%")
        print("swap(%)     " + str(max_used_memory["swap_used"]/total_swapmemory*100)+ "%")
        print()

if __name__ == "__main__":
    main()
