"""
Generate a simple alert sound file (alert.wav)
Run this script once to create the alert sound for the drowsiness detection system
"""

import numpy as np
import wave
import struct


def generate_alert_sound(filename="alert.wav", duration=10, frequency=1000, sample_rate=44100):
    """
    Generate a continuous beeping alert sound with pulses
    
    Parameters:
    - filename: Output file name
    - duration: Duration in seconds (default: 10 seconds continuous)
    - frequency: Frequency in Hz
    - sample_rate: Sample rate in Hz
    """
    
    # Create pulsing alert (on/off pattern)
    pulse_duration = 0.3  # 300ms beep
    silence_duration = 0.2  # 200ms silence
    pulse_cycle = pulse_duration + silence_duration
    
    # Calculate total samples needed
    total_samples = int(sample_rate * duration)
    signal = np.zeros(total_samples)
    
    # Fill with pulsing pattern
    current_sample = 0
    while current_sample < total_samples:
        # On phase - beep
        on_samples = int(sample_rate * pulse_duration)
        if current_sample + on_samples <= total_samples:
            t = np.linspace(0, pulse_duration, on_samples)
            beep = np.sin(2 * np.pi * frequency * t)
            signal[current_sample:current_sample + on_samples] = beep * 32767 * 0.8
            current_sample += on_samples
        
        # Off phase - silence
        off_samples = int(sample_rate * silence_duration)
        if current_sample + off_samples <= total_samples:
            current_sample += off_samples
    
    # Convert to 16-bit audio
    signal = signal.astype(np.int16)
    
    # Create WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes = 16 bits
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(signal.tobytes())
    
    print(f"✓ Continuous alert sound created: {filename} ({duration}s duration)")


if __name__ == "__main__":
    generate_alert_sound()
    print("\nYou can now run: python drowsiness_detector.py")
