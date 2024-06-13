import wave  # Module for handling WAV files
import numpy as np  # Library for numerical operations
from pydub import AudioSegment  # Library for handling various audio file formats

# Converts a text string into a binary string
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    # Calculate the number of bits needed to represent the text
    num_bits = 8 * len(text.encode(encoding, errors))
    # Convert text to an integer, then to a binary string
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    # Pad the binary string with leading zeros
    return bits.zfill(num_bits)

# Converts a binary string back into a text string
def bits_to_text(bits, encoding='utf-8', errors='replace'):
    if not bits:
        return ''
    # Convert binary string to an integer
    n = int(bits, 2)
    try:
        # Convert integer to bytes, then decode to text
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors)
    except UnicodeDecodeError:
        return ''

# Converts an audio file to WAV format if it isn't already
def convert_to_wav(file_path):
    # If the file is already WAV, return the path
    if file_path.lower().endswith('.wav'):
        return file_path
    # Convert other formats to WAV using pydub
    audio = AudioSegment.from_file(file_path)
    wav_path = "temp.wav"  # Temporary WAV file path
    audio.export(wav_path, format="wav")  # Export as WAV
    return wav_path

# Encodes text into a WAV file using the specified number of least significant bits (LSBs)
def encode_wav(file_path, text, num_lsb=1, output_file='encoded.wav'):
    wav_path = convert_to_wav(file_path)  # Ensure file is in WAV format
    with wave.open(wav_path, 'rb') as audio:
        params = audio.getparams()  # Get audio parameters
        frames = audio.readframes(audio.getnframes())  # Read all audio frames
    
    # Add markers to text to identify boundaries during decoding
    text = "=====" + text + "====="
    
    # Convert audio frames to a numpy array
    audio_data = np.frombuffer(frames, dtype=np.uint8)
    writable_audio_data = np.copy(audio_data)  # Make a writable copy
    text_bits = text_to_bits(text)  # Convert text to binary string
    
    # Check if text can fit in the audio file with the given LSBs
    if len(text_bits) > len(audio_data) * num_lsb:
        raise ValueError("Text too long to encode in provided audio file with current LSB setting.")
    
    # Pad the text bits to match the length of audio data
    text_bits += '0' * ((len(audio_data) * num_lsb) - len(text_bits))
    
    # Encode text bits into audio data LSBs
    for i in range(0, len(text_bits), num_lsb):
        byte_index = i // num_lsb  # Determine which byte to modify
        writable_audio_data[byte_index] = (
            (writable_audio_data[byte_index] & ~((1 << num_lsb) - 1)) |
            int(text_bits[i:i + num_lsb], 2)
        )
    
    # Write the modified audio data to a new file
    with wave.open(output_file, 'wb') as audio:
        audio.setparams(params)  # Set audio parameters
        audio.writeframes(writable_audio_data.tobytes())  # Write frames

# Decodes text from a WAV file using the specified number of LSBs
def decode_wav(file_path, num_lsb=1):
    wav_path = convert_to_wav(file_path)  # Ensure file is in WAV format
    with wave.open(wav_path, 'rb') as audio:
        frames = audio.readframes(audio.getnframes())  # Read all audio frames
    
    # Convert audio frames to a numpy array
    audio_data = np.frombuffer(frames, dtype=np.uint8)
    
    # Extract LSBs from each byte in the audio data
    bits = ''.join(
        bin(byte & ((1 << num_lsb) - 1))[2:].zfill(num_lsb)
        for byte in audio_data
    )
    
    # Convert the binary string to text
    decoded_text = bits_to_text(bits)
    
    # Check for the boundary markers in the decoded text
    if "=====" in decoded_text:
        start_index = decoded_text.index("=====") + 5  # Find start marker
        end_index = decoded_text.rindex("=====")  # Find end marker
        decoded_text = decoded_text[start_index:end_index]  # Extract text
        return decoded_text
    else:
        raise ValueError("Error Decoding. Bits used does not match bits used in encoding.")  # Raise error if markers are not found
