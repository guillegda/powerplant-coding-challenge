# Changelog - Powerplant Production Plan API

All notable changes to this project will be documented in this file, following the principles of *Keep a Changelog* and semantic versioning.

## [1.0.0] - 2026-03-15

### Added
In this initial version, the core API infrastructure has been deployed using **FastAPI** under **Python 3.13**, ensuring optimal performance and native data validation through **Pydantic**. 

Regarding the business logic, the dispatch algorithm's core has been implemented within the `solver.py` module. This component is capable of calculating the merit order of power plants based on real marginal costs, including weather-dependent wind energy processing and **CO2** emission cost calculations.

In relation to project portability, an optimized **Dockerfile** for containerized deployments has been incorporated, allowing the application to run in an isolated environment independent of the host operating system. Furthermore, the necessary validation schemas have been included to ensure that API inputs and outputs strictly comply with the technical challenge specifications.

### Technical Features
* Implementation of adjustment logic for minimum power constraints ($P_{min}$).
* Support for multiple fuel types (Gas, Kerosene) and renewable sources.
* Integration of interactive documentation through **Swagger UI** at the `/docs` endpoint.
* Configuration of a professional **logging** system for request monitoring and error management.

### Changed
* The listening port has been established at **8888** as a mandatory requirement of the requested architecture.
* Therefore, the file structure has been organized following modular design patterns to facilitate the future scalability of the system.