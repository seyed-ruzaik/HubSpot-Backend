import requests
from flask import Flask, jsonify

app = Flask(__name__)

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
        # Return None if the request failed
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
        # Return None if the request failed
        return None


@app.route('/emails', methods=['GET'])
def get_emails():
    """
    Endpoint to fetch marketing emails and return them as JSON.
    """
    emails = fetch_emails()
    if emails:
        email_data = []
        if 'objects' in emails:
            for email in emails['objects']:
                email_info = {
                    "Email ID": email['id'],
                    "Subject": email['name'],
                    "Sender": email['author']
                }
                email_data.append(email_info)
        return jsonify(email_data)
    else:
        return jsonify({"error": "Error fetching emails"}), 500


@app.route('/tickets', methods=['GET'])
def get_tickets():
    """
    Endpoint to fetch tickets and return them as JSON.
    """
    tickets = fetch_tickets()
    if tickets:
        ticket_data = []
        if 'results' in tickets:
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
        return jsonify(ticket_data)
    else:
        return jsonify({"error": "Error fetching tickets"}), 500


if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
