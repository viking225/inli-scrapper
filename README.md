# Inli Rental Scraper

This project is an AI-powered web scraper that extracts rental listings from the Inli website (https://www.inli.fr). It uses the browser-use library to automate browser interactions and scrape rental data, which is then saved to JSON files for further processing.

Funly enough i could i have done it with playwright but i just wanted to test browser-use and see how it works.
Also it's my first python script.

## Target Use Case

This scraper is designed to be integrated into an n8n pipeline for automated rental data collection and processing workflows.

## Installation

1. Clone or download this repository to your local machine.

2. Ensure you have Python 3.11 or higher installed.

3. Ensure you have uv installed

4. Install the required dependencies:
   ```bash
   uv sync
   ```

5. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your Google API key for the ChatGoogle LLM:
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```
   - Add the url you want to target
    ```
    INLI_URL=the_inli_url_w_query_params
    ```

## Usage

Run the application using the following command:

```bash
docker-compose up -d
```

The script will:
1. Open the Inli website with the specified search parameters
2. Scrape all available rental listings
3. Compare with previously scraped data to identify new listings
4. Extract detailed information from new listings
5. Save the data to `inli_results/new.json`
6. Update the database in `inli_results/database.json`

## Requirements

- Docker
- Google API key for Gemini LLM
- Internet connection for web scraping

## Dependencies

Key dependencies include:
- browser-use: For automated browser control
- python-dotenv: For environment variable management
- google-genai: For LLM integration

See `requirements.txt` for the complete list of dependencies.
