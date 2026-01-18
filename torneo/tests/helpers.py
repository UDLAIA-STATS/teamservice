import json

def parse_response(response):
    """Helper function to parse JSON response data."""
    return json.loads(response.content.decode('utf-8'))
