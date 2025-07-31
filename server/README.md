# Blip Server

## Overview

This project provides the backend server for the Blip application, offering functionalities for managing clusters, groups, users, sparks, and routines. It includes API endpoints, background services, and utility functions to support the application's features.

## Functionality

-   **User Management:** Create, update, and manage user accounts.
-   **Cluster Management:** Organize users into clusters (e.g., colleges, workplaces).
-   **Group Management:** Create and manage groups within clusters.
-   **Spark Scheduling:** Schedule and manage sparks (events or activities).
-   **Routine Management:** Define and manage recurring routines or tasks.
-   **Calendar Integration:** Integrates with calendar services to manage and display events.

## API Endpoints

The API endpoints are located in the `api` directory. Key endpoints include:

-   `/api/v1/users`: User management endpoints.
-   `/api/v1/clusters`: Cluster management endpoints.
-   `/api/v1/groups`: Group management endpoints.
-   `/api/v1/sparks`: Spark scheduling endpoints.
-   `/api/v1/routines`: Routine management endpoints.

See the `api/v1/routes.py` and `api/routes.py` files for detailed route definitions.

## Services

The `services` directory contains background services that provide additional functionality:

-   `calendar.py`: Manages calendar integration and event handling.
-   `match.py`: Implements matching algorithms.

## Utilities

The `utils` directory provides utility functions and helper classes:

-   `auth.py`: Handles authentication and authorization.

## Models

The `models` directory defines the data models used throughout the application:

-   `user.py`: Defines the User model.
-   `cluster.py`: Defines the Cluster model.
-   `group.py`: Defines the Group model.
-   `spark.py`: Defines the Spark model.
-   `routine.py`: Defines the Routine model.

## Configuration

The `config` directory contains configuration files for the application:

-   `database.py`: Configures the database connection.

