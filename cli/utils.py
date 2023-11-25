def format_response(response):
    if response.status_code == 200:
        print("Success:")
        print(response.json())
    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def handle_error(e):
    print(f"An error occurred: {e}")
