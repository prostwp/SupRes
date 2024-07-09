from datetime import datetime, timedelta
from sup_res_keys import keys
with open("news.txt", "r") as content:

    try:
        with open("news.txt", 'r') as file:
            content = file.readlines()
        if content and len(content) == 2:
            file_time = datetime.strptime(content[1], '%H:%M').time()
            current_time = datetime.now()
            threshold_time = datetime.combine(current_time.date(), file_time)
            time_difference = threshold_time - current_time
            # toggle_bold()
            print(keys["fundamental_factors"][0])
            # toggle_bold()
            if time_difference > timedelta(hours=1):
                print(content[0])
            elif timedelta(0) <= time_difference <= timedelta(hours=1):
                print(content[0].replace("hour", "minute"))
            else:
                with open("news.txt", 'w') as file:
                    pass
        else:
            print(keys["no_news"][0])
    except FileNotFoundError:
        print("File not found.")