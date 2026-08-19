# midas-logistics
Multi-Agent logistics coordination and intelligent freight optimization system.
MIDAS
Multi-Agent Intelligent Logistics Coordination System

MIDAS is a logistics coordination platform designed to reduce empty/under-utilized truck capacity by intelligently matching available truck capacity with nearby freight requirements.

The system models trucks, warehouses, freight requests and logistics agents as interconnected entities. It uses a central backend, optimization services, simulation and a web-based dashboard to demonstrate intelligent freight coordination.

Current status: Project infrastructure and development environment are established. Core logistics functionality is under development.

1. Problem

A large number of logistics vehicles travel while carrying only a portion of their maximum capacity.

For example:

Truck A
Capacity: 100 boxes
Current load: 60 boxes
Available: 40 boxes

At the same time, another company may need:

Company B
Cargo: 30 boxes
Destination: Location X

Instead of sending another vehicle, MIDAS attempts to determine whether Truck A can efficiently transport the additional cargo.

The system considers factors such as:

Available truck capacity
Truck location
Cargo origin
Cargo destination
Distance
Route compatibility
Delivery requirements
Estimated additional cost
Operational constraints

The goal is to improve vehicle utilization while reducing unnecessary trips.

2. Core Concept

The simplified MIDAS workflow is:

                    Freight Request
                          │
                          ▼
                    MIDAS Backend
                          │
                          ▼
                 Find Suitable Trucks
                          │
                          ▼
                    Agent / Matcher
                          │
                          ▼
                     Optimizer
                          │
                          ▼
                  Best Assignment
                          │
                          ▼
                   Backend Update
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        Driver / Truck            Dashboard

For the MVP, the system will use simulated trucks and logistics events rather than requiring real trucks or physical hardware.

3. System Architecture
                         ┌──────────────────┐
                         │     Frontend     │
                         │  React + Vite    │
                         └────────┬─────────┘
                                  │
                                  │ HTTP / API
                                  ▼
                         ┌──────────────────┐
                         │     Backend      │
                         │     FastAPI      │
                         └────────┬─────────┘
                                  │
             ┌────────────────────┼────────────────────┐
             │                    │                    │
             ▼                    ▼                    ▼
       ┌───────────┐       ┌────────────┐       ┌─────────────┐
       │ Database  │       │  Services  │       │  Optimizer  │
       │ SQLite    │       │ Matching   │       │  OR-Tools   │
       └───────────┘       └────────────┘       └─────────────┘
                                  ▲
                                  │
                       ┌──────────┴──────────┐
                       │                     │
                       ▼                     ▼
                ┌─────────────┐       ┌─────────────┐
                │    Agents   │       │ Simulation  │
                │ Truck/Other │       │ Fake Trucks │
                └─────────────┘       └─────────────┘
4. Repository Structure
midas-logistics/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── .venv/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── eslint.config.js
│   └── vite.config.js
│
├── agents/
│   ├── truck_agent/
│   └── warehouse_agent/
│
├── optimizer/
│   ├── src/
│   └── tests/
│
├── simulation/
│   ├── trucks/
│   ├── warehouses/
│   └── events/
│
├── hardware/
│   └── esp32/
│
├── docs/
│
├── setup.ps1
├── .gitignore
└── README.md
5. Backend

Location:

backend/

The backend is the central coordination layer of MIDAS.

Technology:

Python
FastAPI
SQLAlchemy
SQLite
Pydantic
HTTPX
OR-Tools
Pytest
Ruff
Pyright

The backend will eventually manage:

Trucks
Warehouses
Companies
Cargo
Freight requests
Assignments
Routes
Agent communication
Optimization requests
System state
Backend API

The frontend and other components communicate with the backend through APIs.

For example:

GET    /api/trucks
POST   /api/trucks


GET    /api/warehouses
POST   /api/warehouses


GET    /api/requests
POST   /api/requests


POST   /api/requests/{id}/match


GET    /api/assignments

The exact API will be finalized as development progresses.

6. Backend Directory Structure
backend/app/main.py

Main FastAPI application.

Responsible for starting the backend and registering API routes.

backend/app/api/

Contains API endpoints.

Example:

api/
├── trucks.py
├── warehouses.py
├── requests.py
└── assignments.py

The API layer should primarily handle:

Request
   ↓
Validate input
   ↓
Call service
   ↓
Return response

Business logic should not be unnecessarily placed directly inside API route functions.

7. backend/app/models/

Contains database models.

Examples:

Truck
Warehouse
Company
CargoRequest
Assignment
Route

These models represent the persistent state of the logistics system.

8. backend/app/schemas/

Contains Pydantic schemas used for API input/output validation.

For example:

TruckCreate
TruckResponse
CargoRequestCreate
CargoRequestResponse
AssignmentResponse

Models represent database entities.

Schemas represent data moving through the API.

9. backend/app/services/

Contains the actual business logic.

Examples:

truck_service.py
matching_service.py
assignment_service.py
routing_service.py

For example:

Cargo Request
      ↓
Matching Service
      ↓
Candidate Trucks
      ↓
Feasibility Check
      ↓
