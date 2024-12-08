import wave
import numpy as np

def read_wav_file(filename):
    with wave.open(filename, 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        duration = num_frames / frame_rate

        audio_data = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

        return audio_data, num_channels, sample_width, frame_rate, num_frames, duration
    
def read_wav_file_metadata(filename):
    with wave.open(filename, 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        duration = num_frames / frame_rate

        return num_channels, sample_width, frame_rate, num_frames, duration
    
def get_wav_num_channels(filename):
    with wave.open(filename, 'rb') as wav_file:
        return wav_file.getnchannels()
    
def get_wav_sample_width(filename):
    with wave.open(filename, 'rb') as wav_file:
        return wav_file.getsampwidth()
    
def get_wav_frame_rate(filename):
    with wave.open(filename, 'rb') as wav_file:
        return wav_file.getframerate()
    
def get_wav_num_frames(filename):
    with wave.open(filename, 'rb') as wav_file:
        return wav_file.getnframes()
    
def get_wav_duration(filename):
    with wave.open(filename, 'rb') as wav_file:
        return wav_file.getnframes() / wav_file.getframerate()

def get_wav_data(filename):
    with wave.open(filename, 'rb') as wav_file:
        return wav_file.readframes(wav_file.getnframes())
    
def write_wav_file(filename, audio_data, num_channels, sample_width, frame_rate):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)
        wav_file.writeframes(audio_data.tobytes())

def convert_array_to_wav(filename, audio_data, num_channels, sample_width, frame_rate):
    write_wav_file(filename, audio_data, num_channels, sample_width, frame_rate)

def split_wav_file(filename, duration):
    with wave.open(filename, 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        audio_data = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

        num_segments = int(np.ceil(num_frames / (duration * frame_rate)))
        segment_length = int(num_frames / num_segments)

        for i in range(num_segments):
            start_frame = i * segment_length
            end_frame = (i + 1) * segment_length
            if i == num_segments - 1:
                end_frame = num_frames

            segment_data = audio_data[start_frame:end_frame]
            segment_filename = f"{filename}_{i}.wav"
            write_wav_file(segment_filename, segment_data, num_channels, sample_width, frame_rate)


