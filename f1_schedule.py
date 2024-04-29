import aiohttp
import xml.etree.ElementTree as ET

# Async function to fetch current F1 schedule data from the Ergast API
async def fetch_f1_schedule():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://ergast.com/api/f1/current') as response:
            if response.status == 200:
                return await response.text()  # You can parse the XML here if needed
            else:
                return "Failed to retrieve F1 schedule."

def parse_f1_schedule(xml_data):
    # Parse the XML data
    root = ET.fromstring(xml_data)
    
    # Namespace map from the XML data
    ns = {'mrd': 'http://ergast.com/mrd/1.5'}
    
    # Find all Race elements in the XML
    races = root.findall('.//mrd:Race', ns)
    
    # List to hold race information
    schedule = []

    # Iterate through each Race element and extract data
    for race in races:
        race_name = race.find('mrd:RaceName', ns).text
        circuit_name = race.find('mrd:Circuit/mrd:CircuitName', ns).text
        locality = race.find('mrd:Circuit/mrd:Location/mrd:Locality', ns).text
        country = race.find('mrd:Circuit/mrd:Location/mrd:Country', ns).text
        date = race.find('mrd:Date', ns).text
        time = race.find('mrd:Time', ns).text

        # Gather practice and qualifying times
        practices = []
        for session_tag in ['FirstPractice', 'SecondPractice', 'ThirdPractice']:
            session = race.find(f'mrd:{session_tag}', ns)
            if session is not None:
                session_date = session.find('mrd:Date', ns).text
                session_time = session.find('mrd:Time', ns).text
                practices.append(f"{session_tag.replace('Practice', ' Practice: ')}{session_date} at {session_time} UTC")

        qualifying = race.find('mrd:Qualifying', ns)
        if qualifying is not None:
            qualifying_date = qualifying.find('mrd:Date', ns).text
            qualifying_time = qualifying.find('mrd:Time', ns).text
            qualifying_str = f"Qualifying: {qualifying_date} at {qualifying_time} UTC"
        else:
            qualifying_str = "Qualifying details not available."

        # Create a dictionary of the race details
        race_details = {
            'race_name': race_name,
            'circuit': circuit_name,
            'locality': locality,
            'country': country,
            'date': date,
            'time': time + " UTC",
            'practices': "\n".join(practices),
            'qualifying': qualifying_str
        }

        # Add the dictionary to the schedule list
        schedule.append(race_details)

    return schedule

# This function formats the schedule into a readable format for Discord
def format_schedule_for_discord(schedule):
    race = schedule[0]  # Only take the first race from the schedule （FOR NOW)
    message = (
        f"**{race['race_name']}**\n"
        f"Location: {race['circuit']} in {race['locality']}, {race['country']}\n"
        f"Race Date and Time: {race['date']} at {race['time']}\n"
        f"{race['practices']}\n"
        f"{race['qualifying']}\n"
    )
    return message