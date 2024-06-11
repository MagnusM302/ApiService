import requests
import logging

# Define base URLs for each API endpoint
ADDRESS_AUTOCOMPLETE_URL = "https://api.dataforsyningen.dk/autocomplete"
ADDRESS_DETAILS_URL = "https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse"
BUILDING_DETAILS_URL = "https://services.datafordeler.dk/BBR/BBRPublic/1/rest/bygning"

logging.basicConfig(level=logging.INFO)

def fetch_address_data(address_query):
    logging.info(f"Fetching address for: {address_query}")
    params = {'q': address_query, 'type': 'adresse'}
    try:
        response = requests.get(ADDRESS_AUTOCOMPLETE_URL, params=params)
        logging.info(f"Address autocomplete response status: {response.status_code}")
        logging.debug(f"Address autocomplete response headers: {response.headers}")
        logging.debug(f"Address autocomplete response content: {response.content.decode('utf-8')}")
        response.raise_for_status()
        data = response.json()
        logging.info(f"Fetched address data: {data}")
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching address data: {e}")
        return None

def fetch_address_details(address_id):
    logging.info(f"Fetching address details for ID: {address_id}")
    url = f"{ADDRESS_DETAILS_URL}?id={address_id}"
    logging.info(f"Address details URL: {url}")
    try:
        response = requests.get(url)
        logging.info(f"Address details response status: {response.status_code}")
        logging.debug(f"Address details response headers: {response.headers}")
        logging.debug(f"Address details response content: {response.content.decode('utf-8')}")
        response.raise_for_status()
        data = response.json()
        logging.info(f"Fetched address details: {data}")
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching address details: {e}")
        return None

def fetch_building_details(building_id, username, password):
    logging.info(f"Fetching building details for ID: {building_id}")
    params = {'id': building_id, 'username': username, 'password': password}
    try:
        response = requests.get(BUILDING_DETAILS_URL, params=params)
        logging.info(f"Building details response status: {response.status_code}")
        logging.debug(f"Building details response headers: {response.headers}")
        logging.debug(f"Building details response content: {response.content.decode('utf-8')}")
        response.raise_for_status()
        data = response.json()
        logging.info(f"Fetched building details: {data}")
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching building details: {e}")
        return None

def main():
    address_query = "Kærvej 7, 9800"
    logging.info(f"Starting main process for address query: {address_query}")
    address_data = fetch_address_data(address_query)

    if address_data:
        if isinstance(address_data, list) and address_data:
            address_info = address_data[0].get('data', {})
            address_id = address_info.get('id')
            logging.info(f"Address ID: {address_id}")
            if address_id:
                address_details = fetch_address_details(address_id)
                if address_details:
                    if isinstance(address_details, list) and address_details:
                        address_detail_info = address_details[0].get('husnummer', {})
                        building_id = address_detail_info.get('adgangTilBygning')
                        logging.info(f"Building ID: {building_id}")

                        if building_id:
                            username = "XJCGPDGQSM"
                            password = "$Skole1234"
                            building_details = fetch_building_details(building_id, username, password)

                            if building_details:
                                logging.info(f"Building Details: {building_details}")
                            else:
                                logging.warning("No building details found.")
                        else:
                            logging.warning("No 'adgangTilBygning' found in husnummer.")
                    else:
                        logging.warning("Address details structure is not as expected.")
                else:
                    logging.warning("No address details found.")
            else:
                logging.warning("No valid address ID found in address data.")
        else:
            logging.warning("Address data structure is not as expected.")
    else:
        logging.warning("No address data found.")

if __name__ == '__main__':
    main()
