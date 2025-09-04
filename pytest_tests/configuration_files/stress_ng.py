import csv
import argparse
import os
import subprocess
import time
from datetime import datetime, timedelta
import psutil
import random
import math


DEFAULT_DURATION = 180
DEFAULT_CPU = 1
DEFAULT_MEMORY=2

MEMORY_LOWER_BOUND = 1
MEMORY_UPPER_BOUND = 64
CPU_LOWER_BOUND = 1
CPU_UPPER_BOUND = 64
RANGE = 10

MEMORY_VALUES = [2, 32, 16, 61, 5]
CPU_VALUES=[1, 8, 4, 13, 3]

# Define the structure to hold both CPU and memory data with a timestamp
class Metric:
    def __init__(self, cpu, mem, timestamp):
        self.cpu = cpu
        self.mem = mem
        self.timestamp = timestamp

# Get total system memory in MB
def get_total_memory_mb():
    return psutil.virtual_memory().total / (1024 * 1024)

# Helper function to parse the CSV file
def read_csv(file_path):
    data = {}
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for i, record in enumerate(reader):
            if i < 5:  # Skip the first 5 rows
                continue
            try:
                timestamp = datetime.strptime(record[0], "%Y/%m/%d %H:%M:%S")
                value = float(record[1])
                data[timestamp] = value
            except (ValueError, IndexError) as e:
                print(f"Error parsing row {i}: {e}")
    return data

"""
Run stress-ng with specified duration, memory, and CPU usage.

:param duration: Time to run stress-ng in seconds
:param memory: Amount of memory to stress in GB
:param cpu: Number of CPU cores to stress
:param cpu_percentage: Boolean flag to indicate if the cpu parameter represents a percentage.
                        If True, uses cpu as a percentage for --cpu-load. 
                        If False, uses cpu as a count for --cpu.
"""
def run_stress_ng(duration, memory, cpu, cpu_percentage):
    if cpu_percentage:
        # Use cpu-load if the CPU parameter is a percentage
        cpu_load = math.ceil(cpu)
        command = [
            "stress-ng",
            "--vm", "1",  # Stress a single VM worker
            "--vm-bytes", f"{memory}G",  # Memory to stress
            "--cpu-load", str(cpu_load),  # CPU load percentage
            "--timeout", f"{duration}s",  # Duration of the test
        ]
    else:
        # Use cpu if the CPU parameter is a number of cores
        command = [
            "stress-ng",
            "--vm", "1",  # Stress a single VM worker
            "--vm-bytes", f"{memory}G",  # Memory to stress
            "--cpu", str(cpu),  # Number of CPU cores to stress
            "--timeout", f"{duration}s",  # Duration of the test
        ]

    print(f"Running stress-ng with memory={memory}GB, cpu={cpu}, duration={duration}s")
    subprocess.run(command, check=True)

"""
Test stress-ng with a range of memory values.
:param duration: Time to run each test in seconds. Default=180s
:param cpu: Amount of CPU to test. Default=1
"""

def test_memory_values(duration=DEFAULT_DURATION, cpu=DEFAULT_CPU):

    for memory in MEMORY_VALUES:
        run_stress_ng(duration, memory, cpu, cpu_percentage=False)

"""
Test stress-ng with a range of CPU values.
:param duration: Time to run each test in seconds. Default=180s
:param memory: amount of memory in GB to test. Default=2GB
"""

def test_cpu_values(duration=DEFAULT_DURATION, memory=DEFAULT_MEMORY):

    for cpu in CPU_VALUES:
        run_stress_ng(duration, memory, cpu=cpu, cpu_percentage=False)


"""
Test stress-ng with a range of random memory values

:param duration: Time to run each test in seconds. Default=180s
:param cpu: Amount of CPU to test. Default=1
:param mem_min, mem_max: lower and upper bound for amount of memory in GB
:param num_tests: # of tests to run
"""

def test_random_memory(duration=DEFAULT_DURATION, cpu=DEFAULT_CPU, mem_min=MEMORY_LOWER_BOUND, mem_max=MEMORY_UPPER_BOUND, num_tests=RANGE):
    MEMORY_VALUES = [random.randint(mem_min, mem_max) for _ in range(num_tests)]
    for memory in MEMORY_VALUES:
        run_stress_ng(duration, memory, cpu, cpu_percentage=False)

"""
Test stress-ng with a range of cpu values.
:param duration: Time to run each test in seconds. Default=180s
:param memory: amount of memory in GB to test. Default=2GB
:param cpumin, cpumax: lower and upper bound for # of cpu cores
:param num_tests: # of tests to run
"""

def test_random_cpu(duration=DEFAULT_DURATION, memory=DEFAULT_MEMORY, cpu_min=CPU_LOWER_BOUND, cpu_max=CPU_UPPER_BOUND, num_tests=RANGE):
    cpu_values = [random.randint(cpu_min, cpu_max) for _ in range(num_tests)]
    for cpu in cpu_values:
        run_stress_ng(duration, memory, cpu, cpu_percentage=False)


