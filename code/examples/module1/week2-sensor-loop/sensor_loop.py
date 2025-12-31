"""
Sensor Loop Example

This script demonstrates the fundamental concept of continuous sensing in Physical AI systems.
It simulates multiple sensors continuously gathering data, processing it, and responding
to environmental changes in real-time.
"""

import time
import random
import threading
import queue
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class SensorData:
    """Represents data from a sensor."""
    sensor_id: str
    sensor_type: str
    value: float
    timestamp: float
    confidence: float = 1.0  # Confidence level (0.0 to 1.0)


class MockSensor:
    """Simulates a physical sensor."""

    def __init__(self, sensor_id: str, sensor_type: str, base_value: float = 0.0, noise_level: float = 0.1):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.base_value = base_value
        self.noise_level = noise_level
        self.is_active = True
        self.last_reading = None

    def read(self) -> SensorData:
        """Simulate reading from the sensor."""
        if not self.is_active:
            return None

        # Add some randomness to simulate real sensor noise
        noise = random.uniform(-self.noise_level, self.noise_level)
        value = self.base_value + noise

        # Simulate occasional sensor fluctuations
        if random.random() < 0.05:  # 5% chance of significant change
            value += random.uniform(-1.0, 1.0)

        self.last_reading = SensorData(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=value,
            timestamp=time.time(),
            confidence=0.95 if abs(noise) < 0.3 else 0.7  # Lower confidence for noisy readings
        )

        return self.last_reading


class SensorFusion:
    """Handles combining data from multiple sensors."""

    def __init__(self):
        self.recent_readings: Dict[str, List[SensorData]] = {}
        self.max_history = 10  # Keep last 10 readings for each sensor

    def add_reading(self, reading: SensorData):
        """Add a new sensor reading."""
        if reading.sensor_id not in self.recent_readings:
            self.recent_readings[reading.sensor_id] = []

        self.recent_readings[reading.sensor_id].append(reading)

        # Limit history size
        if len(self.recent_readings[reading.sensor_id]) > self.max_history:
            self.recent_readings[reading.sensor_id] = self.recent_readings[reading.sensor_id][-self.max_history:]

    def get_environment_state(self) -> Dict:
        """Get a combined view of the environment based on all sensor data."""
        state = {
            'timestamp': time.time(),
            'sensors_active': len(self.recent_readings),
            'average_values': {},
            'trends': {},
            'anomalies': []
        }

        for sensor_id, readings in self.recent_readings.items():
            if readings:
                # Calculate average value
                avg_value = sum(r.value for r in readings) / len(readings)
                state['average_values'][sensor_id] = avg_value

                # Detect trends (simple: compare first and last reading)
                if len(readings) >= 2:
                    first_val = readings[0].value
                    last_val = readings[-1].value
                    trend = last_val - first_val
                    state['trends'][sensor_id] = trend

                    # Detect anomalies (values that deviate significantly)
                    for reading in readings:
                        if abs(reading.value - avg_value) > 1.5:  # Arbitrary threshold
                            state['anomalies'].append({
                                'sensor_id': reading.sensor_id,
                                'value': reading.value,
                                'timestamp': reading.timestamp,
                                'deviation': abs(reading.value - avg_value)
                            })

        return state


class SensorProcessor:
    """Processes sensor data and makes decisions."""

    def __init__(self, fusion_module: SensorFusion):
        self.fusion_module = fusion_module
        self.event_log = []
        self.callbacks = []

    def register_callback(self, callback_func):
        """Register a callback function to be called when significant events occur."""
        self.callbacks.append(callback_func)

    def process_data(self, reading: SensorData):
        """Process a single sensor reading."""
        # Add reading to fusion module
        self.fusion_module.add_reading(reading)

        # Get current environment state
        state = self.fusion_module.get_environment_state()

        # Check for significant events
        event_occurred = False
        event_details = {
            'type': 'normal',
            'sensor_id': reading.sensor_id,
            'value': reading.value,
            'timestamp': reading.timestamp
        }

        # Check for anomalies
        for anomaly in state['anomalies']:
            if anomaly['sensor_id'] == reading.sensor_id:
                event_details['type'] = 'anomaly'
                event_details['deviation'] = anomaly['deviation']
                event_occurred = True
                break

        # Check for significant trends
        if reading.sensor_id in state['trends']:
            trend = state['trends'][reading.sensor_id]
            if abs(trend) > 2.0:  # Arbitrary threshold
                event_details['type'] = 'trend_change'
                event_details['trend'] = trend
                event_occurred = True

        # Log the event
        self.event_log.append(event_details)

        # Call callbacks if an event occurred
        if event_occurred and self.callbacks:
            for callback in self.callbacks:
                callback(event_details)

        return event_details


