import docker
from .utils import log_message

def optimize_dockerfile(dockerfile_path: str, output_path: str) -> None:
    """
    Reads a Dockerfile, suggests improvements, and outputs an optimized version.
    
    Args:
        dockerfile_path (str): Path to the original Dockerfile.
        output_path (str): Path to save the optimized Dockerfile.
    """
    try:
        log_message("Reading Dockerfile...")
        with open(dockerfile_path, "r") as file:
            lines = file.readlines()

        optimized_lines = []
        for line in lines:
            # Example optimization: Remove unnecessary layers
            if line.strip().startswith("RUN apt-get update && apt-get install"):
                optimized_lines.append(line.replace("apt-get update &&", "apt-get install"))
            else:
                optimized_lines.append(line)
        
        log_message("Saving optimized Dockerfile...")
        with open(output_path, "w") as file:
            file.writelines(optimized_lines)

        log_message(f"Optimized Dockerfile saved at {output_path}")
    except Exception as e:
        log_message(f"Error optimizing Dockerfile: {e}")
        raise