"""
Test stress-ng with randomly generated memory and CPU values.
:param duration: Time to run each test in seconds. Default=180s
:param cpu_min, cpu_max: lower and upper bound for # of cpu cores
:param mem_min, mem_max: lower and upper bound for amount of memory in GB
:param num_tests: # of tests to run
"""

def test_random_memory_and_cpu(duration=DEFAULT_DURATION, mem_min=MEMORY_LOWER_BOUND, mem_max=MEMORY_UPPER_BOUND, cpu_min=CPU_LOWER_BOUND, cpu_max=CPU_UPPER_BOUND, num_tests=RANGE):
    for _ in range(num_tests):
        memory = random.randint(mem_min, mem_max)
        cpu = random.randint(cpu_min, cpu_max)
        run_stress_ng(duration, memory, cpu, cpu_percentage=False)

"""
Test stress-ng with CPU and memory values read from CSV files.

:param cpu_csv: Path to the CSV file containing CPU values and timestamps.
:param mem_csv: Path to the CSV file containing memory values and timestamps.
:param percent_mode: Boolean flag indicating whether CPU data should be treated as percentage or absolute value
:param speed_factor: Factor to control how fast to play the trace. Default is time difference btw the timestamps in curve.

The function reads the CPU and memory data from the specified CSV files,
merges the data based on timestamps, and runs stress-ng to simulate the CPU
and memory load according to the values in the CSV files. The duration for
running stress-ng is adjusted by the speed factor to control playback speed.
"""
def test_cpu_mem_from_curve(cpu_csv, mem_csv, percent_mode, speed_factor):
    # Perform tests with the CSV data
    print(f"Running test with CPU CSV: {cpu_csv}, Memory CSV: {mem_csv}")
    print(f"Percentage Mode: {'On' if percent_mode else 'Off'}, Speed Factor: {speed_factor}")
    
    # Read CPU and memory data from the CSV files
    try:
        cpu_data = read_csv(cpu_csv)
        mem_data = read_csv(mem_csv)
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        return
    # Merge CPU and memory data by matching timestamps
    metrics = []
    for timestamp, cpu in cpu_data.items():
        if timestamp in mem_data:
            mem = mem_data[timestamp]
            metrics.append(Metric(cpu, mem, timestamp))

    # Loop over the metrics and run stress-ng for each timestamp
    for i, m in enumerate(metrics):
        print(f"Timestamp: {m.timestamp}, CPU: {m.cpu:.2f}, Memory: {m.mem:.2f}")

        current_time = m.timestamp
        next_time = metrics[i + 1].timestamp if i + 1 < len(metrics) else current_time + timedelta(seconds=1)
        
        # Calculate the duration based on the timestamp difference
        original_duration = int((next_time - current_time).total_seconds())

        # If speed_factor is set explicitly, adjust the duration accordingly
        duration = original_duration if speed_factor is None else int(original_duration / speed_factor)
                
        if percent_mode:
            # Ceiling CPU value and treat as percentage
            m.cpu = math.ceil(m.cpu)
            # Get total system memory in bytes
            total_mem = psutil.virtual_memory().total
            
            # Calculate memory in bytes based on percentage (m.mem is a percentage of total memory)
            mem_bytes = int(m.mem * total_mem / 100)
            
            # Convert memory from bytes to GB (1 GB = 1024^3 bytes)
            mem_gb = mem_bytes / (1024 ** 3)
            run_stress_ng(duration, mem_gb, m.cpu, cpu_percentage=True)
        else:
            # Convert memory from MB to GB (1 GB = 1024 MB)
            mem_gb = m.mem / 1024
            # Run stress-ng with memory in GB and CPU cores
            run_stress_ng(duration, mem_gb, m.cpu, cpu_percentage=False)
        # Run stress-ng with calculated CPU and memory load
        run_stress_ng(duration, m.mem, m.cpu, True)


if __name__ == "__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpuCSV", default="cpu_data.csv", help="Path to the CPU CSV file")
    parser.add_argument("--memCSV", default="mem_data.csv", help="Path to the memory CSV file")
    parser.add_argument("--percent_mode", action="store_true", help="If set, interpret the CSV data as percentages. Otherwise, treat them as absolute values.")
    parser.add_argument("--speed_factor", type=float, help="Factor to control how fast to play the trace. If not set, use the curve's original timing.")

    args = parser.parse_args()
    
    # Perform tests
    # print("Testing memory values:")
    # test_memory_values()
    
    # print("Testing CPU values:")
    # test_cpu_values()
    
    # print("Testing with random cpu:")
    # test_random_cpu()

    # print("Testing with random memory:")
    # test_random_memory()

    # print("Testing with both random cpu and memory:")
    # test_random_memory_and_cpu()
    
    print("Testing CPU and Memory values from curve (CSV files):")
    test_cpu_mem_from_curve(args.cpuCSV, args.memCSV, args.percent_mode, args.speed_factor)