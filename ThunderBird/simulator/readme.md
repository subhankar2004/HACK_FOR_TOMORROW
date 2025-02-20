# Satellite Simulator

## Overview

The Satellite Simulator is a Go-based application that simulates a constellation of satellites in low Earth orbit (LEO). It calculates and updates the positions of the satellites based on their orbital parameters and provides telemetry data via an HTTP endpoint.

## Features

- Simulates multiple satellites with varying orbital parameters.
- Calculates the 3D position of each satellite.
- Generates quantum keys for secure communication.
- Provides real-time telemetry data through an HTTP server.

## Requirements

- Go 1.16 or higher

## Build the Application

1. Go to simulator directory:

    ```sh
    Go to directory of simulator cd simulator .
    ```

2. Build the application:

    ```sh
    go run satelite.go
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
```` ▋