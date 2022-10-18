from .location_requests import get_single_location
from .customer_requests import get_single_customer
import sqlite3
import json
from models import Animal
from models import Location
from models import Customer


def get_all_animals():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address,
	        c.name customer_name,
	        c.address customer_address,
	        c.email customer_email
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        JOIN Customer c 
	        ON c.id = a.customer_id
        """
        )

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(
                row["id"],
                row["name"],
                row["status"],
                row["breed"],
                row["customer_id"],
                row["location_id"],
            )

            # Create a Location instance from the current row
            location = Location(
                row["id"], row["location_name"], row["location_address"]
            )

            customer = Customer(
                row["id"],
                row["customer_name"],
                row["customer_address"],
                row["customer_email"],
            )

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return json.dumps(animals)


# Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
        FROM Animal a
        WHERE a.id = ?
        """,
            (id,),
            # This will be done in chapter 7 of book 2.
            #     """
            # SELECT
            #     l.name,
            # FROM location l
            # WHERE l.id = ?
            # """,
            #     (id,),
            #     """
            # SELECT
            #     c.name,
            # FROM customer c
            # WHERE c.id = ?
            # """,
            #     (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(
            data["id"],
            data["name"],
            data["status"],
            data["breed"],
            data["customer_id"],
            data["location_id"],
            # This will be done in chapter 7 of book 2.
            # matching_location = get_single_location(animal["location_id"])
            # animal["location"] = matching_location
            # matching_customer = get_single_customer(animal["customer_id"])
            # animal["customer"] = matching_customer
            # data.pop("location_Id", None)
            # data.pop("customer_Id", None)
        )

        return animal.__dict__


def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Animal
            ( name, status, breed, customer_id, location_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """,
            (
                new_animal["name"],
                new_animal["status"],
                new_animal["breed"],
                new_animal["customer_id"],
                new_animal["location_id"],
            )
        )

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal["id"] = id

    return new_animal


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Animal
        WHERE id = ?
        """,
            (id,),
        )


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Animal
            SET
                name = ?,
                status = ?,
                breed = ?,
                customer_id = ?,
                location_id = ?
        WHERE id = ?
        """,
            (
                new_animal["name"],
                new_animal["status"],
                new_animal["breed"],
                new_animal["customerId"],
                new_animal["locationId"],
                id,
            ),
        )

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


def get_animals_by_location(location):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
        FROM Animal a
        WHERE a.location_id = ?
        """,
            (location,),
        )

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row["id"],
                row["name"],
                row["status"],
                row["breed"],
                row["customer_id"],
                row["location_id"],
            )
            animals.append(animal.__dict__)

    return animals


def get_animals_by_status(status):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            a.id,
            a.name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id
        FROM Animal a
        WHERE status = ?
        """,
            (status,),
        )

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row["id"],
                row["name"],
                row["status"],
                row["breed"],
                row["customer_id"],
                row["location_id"],
            )
            animals.append(animal.__dict__)

    return animals
