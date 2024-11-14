import numpy as np
import librosa
import soundfile as sf
from scipy.signal import find_peaks
from scipy.stats import iqr
from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import timedelta

@dataclass
class WhistleEvent:
    """Class to store detected whistle events"""
    timestamp: float
    duration: float
    intensity: float
    confidence: float

class WhistleDetector:
    def __init__(
        self,
        sample_rate: int = 22050,
        frame_length: int = 2048,
        hop_length: int = 512,
        freq_min: float = 2000,
        freq_max: float = 4000,
        min_duration: float = 0.1,  # Minimum whistle duration in seconds
        window_size: float = 1.0    # Window size for statistical analysis in seconds
    ):
        self.sample_rate = sample_rate
        self.frame_length = frame_length
        self.hop_length = hop_length
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.min_duration = min_duration
        self.window_size = window_size
        
        # Convert frequency range to FFT bins
        self.bin_min = int(freq_min * frame_length / sample_rate)
        self.bin_max = int(freq_max * frame_length / sample_rate)

    def _remove_outliers(self, data: np.ndarray, threshold: float = 1.5) -> np.ndarray:
        """Remove outliers using IQR method"""
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr_value = q3 - q1
        lower_bound = q1 - threshold * iqr_value
        upper_bound = q3 + threshold * iqr_value
        return np.clip(data, lower_bound, upper_bound)

    def _analyze_window(self, 
                       spectrogram: np.ndarray, 
                       start_frame: int, 
                       window_frames: int) -> Tuple[float, float]:
        """Analyze a time window of the spectrogram"""
        window = spectrogram[:, start_frame:start_frame + window_frames]
        window_energy = np.mean(window, axis=0)
        
        # Remove outliers
        cleaned_energy = self._remove_outliers(window_energy)
        
        # Calculate statistics
        window_min = np.min(cleaned_energy)
        window_median = np.median(cleaned_energy)
        
        return window_min, window_median

    def detect_whistles(self, audio_path: str) -> List[WhistleEvent]:
        """
        Detect whistles using statistical analysis of spectral energy
        """
        # Load audio
        audio, _ = librosa.load(audio_path, sr=self.sample_rate)
        
        # Compute spectrogram
        D = librosa.stft(audio, n_fft=self.frame_length, hop_length=self.hop_length)
        mag_spec = np.abs(D)
        
        # Focus on whistle frequency range
        whistle_band = mag_spec[self.bin_min:self.bin_max, :]
        
        # Calculate window size in frames
        window_frames = int(self.window_size * self.sample_rate / self.hop_length)
        
        whistle_events = []
        frame_idx = 0
        
        while frame_idx < whistle_band.shape[1] - window_frames:
            # Analyze current window
            window_min, window_median = self._analyze_window(
                whistle_band, frame_idx, window_frames
            )
            
            # Get energy for current frame
            frame_energy = np.mean(whistle_band[:, frame_idx])
            
            # Check if current frame energy is between min and median (potential whistle)
            if window_min <= frame_energy <= window_median:
                # Look for continuous frames that satisfy the condition
                start_frame = frame_idx
                while (frame_idx < whistle_band.shape[1] and 
                       window_min <= np.mean(whistle_band[:, frame_idx]) <= window_median):
                    frame_idx += 1
                
                duration = librosa.frames_to_time(
                    frame_idx - start_frame,
                    sr=self.sample_rate,
                    hop_length=self.hop_length
                )
                
                # Only consider events longer than minimum duration
                if duration >= self.min_duration:
                    # Calculate confidence based on how close energy is to median
                    avg_energy = np.mean([np.mean(whistle_band[:, i]) 
                                        for i in range(start_frame, frame_idx)])
                    energy_range = window_median - window_min
                    if energy_range > 0:
                        confidence = 1 - ((window_median - avg_energy) / energy_range)
                    else:
                        confidence = 0.5
                    
                    event = WhistleEvent(
                        timestamp=librosa.frames_to_time(start_frame, 
                                                       sr=self.sample_rate,
                                                       hop_length=self.hop_length),
                        duration=duration,
                        intensity=avg_energy,
                        confidence=confidence
                    )
                    whistle_events.append(event)
            else:
                frame_idx += 1
            
        return whistle_events

    def format_timestamp(self, seconds: float) -> Tuple[str, str]:
        """Convert seconds to minutes and seconds"""
        time = str(timedelta(seconds=int(seconds)))
        return time.split(':')[1:]

    def print_detections(self, whistle_events: List[WhistleEvent]):
        """Print detected whistle events in a readable format"""
        print("\nDetected Whistle Events:")
        print("-" * 65)
        print(f"{'Time':>10} | {'Duration (s)':>12} | {'Intensity':>10} | {'Confidence':>10}")
        print("-" * 65)
        
        for event in whistle_events:
            minutes, seconds = self.format_timestamp(event.timestamp)
            print(f"{minutes}:{seconds:>02} | {event.duration:>12.2f} | {event.intensity:>10.2f} | {event.confidence:>10.2f}")

def main():
    detector = WhistleDetector(
        freq_min=2000,
        freq_max=4000,
        min_duration=0.1,
        window_size=1.0
    )
    
    # Replace with your audio file path
    audio_path = "/home/thiendc/projects/video_summarization/v2/output_first_40_seconds.wav"
    
    try:
        whistle_events = detector.detect_whistles(audio_path)
        detector.print_detections(whistle_events)
        
        print(f"\nTotal whistles detected: {len(whistle_events)}")
        
    except Exception as e:
        print(f"Error processing audio file: {str(e)}")

if __name__ == "__main__":
    main()