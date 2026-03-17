# Laboratory 07

# Building a REST API

## Laboratory Theme
Introduction to REST APIs and Microservice Communication

---

# 1. Objective

In this laboratory you will build your **first REST API** using Python.

The goal is to understand how applications communicate using **HTTP requests** and **JSON data**.

By the end of this lab you will:

• create a simple API service
• implement several API endpoints
• send and receive JSON data
• test your API using a browser

---

# 2. Scenario

You are developing a small **Smart Building system**.

The building contains connected devices such as:

• coffee machines
• refrigerators
• smart lamps
• thermostats

Other software systems need to communicate with your platform to:

• see all devices
• add new devices
• retrieve a specific device
• remove devices

To support this communication you will implement a **Device Management API**.

---

# 3. What You Will Build

During this lab you will implement a REST API with the following endpoints:

```
GET /devices
POST /devices
GET /devices/{id}
DELETE /devices/{id}
```

Later in the lab you will extend the API with additional features.

---

# 4. Laboratory Tasks

In this lab you will:

1. Create a Python project
2. Install the FastAPI framework
3. Build a REST API service
4. Test the API using the automatic documentation

---

# 5. Project Setup

Create a new project directory:

```
lab07_device_api
```

Move into the directory:

```
cd lab07_device_api
```

Create the application file:

```
main.py
```

---

# 7. Installing Required Libraries

Install the required Python packages:

```
pip install fastapi uvicorn
```

FastAPI will be used to implement the REST API.

Uvicorn will run the API server.

---

# 8. Creating the First API Service

Open **main.py** and implement the following code:

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Smart Building Device API"}
```

Run the server:

```
uvicorn main:app --reload
```

Open the browser and navigate to:

```
http://127.0.0.1:8000
```

You should see a JSON message returned by the API.

---

# 9. Interactive API Documentation

FastAPI automatically generates an interactive API interface.

Open the following page:

```
http://127.0.0.1:8000/docs
```

This interface allows you to:

• explore API endpoints
• send HTTP requests
• inspect API responses

This interface is commonly used by developers to test APIs.

---

# 10. Data Model

For simplicity the devices will be stored in an **in‑memory list**.

Add the following structure to your code:

```
devices = []
```

Each device should contain the following attributes:

• id
• name
• energy_usage
• status
• location

Example device:

```
{
 "id": 1,
 "name": "coffee_machine",
 "energy_usage": 120,
 "status": "active",
 "location": "kitchen"
}
```

---

# 11. Task 1 — Retrieve All Devices

Create an endpoint that returns all registered devices.

Endpoint:

```
GET /devices
```

Expected response:

A list containing all devices.

---

# 12. Task 2 — Register a New Device

Create an endpoint that allows new devices to be added.

Endpoint:

```
POST /devices
```

Example request body:

```
{
 "name": "smart_lamp",
 "energy_usage": 40,
 "status": "active",
 "location": "office"
}
```

The API should automatically assign an ID to the new device.

---

# 13. Task 3 — Retrieve a Device by ID

Create an endpoint that returns a specific device.

Endpoint:

```
GET /devices/{device_id}
```

Example request:

```
GET /devices/1
```

If the device exists, return its information.

If the device does not exist, return an error message.

---

# 14. Task 4 — Delete a Device

Create an endpoint that removes a device.

Endpoint:

```
DELETE /devices/{device_id}
```

After deletion the device should no longer appear in the list.

---

# 15. Task 5 — Filter Devices by Status

Extend the API by allowing filtering using query parameters.

Endpoint:

```
GET /devices?status=active
```

The API should return only devices with the specified status.

---

# 16. Task 6 — Energy Consumption Statistics

Create a small analytics endpoint.

Endpoint:

```
GET /energy/total
```

This endpoint should calculate the **total energy usage** of all registered devices.

Example response:

```
{
 "total_energy_usage": 475
}
```

---

# 17. API Testing

Use the API interface to test the following operations:

1. Add several devices
2. Retrieve all devices
3. Retrieve a specific device
4. Delete a device
5. Filter active devices
6. Check total energy usage

Observe the JSON responses returned by the server.

---

# 18. Bonus Challenge (Optional)

Implement the following endpoint:

```
PUT /devices/{device_id}
```

This endpoint should update device information.

---

# 19. Deliverables

Your submission should contain the following project structure:

```
lab07_device_api

main.py
doc file
```

The doc file must include:

• project description
• API requests screenshots

---

# 20. Expected Learning Outcomes

After completing this laboratory you should understand:

• how APIs enable communication between software systems
• how REST APIs are structured
• how HTTP methods are used in practice
• how JSON is used for data exchange
• how to implement a simple service using Python

---

End of Laboratory 07

