# Inli Rental Scraper

This project is an AI-powered web scraper that extracts rental listings from the Inli website (https://www.inli.fr). It uses the browser-use library to automate browser interactions and scrape rental data, which is then saved to JSON files for further processing.

Funly enough i could i have done it with playwright but i just wanted to test browser-use and see how it works.
Also it's my first python script.

## Target Use Case

This scraper is designed to be integrated into an n8n pipeline for automated rental data collection and processing workflows.

## Installation

1. Clone or download this repository to your local machine.

2. Ensure you have Python 3.11 or higher installed.

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your Google API key for the ChatGoogle LLM:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

## Usage

Run the scraper using the following command:

```bash
python agent.py
```

The script will:
1. Open the Inli website with the specified search parameters
2. Scrape all available rental listings
3. Compare with previously scraped data to identify new listings
4. Extract detailed information from new listings
5. Save the data to `inli_results/new.json`
6. Update the database in `inli_results/database.json`

## Output

- `inli_results/database.json`: Contains all previously scraped rental data
- `inli_results/new.json`: Contains only the newly scraped rental listings

Each rental entry includes:
- description: Full text description of the rental
- price: Numerical price in euros
- nbOfRooms: Number of rooms
- surface: Surface area in square meters
- imgUrl: URL of the main image (or empty string if none)
- address: Guessed address from page content or Google Maps
- reference: Rental reference number
- url: URL of the rental listing page

## n8n Integration

To use this scraper in an n8n pipeline:

1. Set up the scraper as a scheduled task or webhook endpoint
2. Configure n8n to trigger the scraper execution
3. Use n8n's file operations to read the generated JSON files
4. Process the rental data through your n8n workflow (e.g., send notifications, update databases, generate reports)

## Requirements

- Python 3.8+
- Google API key for Gemini LLM
- Internet connection for web scraping

## Dependencies

Key dependencies include:
- browser-use: For automated browser control
- python-dotenv: For environment variable management
- google-genai: For LLM integration

See `requirements.txt` for the complete list of dependencies.
