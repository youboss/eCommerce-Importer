# eCommerce Product Importer & Salesforce Integration

A scalable Python web application that imports products from eCommerce websites (Amazon, Flipkart, Meesho) and allows creating records directly in Salesforce.

## Features
- Dynamic product scraping using `Playwright` and `BeautifulSoup`.
- Automatic platform detection.
- Pagination handling for retrieving multiple pages of product listings.
- Detailed product scraping on demand.
- Direct integration with the Salesforce REST API to create `Product2` records.
- Environment variables-based configuration.
- FastAPI backend with simple Bootstrap 5 frontend.

## Installation

1. **Clone or Extract the Repository**
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Playwright Browsers**
   ```bash
   playwright install chromium
   ```

## Configuration

1. **Set up `.env` File**
   Open the `.env` file in the root directory and update your Salesforce credentials:

   ```env
   SALESFORCE_USERNAME=your_username
   SALESFORCE_PASSWORD=your_password
   SALESFORCE_SECURITY_TOKEN=your_token
   SALESFORCE_CLIENT_ID=your_client_id
   SALESFORCE_CLIENT_SECRET=your_client_secret
   SALESFORCE_INSTANCE_URL=https://login.salesforce.com
   ```

2. **Salesforce Custom Fields**
   Ensure the following custom fields are created on the `Product2` object in your Salesforce org:
   - `Product_URL__c` (URL or Text)
   - `Image_URL__c` (URL or Text)
   - `External_Source__c` (Text)

## Running the Application

1. **Start the FastAPI Server**
   ```bash
   uvicorn app:app --reload
   ```

2. **Access the Application**
   Open your browser and navigate to `http://localhost:8000/`.

## Testing the Application

1. Go to `http://localhost:8000/`.
2. Paste an eCommerce category URL (e.g., `https://www.amazon.in/s?rh=n%3A1375425031%2Cp_123%3A46655`).
3. Click "Fetch Products". Wait for the scraper to traverse pages and display the grid.
4. Click "View Details" on any product to dynamically fetch its full details (Description, SKU, etc.).
5. Click "Save to Salesforce" to push the product data via the REST API to your Salesforce org.

## Adding New Scrapers

1. Create a `<platform>_scraper.py` file in `scrapers/`.
2. Inherit from `BaseScraper` and implement `get_products` and `get_product_details`.
3. Update `ScraperFactory` in `scrapers/factory.py` to route URLs to the newly created scraper.
