# Powerplant Production Plan API

This project represents an advanced technical solution for the Unit Commitment optimization challenge. Its fundamental purpose is to calculate the optimal load each power plant must generate to meet a specific demand, minimizing operating costs while ensuring compliance with each unit's technical constraints.

## Project Description

The application is implemented as a REST API developed with **FastAPI** and **Python 3.13**, designed to process load data, fuel costs, and generation capacities. Regarding the core logic, a **Merit Order** algorithm has been implemented to prioritize energy sources based on their marginal cost. It is important to highlight that the system integrates the calculation of **CO2** emission rights (0.3 ton/MWh) for gas-fired plants, aligning the solution with current energy sector sustainability standards.

## Architecture and Technologies

In relation to the software design, a separation of concerns approach has been followed to maximize maintainability. Specifically, **FastAPI & Pydantic** handle the transport layer and strict data schema validation, while a framework-independent **Logic Solver** facilitates unit testing. Furthermore, a **Logging & Observability** system provides event tracking for execution monitoring and real-time error management. Ultimately, the project uses **Docker** for full containerization to ensure consistent deployment across any environment.

## Launch Instructions

### Option 1: Docker (Recommended)
To ensure portability, the project includes a `Dockerfile`. The API can be started by executing the following commands in the repository root:

1.  Build the image: `docker build -t powerplant-api .`
2.  Run the container: `docker run -p 8888:8888 powerplant-api`

### Option 2: Local Installation
If you prefer a native execution, using a virtual environment is recommended:

1.  Create and activate the environment: `python -m venv venv` and `.\venv\Scripts\activate` (Windows).
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Launch the API: `python -m app.main`.

In compliance with the test requirements, the application remains accessible on port **8888**.

## Dispatch Algorithm Details

Regarding internal operations, the algorithm dynamically manages minimum ($P_{min}$) and maximum ($P_{max}$) power constraints. In scenarios where adding a low-cost plant creates excess production due to its $P_{min}$, the system applies a retroactive adjustment to plants already dispatched. Therefore, this mechanism ensures that the total production sum matches the requested demand exactly, consistently maintaining an accuracy of **0.1 MW**.

## Validation and Usage

The API includes interactive documentation accessible at `http://localhost:8888/docs`. To validate the solution, the files located in `./example_payloads` have been used, confirming that the production plan generated for `payload3.json` fully aligns with the results expected by the engineering team.

Furthermore, specific test cases have been incorporated to verify the stability of the algorithm under technical constraints:
- payload_custom_limit_0.json & response_custom_limit_0.json: Validation of the early termination logic (break) when the demand is met exactly before processing more expensive units.
- payload_custom_limit_1.json & response_custom_limit_1.json: Verification of the backtracking/skip protocol. This test demonstrates how the API handles a "technical deadlock" by skipping a rigid plant ($P_{min}$ constraints) that cannot be adjusted, successfully fulfilling the load with the next available flexible unit.
---
*Developed for the Short-term Power as-a-Service team recruitment process.*