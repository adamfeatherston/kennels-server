import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import response
from views import (
    get_all_animals,
    get_single_animal,
    create_animal,
    delete_animal,
    update_animal,
)
from views import (
    get_all_locations,
    get_single_location,
    create_location,
    delete_location,
    update_location,
)
from views import (
    get_all_customers,
    get_single_customer,
    create_customer,
    delete_customer,
    update_customer,
)
from views import (
    get_all_employees,
    get_single_employee,
    create_employee,
    delete_employee,
    update_employee,
)

from models import Animal
from models import Customer
from models import Employee
from models import Location
from urllib.parse import urlparse, parse_qs

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split("/")  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)  # This is a tuple

    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if "?" not in self.path:
            (resource, id) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}" 
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"              

        else:  # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get("email") and resource == "customers":
                response = get_customer_by_email(query["email"][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):

        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new entry(s)
        new_entry = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            # Initialize new animal
            new_entry = create_animal(post_body)

        # Add a new location to the list.
        if resource == "locations":
            # Initialize new location: both name and address properties must be present in POST dictionary/body to be posted.
            if "name" in post_body and "address" in post_body:
                self._set_headers(201)
                new_entry = create_location(post_body)
            else:
                self._set_headers(400)
                new_entry = {
                    "message": f'{"name is required" if "name" not in post_body else ""} {"address is required" if "address" not in post_body else ""}'
                }

        # Add a new employee to the list.
        if resource == "employees":
            # Initialize new location
            new_entry = create_employee(post_body)

        # Add a new customer to the list.
        if resource == "customers":
            # Initialize new location
            new_entry = create_customer(post_body)

        # Encode the new entry(s) and send in response
        self.wfile.write(json.dumps(new_entry).encode())

    def do_DELETE(self):

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            self._set_headers(204)
            delete_animal(id)

        # Delete a single customer from the list
        if resource == "customers":
            self._set_headers(405)
            response = {"message": f"Ruh, roh: This function is not supported, sorry!"}

        # Delete a single employee from the list
        if resource == "employees":
            self._set_headers(204)
            delete_employee(id)

        # Delete a single location from the list
        if resource == "locations":
            self._set_headers(204)
            delete_location(id)

        # Encode the new resource and send in response
        self.wfile.write(json.dumps(response).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(204)
        content_len = int(self.headers.get("content-length", 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Update dictionary from animals list
        if resource == "animals":
            update_animal(id, post_body)

        # Update dictionary from customers list
        if resource == "customers":
            update_customer(id, post_body)

        # Update dictionary from employees list
        if resource == "employees":
            update_employee(id, post_body)

        # Update dictionary from locations list
        if resource == "locations":
            update_location(id, post_body)

        # Encode the new resource and send in response
        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Accept"
        )
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ""
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
