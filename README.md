# HubSpot API Integration

This repository contains a Python script to fetch and display marketing emails and tickets from HubSpot using their API.

## Functionalities

- **Fetch Emails**: Retrieve marketing emails from HubSpot using the HubSpot API.
- **Fetch Tickets**: Retrieve tickets from HubSpot using the CRM API.
- **Display Data**:
  - Print the fetched email and ticket data to the console in a readable format.
  - Save the fetched email and ticket data to CSV files for easy inspection.
  - Display the data in tabular format using pandas for better visualization.

## How to Run

1. **Install the required libraries**:
    ```sh
    pip install requests pandas
    ```

2. **Update the access token**:
    - Open the `avantrio.py` file.
    - Replace the value of `access_token` with your HubSpot private app access token.

3. **Run the script**:
    ```sh
    python avantrio.py
    ```

## Code Explanation

The script performs the following steps:

1. **Authentication**:
    - Uses a private app access token for authentication to the HubSpot API.

2. **Fetch Data**:
    - **Fetch Emails**: Uses the `fetch_emails` function to retrieve marketing emails from the HubSpot API.
    - **Fetch Tickets**: Uses the `fetch_tickets` function to retrieve tickets from the HubSpot CRM API.

3. **Display Data**:
    - **Print to Console**: Prints the fetched email and ticket data to the console in a readable format.
    - **Save to CSV**: Saves the fetched email and ticket data to `emails.csv` and `tickets.csv` respectively.
    - **Display as Tables**: Uses pandas to display the data in a tabular format.

### Script Breakdown

- **fetch_emails**: 
    - Makes a GET request to the HubSpot API to fetch marketing emails.
    - Handles errors and returns the email data.

- **fetch_tickets**: 
    - Makes a GET request to the HubSpot CRM API to fetch tickets.
    - Handles errors and returns the ticket data.

- **display_data**: 
    - Parses and prints email and ticket data.
    - Converts data to pandas DataFrames.
    - Saves data to CSV files.
    - Prints data as tables.
    - Additionally a GUI using Tkinter to display the data.

## Author

[Seyed Ruzaik]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
