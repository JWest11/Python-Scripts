import sched, datetime, urllib3, time, json, os
http = urllib3.PoolManager()


def get_request(schedulerObject):
    
    request = http.request("GET", "ifconfig.co/json")

    requestDataJsonString = json.loads(request.data.decode("utf-8"))

    file = open("Output.txt", "a")
    file.close()
    file = open("Output.txt", "r")

    try:
        data = json.loads(file.read())
        data.append(requestDataJsonString)
        data = json.dumps(data)
    except:
        data = json.dumps([requestDataJsonString])
    file.close()

    file = open("Output.txt", "w")
    file.write(data)
    file.close()

    print(f"Get request performed at {datetime.datetime.now().isoformat()}")
    print(requestDataJsonString)
    if not schedulerObject.empty():
        show_queue(schedulerObject)
    else:
        print("Scheduler has no more tasks.")


def show_queue(schedulerObject):
    print("CurrentQueue:")
    for event in schedulerObject.queue:
        print(datetime.datetime.fromtimestamp(event.time).isoformat())


def app():
    print("")
    inputString = input('Plese enter times in quotation marks separated by commas.\nExample: 09:15:25,11:58:23,00:01:09\nTimes in the past will not be run, and invalid inputs are ignored (ie 06:00:00 will not be run if the current time is 07:00:00)\nalternatively type "file" to select a file with the times formatted in the same way\n')
    if inputString == "file":
        fileName = input("Input the file name including extension. Example: Input.txt\n")
        try:
            file = open(fileName, "r")
            inputTimeList = file.read().split(',')
        except:
            print("file not found")
            app()
    else:
        inputTimeList = inputString.split(',')

    scheduler = sched.scheduler(time.time, time.sleep)

    for timeString in inputTimeList:

        try:
            timeComponent = datetime.time.fromisoformat(timeString)
        except:
            continue

        dt = datetime.datetime.combine(datetime.date.today(), timeComponent)
        if dt.timestamp() < time.time():
            continue
        scheduler.enterabs(time=dt.timestamp(), action=get_request, priority=0, argument=[scheduler])

    if not scheduler.empty():
        print("Scheduler is running, get requests will be performed at the times specified. Keep this window open.")
        show_queue(scheduler)
        scheduler.run()
    else:
        print("No valid tasks, check input values.")
        app()

os.system("cls" if os.name == "nt" else "clear")
app()