# RenderingEngine README

## Overview
The `RenderingEngine` is a Python-based mathematical rendering engine that computes dynamic values based on pseudo-random noise functions. It runs continuously in a separate thread, updating the rendering value over time. This class is a simple demonstration of computational algorithms combined with threading and can serve as the basis for simulation or visualization systems.

---

## Features
- **Pseudo-random noise generation:** Generates dynamic values based on seeded random noise.
- **Mathematical calculations:** Uses trigonometric functions for value computation.
- **Threaded execution:** Runs in its own thread for non-blocking operation.
- **Configurable behavior:** Parameters like limits and noise increment/decrement rates can be adjusted.

---

## Requirements
- Python 3.6+
- Standard Python libraries (`math`, `random`, `threading`, `time`)

---

## Installation
Copy the `RenderingEngine` class into your project or save it as a `.py` file to use as a module.

---

## Usage

### Initialization
Create an instance of `RenderingEngine` with desired configuration parameters:
```python
from rendering_engine import RenderingEngine  # Import if saved as a module

reng = RenderingEngine(limit=100, increase=0.02, decrease=0.0002)
```

### Starting the Engine
Start the engine in a separate thread:
```python
reng.start()
```

### Fetching Values
Retrieve the current rendering value at any time:
```python
current_value = reng.get_value()
print(f"Current Rendering Value: {current_value}")
```

### Stopping the Engine
Stop the engine to end its computation loop:
```python
reng.stop()
```

### Example Code
```python
if __name__ == "__main__":
    reng = RenderingEngine(limit=100)
    reng.start()

    try:
        while True:
            print(f"Rendering Value: {reng.get_value()}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping Rendering Engine...")
        reng.stop()
```

---

## Parameters
- **`limit`** *(float)*: A multiplier for the rendering value's magnitude.
- **`increase`** *(float)*: The rate at which the first noise seed increases per cycle.
- **`decrease`** *(float)*: The rate at which the second noise seed decreases per cycle.

---

## How It Works
1. **Noise Generation:** Two pseudo-random noise values are computed using seeds.
2. **Mathematical Transformation:** The rendering value is derived by applying trigonometric functions (sin, tan, cos) and the limit multiplier.
3. **Threading:** The computation runs continuously in a background thread, allowing the main program to remain responsive.

---

## Notes
- Ensure to handle thread cleanup properly by calling the `stop` method to terminate the computation thread.
- This engine simulates dynamic value generation but is not optimized for high-precision or real-time applications.
- The mathematical calculations include safeguards against division by zero.

---

## License
This project is open-source and free to use under the MIT License. 

--- 

Feel free to customize or extend the `RenderingEngine` class for your specific use case!
