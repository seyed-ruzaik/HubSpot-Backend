import pandas as pd
import requests

# Authentication
access_token = "MY_TOKEN"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# HubSpot API endpoints
email_endpoint = "https://api.hubapi.com/marketing-emails/v1/emails/with-statistics"
tickets_endpoint = "https://api.hubapi.com/crm/v3/objects/tickets"


def fetch_emails():
    """
    Fetch sales emails from HubSpot using the Engagements API.
    """
    params = {
        "limit": 10,  # Adjust the limit as needed
        "engagements": "EMAIL"
    }
    response = requests.get(email_endpoint, headers=headers, params=params)
    if response.status_code == 200:
        # Parse the JSON response if the request was successful
        emails = response.json()
        return emails
    else:
        # Print the error message if the request failed
        print(f"Error fetching emails: {response.status_code} - {response.text}")
        return None


def fetch_tickets():
    """
    Fetch tickets from HubSpot using the CRM API.
    """
    response = requests.get(tickets_endpoint, headers=headers)
    if response.status_code == 200:
        # Parse the JSON response if the request was successful
        tickets = response.json()
        return tickets
    else:
        # Print the error message if the request failed
        print(f"Error fetching tickets: {response.status_code} - {response.text}")
        return None


def display_data(emails, tickets):
    """
    Display the fetched email and ticket data.
    - Print the data to the console.
    - Save the data to CSV files.
    - Display the data in tabular format.
    """
    email_data = []
    print("\nEmails:")
    if emails and 'results' in emails:
        # Iterate through the email results and print details
        for email in emails['results']:
            email_engagement = email['engagement']
            email_metadata = email['metadata']
            email_info = {
                "Email ID": email_engagement['id'],
                "Subject": email_metadata.get('subject'),
                "Status": email_engagement['status']
            }
            email_data.append(email_info)
            print(
                f"Email ID: {email_engagement['id']}, Subject: {email_metadata.get('subject')}, Status: {email_engagement['status']}")
    else:
        print("No emails found or unable to fetch emails.")

    ticket_data = []
    print("\nTickets:")
    if tickets and 'results' in tickets:
        # Iterate through the ticket results and print details
        for ticket in tickets['results']:
            properties = ticket['properties']
            ticket_info = {
                "Ticket ID": ticket['id'],
                "Subject": properties.get('subject'),
                "Status": properties.get('hs_pipeline_stage')
            }
            ticket_data.append(ticket_info)
            print(
                f"Ticket ID: {ticket['id']}, Subject: {properties.get('subject')}, Status: {properties.get('hs_pipeline_stage')}")
    else:
        print("No tickets found or unable to fetch tickets.")

    # Convert email data to DataFrame and save to CSV
    emails_df = pd.DataFrame(email_data)
    emails_df.to_csv('emails.csv', index=False)

    # Convert ticket data to DataFrame and save to CSV
    tickets_df = pd.DataFrame(ticket_data)
    tickets_df.to_csv('tickets.csv', index=False)

    # Print email data as table
    print("\nEmail Data:")
    print(emails_df.to_string(index=False))

    # Print ticket data as table
    print("\nTicket Data:")
    print(tickets_df.to_string(index=False))


if __name__ == "__main__":
    # Fetch emails and tickets
    emails = fetch_emails()
    tickets = fetch_tickets()
    # Display fetched data
    display_data(emails, tickets)