Optimizer
      ↓
Best Truck
10. Agents

Location:

agents/

MIDAS follows a multi-agent architecture concept.

An agent represents the decision-making or operational logic associated with an entity.

The most important initial agent is the:

Truck Agent

A truck agent can represent:

Truck ID
Current location
Destination
Capacity
Current load
Available capacity
Current route
Availability

The agent can receive a freight opportunity and determine whether the truck should consider it.

Important MVP decision

The agent does not need to physically run inside every real truck.

For the hackathon:

                MIDAS Backend
                     │
                     ▼
              Simulated Agents
                     │
                     ▼
                Simulated Trucks

This allows us to demonstrate the architecture without requiring physical hardware.

11. Optimizer

Location:

optimizer/

The optimizer is responsible for finding good assignments and routes.

The project will use Google OR-Tools where appropriate.

Potential optimization factors include:

Distance
Available capacity
Route compatibility
Additional travel
Delivery deadline
Priority
Estimated cost

The initial MVP may use a simple deterministic matching algorithm before introducing more complex optimization.

Example:

Candidate Truck A
Distance = 5 km
Available Capacity = 40


Candidate Truck B
Distance = 30 km
Available Capacity = 70


Cargo Requirement = 30


                 ↓


           Truck A selected
12. Simulation

Location:

simulation/

The simulation represents the physical logistics network digitally.

Instead of requiring real trucks, it creates simulated entities.

Example:

Truck 001
Location: 30.7046, 76.7179
Capacity: 100
Current Load: 60


Truck 002
Location: 30.7200, 76.7300
Capacity: 80
Current Load: 20

The simulator can generate events such as:

Truck movement
Cargo request
Warehouse request
Truck availability
Route update
Assignment

The backend should treat simulated entities similarly to real entities.

This makes it possible to replace the simulator with real data in a future version.

13. Frontend

Location:

frontend/

Technology:

React
Vite
Axios
Leaflet
React-Leaflet
ESLint
Prettier

The frontend is the visual interface for the system.

Potential screens include:

Operations Dashboard
Active Trucks
Pending Cargo
Available Capacity
Active Assignments
System Status
Live Map

Displays:

🚚 Trucks
🏭 Warehouses
📦 Cargo locations
📍 Routes
Freight Request

Allows a user to create:

Origin
Destination
Cargo quantity
Priority
Deadline
Assignment View

Shows:

Cargo Request
      ↓
Selected Truck
      ↓
Additional Distance
      ↓
Estimated Cost
      ↓
Assignment Status
14. Hardware

Location:

hardware/

Hardware is currently a future/optional component.

Possible future architecture:

Backend
   ↓
Truck Agent
   ↓
Tablet
   ↓
Physical Truck / ESP32

The MVP should not depend on physical hardware.

The hardware folder exists so that hardware integration can be explored without changing the main architecture.

15. Database

The MVP will use SQLite.

Conceptually:

Company
   │
   ├── Trucks
   │
   └── Cargo Requests


Warehouse
   │
   └── Cargo


Truck
   │
   ├── Location
   ├── Capacity
   ├── Current Load
   └── Route


Cargo Request
   │
   ├── Origin
   ├── Destination
   ├── Quantity
   └── Priority

The database stores the current state of the logistics network.

16. Communication Between Components

The primary communication pattern is:

Frontend
    │
    │ HTTP
    ▼
FastAPI Backend
    │
    ├──────── Database
    │
    ├──────── Agents
    │
    ├──────── Optimizer
    │
    └──────── Simulation

The frontend should not directly access the database.

The frontend communicates through backend APIs.

17. Example MIDAS Workflow

Suppose:

Truck A
Capacity: 100 boxes
Current load: 60 boxes
Available: 40 boxes

Truck A is travelling from:

Warehouse A → Warehouse C

Another company creates:

Cargo Request
40 boxes
Warehouse B → Warehouse C

The system receives the request.

Step 1 — Request
Company B
    ↓
MIDAS API
Step 2 — Find candidate trucks

The backend searches for trucks that:

have enough capacity
AND
are operational
AND
are geographically relevant
AND
have compatible routes
Step 3 — Feasibility

The candidate is evaluated.

Truck A
Available capacity = 40
Required capacity = 40

Capacity requirement is satisfied.

Step 4 — Optimization

The optimizer evaluates the additional route cost.

Step 5 — Assignment

If the assignment is beneficial:

Cargo Request
      ↓
Truck A
Step 6 — Update

The backend updates:

Truck A
Available capacity
Route
Assignment
Step 7 — Dashboard

The frontend displays the updated situation.

18. Development Tools
Python

Backend and simulation/agent components.

FastAPI

Backend REST API.

SQLAlchemy

Database interaction.

SQLite

MVP database.

OR-Tools

Optimization.

React

Frontend.

Vite

Frontend development/build system.

Axios

Frontend → backend communication.

Leaflet

Map visualization.

ESLint

JavaScript/React linting.

Prettier

Frontend formatting.

Ruff

Python linting and formatting.

Pyright

Python type checking.

Pytest

Python testing.

Git + GitHub

Version control and collaboration.
