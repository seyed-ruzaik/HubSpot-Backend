import tkinter as tk
from tkinter import ttk

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
    Fetch marketing emails from HubSpot using the Marketing Emails API.
    """
    response = requests.get(email_endpoint, headers=headers)
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
    Display the fetched email and ticket data in a user-friendly format:
    - Print the data to the console
    - Save the data to CSV files
    - Display the data in tabular format using pandas
    - Display the data in a GUI using tkinter
    """
    # Initialize lists to store email and ticket data
    email_data = []
    ticket_data = []

    # Print email data to the console
    print("\nEmails:")
    if emails and 'objects' in emails:
        for email in emails['objects']:
            email_info = {
                "Email ID": email['id'],
                "Subject": email['name'],
                "Sender": email['author']
            }
            email_data.append(email_info)
            print(f"Email ID: {email['id']}, Subject: {email['name']}, Sender: {email['author']}")
    else:
        print("No emails found or unable to fetch emails.")

    # Print ticket data to the console
    print("\nTickets:")
    if tickets and 'results' in tickets:
        for ticket in tickets['results']:
            properties = ticket['properties']
            all_status = ["New", "Waiting on contact", "Waiting on us", "Closed"]
            ticket_status_no = int(properties.get('hs_pipeline_stage'))
            ticket_status = all_status[ticket_status_no - 1]
            ticket_info = {
                "Ticket ID": ticket['id'],
                "Subject": properties.get('subject'),
                "Status": ticket_status
            }
            ticket_data.append(ticket_info)
            print(f"Ticket ID: {ticket['id']}, Subject: {properties.get('subject')}, Status: {ticket_status}")
    else:
        print("No tickets found or unable to fetch tickets.")

    # Convert email data to a pandas DataFrame
    emails_df = pd.DataFrame(email_data)
    # Save email data to a CSV file
    emails_df.to_csv('emails.csv', index=False)

    # Convert ticket data to a pandas DataFrame
    tickets_df = pd.DataFrame(ticket_data)
    # Save ticket data to a CSV file
    tickets_df.to_csv('tickets.csv', index=False)

    # Create GUI to display data in tables
    root = tk.Tk()
    root.title("HubSpot Data")

    # Create a frame for the email table
    email_frame = tk.Frame(root)
    email_frame.pack(pady=10)

    # Email table title
    email_label = tk.Label(email_frame, text="Emails", font=('Arial', 14))
    email_label.pack()

    # Create email table
    email_table = ttk.Treeview(email_frame, columns=("Email ID", "Subject", "Sender"), show='headings')
    email_table.heading("Email ID", text="Email ID")
    email_table.heading("Subject", text="Subject")
    email_table.heading("Sender", text="Sender")
    email_table.pack()

    # Insert email data into the table
    for email in email_data:
        email_table.insert('', 'end', values=(email["Email ID"], email["Subject"], email["Sender"]))

    # Create a frame for the ticket table
    ticket_frame = tk.Frame(root)
    ticket_frame.pack(pady=10)

    # Ticket table title
    ticket_label = tk.Label(ticket_frame, text="Tickets", font=('Arial', 14))
    ticket_label.pack()

    # Create ticket table
    ticket_table = ttk.Treeview(ticket_frame, columns=("Ticket ID", "Subject", "Status"), show='headings')
    ticket_table.heading("Ticket ID", text="Ticket ID")
    ticket_table.heading("Subject", text="Subject")
    ticket_table.heading("Status", text="Status")
    ticket_table.pack()

    # Insert ticket data into the table
    for ticket in ticket_data:
        ticket_table.insert('', 'end', values=(ticket["Ticket ID"], ticket["Subject"], ticket["Status"]))

    # Start the GUI main loop
    root.mainloop()


if __name__ == "__main__":
    # Fetch emails and tickets
    emails = fetch_emails()
    tickets = fetch_tickets()
    # Display fetched data
    display_data(emails, tickets)
