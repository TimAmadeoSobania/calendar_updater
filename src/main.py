from datetime import datetime
import time

running = True
current_hour = datetime.now().hour -1

while running:
    try:
        
        if datetime.now().hour == current_hour:
            time.sleep(60)
        else:
            current_hour = datetime.now().hour

            # Run the update_calendar.py script
            exec(open("src/update_calendar.py").read())


    except KeyboardInterrupt:
        print('Program stopped')
        running = False
    except Exception as e:
        with open('error.txt', 'a') as file:
            file.write(f"{datetime.now()} | error: {str(e)}")
        print('An unexpected error occurred:', str(e))
        running = False
