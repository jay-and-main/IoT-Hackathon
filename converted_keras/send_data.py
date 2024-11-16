import time, random, thingspeak, requests, dotenv, os

dotenv.load_dotenv()

channel_id = os.getenv('CHANNEL_ID')
write_key = os.getenv('WRITE_KEY')

# Set up the Thingspeak channel
channel = thingspeak.Channel(id=channel_id, api_key=write_key)

# Coz he's the only authorized user rn
user = 'Jayant'

def measure_and_write(channel):
    try:
        dist_reading = random.uniform(20, 100)  # Simulate a sensor reading
        if dist_reading is not None:
            print("Sending sensor data ...")
            response = channel.update({'field1': round(dist_reading, 2), 'field2': user})
        else:
            print("No reading yet ...")
    except Exception as e:
        print("Connection Failed:", e)

def read(channel) :
    url = "https://api.thingspeak.com/channels/2748487/feeds.json?api_key=0WMO5LUU20GGMPG1&results=1"

    response = requests.get(url)
    data = response.json()

    # Access the latest feed entry
    if 'feeds' in data and len(data['feeds']) > 0:
        latest_entry = data['feeds'][0]
        distance = latest_entry['field1']
        user = latest_entry['field2']
        timestamp = latest_entry['created_at']
        print("Latest Entry:")
        print(f"{user} was {distance} cm close to obstacle on {timestamp}")   
    else:
        print("No data found.")
    
    print(data['channel']['updated_at'])

# Main loop to send data at intervals
while True:
    measure_and_write(channel)
    time.sleep(15)
# read(channel=channel_id)
