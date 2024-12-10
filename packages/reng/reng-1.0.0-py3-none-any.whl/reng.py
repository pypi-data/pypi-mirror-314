import math
import threading
import random
import time


class RenderingEngine:
    """
    A simple rendering engine that computes mathematical values based on noise functions.
    """

    def __init__(self, limit, increase=0.02, decrease=0.0002):
        self.limit = limit
        self.increase = increase
        self.decrease = decrease
        self.noise1 = 0.4  # Initial noise seed for the first parameter
        self.noise2 = 1.0  # Initial noise seed for the second parameter
        self.result = 0
        self.running = False

    def noise(self, seed):
        """
        Generate pseudo-random noise based on a seed.
        """
        random.seed(seed)
        return random.uniform(-1, 1)

    def compute(self):
        """
        Continuously compute the rendering value while the engine is running.
        """
        pi = math.pi
        self.running = True
        while self.running:
            try:
                # Calculate noise values
                noise1_val = self.noise(self.noise1)
                noise2_val = self.noise(self.noise2)
                
                # Compute rendering value
                self.result = (
                    pi * math.sin(noise1_val) * math.tan(pi * noise2_val) /
                    max(math.cos(noise2_val), 1e-8)  # Avoid division by zero
                ) * self.limit
                
                # Update noise values
                self.noise1 += self.increase
                self.noise2 -= self.decrease

                # Small delay to simulate rendering cycle
                time.sleep(0.01)
            except Exception as e:
                print(f"Error in computation: {e}")
                break

    def start(self):
        """
        Start the rendering engine in a single thread.
        """
        if not self.running:
            thread = threading.Thread(target=self.compute)
            thread.daemon = True  # Ensure the thread stops with the main program
            thread.start()

    def stop(self):
        """
        Stop the rendering engine.
        """
        self.running = False

    def get_value(self):
        """
        Fetch the current rendering value.
        """
        return self.result


# Example Usage
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

