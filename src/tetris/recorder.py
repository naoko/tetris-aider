"""Screen recorder for Tetris gameplay."""

import os
import time
import cv2
import numpy as np
import pygame
from datetime import datetime

class GameRecorder:
    """Records Tetris gameplay and saves it as a video file."""
    
    def __init__(self, fps=30, output_dir="recordings"):
        """Initialize the recorder.
        
        Args:
            fps: Frames per second for the output video
            output_dir: Directory to save recordings
        """
        self.fps = fps
        self.output_dir = output_dir
        self.recording = False
        self.frames = []
        self.start_time = None
        self.max_duration = 30  # Maximum recording duration in seconds
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
    
    def start_recording(self):
        """Start recording gameplay."""
        self.recording = True
        self.frames = []
        self.start_time = time.time()
        print("Recording started...")
    
    def capture_frame(self, surface):
        """Capture the current frame from the pygame surface.
        
        Args:
            surface: Pygame surface to capture
        """
        if not self.recording:
            return
            
        # Check if we've exceeded the maximum duration
        if time.time() - self.start_time > self.max_duration:
            self.stop_recording()
            return
            
        # Convert pygame surface to numpy array
        frame = pygame.surfarray.array3d(surface)
        # Transpose to get the correct format for OpenCV
        frame = np.transpose(frame, (1, 0, 2))
        # Convert from RGB to BGR (OpenCV format)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        self.frames.append(frame)
    
    def stop_recording(self):
        """Stop recording and save the video."""
        if not self.recording or not self.frames:
            return
            
        self.recording = False
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"tetris_gameplay_{timestamp}.mp4")
        
        # Get dimensions from the first frame
        height, width = self.frames[0].shape[:2]
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, self.fps, (width, height))
        
        # Write frames to video
        for frame in self.frames:
            out.write(frame)
        
        # Release resources
        out.release()
        
        print(f"Recording saved to {filename}")
        self.frames = []

def create_demo_recording(game_instance, duration=20):
    """Create a demo recording of gameplay.
    
    Args:
        game_instance: Instance of TetrisGame
        duration: Duration of recording in seconds
    """
    recorder = GameRecorder()
    recorder.start_recording()
    
    # Store the original _render method
    original_render = game_instance._render
    
    # Override the render method to capture frames
    def wrapped_render():
        original_render()
        recorder.capture_frame(pygame.display.get_surface())
    
    # Replace the render method
    game_instance._render = wrapped_render
    
    # Set a timer to stop recording
    start_time = time.time()
    
    # Run the game with recording
    while time.time() - start_time < duration and game_instance.running:
        game_instance._handle_events()
        game_instance._update_game()
        game_instance._render()
        
    # Stop recording
    recorder.stop_recording()
    
    # Restore original render method
    game_instance._render = original_render
    
    return recorder
