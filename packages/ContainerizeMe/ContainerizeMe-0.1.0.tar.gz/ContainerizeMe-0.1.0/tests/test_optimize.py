import unittest
from containerizeme.optimize import optimize_dockerfile

class TestOptimizeDockerfile(unittest.TestCase):
    def test_optimize_dockerfile(self):
        original = "test_files/Dockerfile.original"
        optimized = "test_files/Dockerfile.optimized"

        optimize_dockerfile(original, optimized)

        with open(optimized, "r") as file:
            lines = file.readlines()

        self.assertIn("apt-get install", lines[0])  # Example assertion

if __name__ == "__main__":
    unittest.main()
