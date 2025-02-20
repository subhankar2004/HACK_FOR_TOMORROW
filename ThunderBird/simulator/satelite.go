// satellite_simulator.go
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"math"
	"math/rand"
	"net/http"
	"time"
)

// Position represents the 3D position of a satellite
type Position struct {
	X float64 `json:"x"`
	Y float64 `json:"y"`
	Z float64 `json:"z"`
}

// Satellite represents a satellite in the system
type Satellite struct {
	ID             string    `json:"id"`
	Name           string    `json:"name"`
	OrbitType      string    `json:"orbitType"`
	Altitude       float64   `json:"altitude"`
	Inclination    float64   `json:"inclination"`
	AscendingNode  float64   `json:"-"`
	InitialAnomaly float64   `json:"-"`
	LaunchTime     time.Time `json:"-"`
	Position       Position  `json:"position"`
	LastContact    time.Time `json:"lastContact"`
	QuantumKeyID   string    `json:"quantumKeyId"`
	KeyGeneration  time.Time `json:"keyGeneration"`
	Status         string    `json:"status"`
}

// SatelliteOrbit represents the orbital parameters
type SatelliteOrbit struct {
	Altitude      float64
	Inclination   float64
	AscendingNode float64
	Anomaly       float64
	LaunchTime    time.Time
}

// Constellation represents a group of satellites
type Constellation struct {
	Satellites []*Satellite
}

const (
	EarthRadius = 6371.0   // km
	GM          = 398600.0 // Earth's gravitational parameter (km³/s²)
)

// calculatePeriod calculates the orbital period using Kepler's third law
func calculatePeriod(altitude float64) float64 {
	semiMajorAxis := EarthRadius + altitude
	return 2 * math.Pi * math.Sqrt(math.Pow(semiMajorAxis, 3)/GM)
}

// getPosition calculates the current position based on orbital parameters
func getPosition(orbit SatelliteOrbit) Position {
	// Calculate time elapsed since launch
	timeElapsed := time.Since(orbit.LaunchTime).Seconds()

	// Calculate current anomaly based on time
	period := calculatePeriod(orbit.Altitude)
	currentAnomaly := orbit.Anomaly + (timeElapsed/period)*360.0
	angleRad := currentAnomaly * math.Pi / 180.0

	// Simplified orbital mechanics - circular orbit
	radius := EarthRadius + orbit.Altitude

	// Calculate position in orbital plane
	xOrbit := radius * math.Cos(angleRad)
	yOrbit := radius * math.Sin(angleRad)

	// Rotate for inclination
	inclRad := orbit.Inclination * math.Pi / 180.0
	xIncl := xOrbit
	yIncl := yOrbit * math.Cos(inclRad)
	zIncl := yOrbit * math.Sin(inclRad)

	// Rotate for ascending node
	nodeRad := orbit.AscendingNode * math.Pi / 180.0
	x := xIncl*math.Cos(nodeRad) - yIncl*math.Sin(nodeRad)
	y := xIncl*math.Sin(nodeRad) + yIncl*math.Cos(nodeRad)
	z := zIncl

	return Position{X: x, Y: y, Z: z}
}

// generateQuantumKey generates a new quantum key ID
func generateQuantumKey() (string, time.Time) {
	keyID := fmt.Sprintf("QK-%05d", rand.Intn(90000)+10000)
	return keyID, time.Now()
}

// createConstellation initializes a satellite constellation
func createConstellation(numSatellites int) *Constellation {
	constellation := &Constellation{
		Satellites: make([]*Satellite, numSatellites),
	}

	for i := 0; i < numSatellites; i++ {
		// Create varied orbit parameters
		altitude := 500.0 + float64(rand.Intn(300))
		inclination := 45.0 + float64(rand.Intn(45))
		ascendingNode := float64(rand.Intn(360))
		initialAnomaly := float64(rand.Intn(360))
		launchTime := time.Now()

		keyID, keyTime := generateQuantumKey()

		sat := &Satellite{
			ID:             fmt.Sprintf("SAT-%03d", i+1),
			Name:           fmt.Sprintf("ThunderBird-%d", i+1),
			OrbitType:      "LEO",
			Altitude:       altitude,
			Inclination:    inclination,
			AscendingNode:  ascendingNode,
			InitialAnomaly: initialAnomaly,
			LaunchTime:     launchTime,
			Position:       Position{X: 0, Y: 0, Z: 0}, // Will be updated
			LastContact:    time.Now(),
			QuantumKeyID:   keyID,
			KeyGeneration:  keyTime,
			Status:         "operational",
		}

		constellation.Satellites[i] = sat
	}

	return constellation
}

// updateTelemetry updates all satellite positions and statuses
func (c *Constellation) updateTelemetry() {
	for _, sat := range c.Satellites {
		// Update position based on orbital parameters
		orbit := SatelliteOrbit{
			Altitude:      sat.Altitude,
			Inclination:   sat.Inclination,
			AscendingNode: sat.AscendingNode,
			Anomaly:       sat.InitialAnomaly,
			LaunchTime:    sat.LaunchTime,
		}

		sat.Position = getPosition(orbit)
		sat.LastContact = time.Now()

		// Occasionally regenerate quantum key
		if rand.Float64() < 0.05 {
			sat.QuantumKeyID, sat.KeyGeneration = generateQuantumKey()
		}

		// Occasionally have brief communication issues
		if rand.Float64() < 0.02 {
			sat.Status = "limited_connection"
		} else {
			sat.Status = "operational"
		}
	}
}

func main() {
	// Parse command line arguments
	numSatellites := flag.Int("satellites", 5, "Number of satellites to simulate")
	port := flag.Int("port", 9090, "Port to run the HTTP server on")
	flag.Parse()

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// Create constellation
	constellation := createConstellation(*numSatellites)

	// Start a goroutine to update telemetry regularly
	go func() {
		for {
			constellation.updateTelemetry()
			time.Sleep(2 * time.Second)
		}
	}()

	// Set up HTTP handler for telemetry
	http.HandleFunc("/telemetry", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")

		// Marshal satellite data to JSON
		data, err := json.Marshal(constellation.Satellites)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.Write(data)
	})

	// Start HTTP server
	fmt.Printf("🛰️ Satellite Simulator running on port %d\n", *port)
	fmt.Printf("Constellation: %d satellites\n", *numSatellites)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", *port), nil))
}
