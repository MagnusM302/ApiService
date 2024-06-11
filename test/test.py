import requests
import logging

logging.basicConfig(level=logging.INFO)

def fetch_address_details_simple(address_id):
    logging.info(f"Fetching address details for ID: {address_id}")
    url = f"https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?id={address_id}"
    logging.info(f"Request URL: {url}")
    try:
        response = requests.get(url)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response headers: {response.headers}")
        logging.info(f"Response content: {response.content.decode('utf-8')}")
        response.raise_for_status()
        data = response.json()
        logging.info(f"Fetched address details: {data}")
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching address details: {e}")
        return None

def main():
    address_id = "0a3f509a-828f-32b8-e044-0003ba298018"
    address_details = fetch_address_details_simple(address_id)
    if address_details:
        logging.info(f"Address Details: {address_details}")
    else:
        logging.warning("No address details found.")

if __name__ == "__main__":
    main()