class SensorLoop:
    """Main sensor loop that continuously reads from sensors."""

    def __init__(self, update_interval: float = 0.1):  # 100ms default
        self.sensors: List[MockSensor] = []
        self.update_interval = update_interval
        self.is_running = False
        self.fusion_module = SensorFusion()
        self.processor = SensorProcessor(self.fusion_module)
        self.data_queue = queue.Queue()
        self.stats = {
            'readings_processed': 0,
            'events_detected': 0,
            'start_time': None
        }

    def add_sensor(self, sensor: MockSensor):
        """Add a sensor to the loop."""
        self.sensors.append(sensor)

    def add_callback(self, callback_func):
        """Add a callback for significant events."""
        self.processor.register_callback(callback_func)

    def sensor_callback(self, event_details):
        """Default callback for sensor events."""
        self.stats['events_detected'] += 1
        print(f"[EVENT] {event_details['type'].upper()}: {event_details['sensor_id']} = {event_details['value']:.2f}")

    def start(self):
        """Start the continuous sensor loop."""
        if self.is_running:
            print("Sensor loop is already running")
            return

        self.is_running = True
        self.stats['start_time'] = time.time()
        print("Starting sensor loop...")

        # Register default callback
        self.add_callback(self.sensor_callback)

        try:
            while self.is_running:
                cycle_start = time.time()

                # Read from all active sensors
                for sensor in self.sensors:
                    if sensor.is_active:
                        reading = sensor.read()
                        if reading:
                            # Process the reading
                            event_details = self.processor.process_data(reading)
                            self.stats['readings_processed'] += 1

                            # Add to data queue for external access if needed
                            try:
                                self.data_queue.put_nowait(reading)
                            except queue.Full:
                                pass  # Queue is full, skip this reading

                # Control timing
                cycle_time = time.time() - cycle_start
                sleep_time = max(0, self.update_interval - cycle_time)

                if sleep_time > 0:
                    time.sleep(sleep_time)

                # Periodic status update
                if self.stats['readings_processed'] % 50 == 0:
                    elapsed = time.time() - self.stats['start_time']
                    print(f"[STATUS] {self.stats['readings_processed']} readings, "
                          f"{self.stats['events_detected']} events in {elapsed:.1f}s")

        except KeyboardInterrupt:
            print("\nStopping sensor loop...")
        finally:
            self.stop()

    def stop(self):
        """Stop the sensor loop."""
        self.is_running = False
        print("Sensor loop stopped")


def main():
    """Main function to demonstrate the sensor loop."""
    print("Physical AI Sensor Loop Example")
    print("=" * 40)

    # Create the sensor loop
    sensor_loop = SensorLoop(update_interval=0.2)  # Update every 200ms

    # Create various types of sensors
    sensors = [
        MockSensor("vision_01", "camera", base_value=10.0, noise_level=0.5),
        MockSensor("proximity_01", "lidar", base_value=5.0, noise_level=0.3),
        MockSensor("temperature_01", "thermometer", base_value=22.0, noise_level=0.2),
        MockSensor("accelerometer_01", "imu", base_value=0.0, noise_level=0.1),
        MockSensor("microphone_01", "audio", base_value=0.5, noise_level=0.4)
    ]

    # Add sensors to the loop
    for sensor in sensors:
        sensor_loop.add_sensor(sensor)
        print(f"Added {sensor.sensor_type} sensor: {sensor.sensor_id}")

    print(f"\nStarting sensor loop with {len(sensors)} sensors...")
    print("Press Ctrl+C to stop the loop\n")

    # Start the loop
    sensor_loop.start()

    # Print final statistics
    elapsed = time.time() - sensor_loop.stats['start_time']
    print(f"\nFinal Statistics:")
    print(f"  Total readings processed: {sensor_loop.stats['readings_processed']}")
    print(f"  Events detected: {sensor_loop.stats['events_detected']}")
    print(f"  Runtime: {elapsed:.1f} seconds")
    print(f"  Average rate: {sensor_loop.stats['readings_processed']/elapsed:.1f} readings/sec")


if __name__ == "__main__":
    main()