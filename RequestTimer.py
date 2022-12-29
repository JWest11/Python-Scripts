import sched, datetime, urllib3, time, json
http = urllib3.PoolManager()

inputTimeStrings = ["09:15:25","11:58:23", "00:01:09", "16:01:00", "16:38:00", "12983:djkahfls:jklahkfdjg"]

def get_request(schedulerObject):
    
    request = http.request("GET", "ifconfig.co/json")
    print(f"Get request performed at {datetime.datetime.now().isoformat()}")
    print(request.data)
    if not schedulerObject.empty():
        show_queue(schedulerObject)
    else:
        print("Scheduler has no more tasks.")

def show_queue(schedulerObject):
    print("CurrentQueue:")
    for event in schedulerObject.queue:
        print(datetime.datetime.fromtimestamp(event.time).isoformat())

    
request = http.request("GET", "ifconfig.co/json")
requestDataJsonString = json.loads(request.data.decode("utf-8"))

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

scheduler = sched.scheduler(time.time, time.sleep)

for timeString in inputTimeStrings:

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

