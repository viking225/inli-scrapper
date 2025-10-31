from browser_use import Agent, Tools, Browser, ChatGoogle
from dotenv import load_dotenv
import asyncio
import json
import pathlib
import os
import shutil


load_dotenv()

browser = Browser(headless=True)


tools = Tools()
database_content = []

ExtractTask= """
### **AI Agent Task: Scrape rental listing**
#### **Objective:**
Scrape all listing available on the inli website [Inli website](https://www.inli.fr/locations/offres/clichy-92110_v:92110?price_min=&price_max=1739&area_min=51&area_max=&room_min=2&room_max=5&bedroom_min=1&bedroom_max=5).
 - -

 ### **Step 1: Open the Website**
1. Open the webpage https://www.inli.fr/locations/offres/clichy-92110_v:92110?price_min=&price_max=1739&area_min=51&area_max=&room_min=2&room_max=5&bedroom_min=1&bedroom_max=5 
    - ensure that this is the exact url is opened.
    - if the exact url is not opened, open the exact url and verify that all query parameters are present.
2. Wait for the page to load completely before proceeding.
3. Validate any cookie window.

### Step 2: Identify number of rentals
1. Identify the number of rentals available, Each listing is an <a> tag that contains the price and description of the rental.
2. Scroll and visit supplementary pages to identify other rentals.
3. Extract the href for each rentals.

### ** Step 3: Decide if there is new listing**
1. Compare the extracted href , with the url in previous data
2. Filter href that are already present in the previous data.
3. If no data present after filter you can stop execution and consider task done.

### ** Step 4: Extract rental datas**
1. From the filtered data, visit each rental by navigating to the extracted href
2. extract all the data you can. ensure that the data extracted has the same schema. use the example rental information.

### **Step 5:Summarize the Data**
1. Transform all the extracted data to json array following the example output. data should be ABSOLUTELY parsed in json format.
2. Save the valid array json to new.json file and share it with me.
3. Provide a summary of the new rental found with less than 10 words for each and one line by new rental.

### Example Rental information
Each rental is an item on the page, it contain information about the rental information is not strcutured and you should try to guess which is which
    'description' (the full text description of the rental), 
    'price' (the numerical value in euros, e.g., '1 444 € cc' should be 1444), 
    'nbOfRooms' (the number of rooms, e.g., '3 pièces' should be 3), 
    'surface' (the numerical value in m², e.g., '60 m²' should be 60), and 'imgUrl' (the URL of the main image associated with this listing, or an empty string if no image is found).
    'address' Guessed address of the rental, using information contained in the page, or information contained in the google map positionned at the bottom of the page. If not found leave empty  
    'reference', correspond to the value after "Référence logement" in each item
    'url', the href of each rental page visited

### Example Output format for new array
[
    {{"description": "Exclusivité Sans frais d'agence, direct bailleur inli", "price": 1532, nbOfRooms: 3, surface: 60.27, imgUrl: 'http://haha.com/img.png', address: '', reference: "FEFEVE44" }},
    {{"description": "Batiment C escalier 2", "price": 1534, nbOfRooms: 3, surface: 60, http://haha_escalier_2.com/img.png, address: '113 boulevard clichy', reference: "24534FRF" }}

]


### Previous Data
<<<
{0}
>>>
### **Important**
Only save the extracted data to new.json when you finish the extraction for all the listing. 
Before saving data, you should validate that its a valid json array
"""

def createFileSytem():
    SCRIPT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
    agent_dir = SCRIPT_DIR / 'inli_results'
    databaseFile = agent_dir / 'database.json'
    newJsonFile = agent_dir / 'new.json'

    (agent_dir / 'fs').mkdir(exist_ok=True, parents=True)

    if not os.path.exists(databaseFile):
        with databaseFile.open("w", encoding ="utf-8") as f:
            f.write('[]')

    if not os.path.exists(newJsonFile):
        with newJsonFile.open("w", encoding ="utf-8") as f:
            f.write('[]')

    print(f"Set {databaseFile} and {newJsonFile}")

    return agent_dir



def getDatabase(path: pathlib.Path) -> list:
    with open(f'{path}/database.json', 'r') as f:
        database_content = json.loads(f.read())

    return database_content

def save_database(path: pathlib.Path) -> any:
    
    newData = []
    
    with open(f'{path}/fs/browseruse_agent_data/new.json', 'r') as f:
        newData = json.loads(f.read())

    database_content.extend(newData)

    with open(f'{path}/database.json', 'w') as f:
        json.dump(database_content, f)
        


async def main():
    system_path = createFileSytem()
    agentFs = str(system_path / 'fs')

    database_content = getDatabase(system_path)
    llm = ChatGoogle(model="gemini-2.5-pro")
    oldData = json.dumps(database_content)
    agent = Agent(task=ExtractTask.format(oldData), llm=llm, browser=browser, max_history_items=20, file_system_path=agentFs)

    try: 
        await agent.run()
        save_database(system_path)
    except Exception as e:
        print(f"Some exception occured while parsing {str(e)}")
    finally :
        shutil.rmtree(agentFs)

if __name__ == "__main__":
    asyncio.run(main())
