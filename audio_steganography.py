import wave
import numpy as np
from pydub import AudioSegment

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    num_bits = 8 * len(text.encode(encoding, errors))
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(num_bits)

def bits_to_text(bits, encoding='utf-8', errors='replace'):
    if not bits:
        return ''
    n = int(bits, 2)
    try:
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors)
    except UnicodeDecodeError:
        return ''

def convert_to_wav(file_path):
    if file_path.lower().endswith('.wav'):
        return file_path
    audio = AudioSegment.from_file(file_path)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")
    return wav_path

def encode_wav(file_path, text, num_lsb=1, output_file='encoded.wav'):
    wav_path = convert_to_wav(file_path)
    with wave.open(wav_path, 'rb') as audio:
        params = audio.getparams()
        frames = audio.readframes(audio.getnframes())

    audio_data = np.frombuffer(frames, dtype=np.uint8)
    writable_audio_data = np.copy(audio_data)
    text_bits = text_to_bits(text)
    
    if len(text_bits) > len(audio_data) * num_lsb:
        raise ValueError("Text too long to encode in provided audio file with current LSB setting.")

    text_bits += '0' * ((len(audio_data) * num_lsb) - len(text_bits))

    for i in range(0, len(text_bits), num_lsb):
        byte_index = i // num_lsb
        writable_audio_data[byte_index] = (writable_audio_data[byte_index] & ~((1 << num_lsb) - 1)) | int(text_bits[i:i + num_lsb], 2)

    with wave.open(output_file, 'wb') as audio:
        audio.setparams(params)
        audio.writeframes(writable_audio_data.tobytes())

def decode_wav(file_path, num_lsb=1):
    wav_path = convert_to_wav(file_path)
    with wave.open(wav_path, 'rb') as audio:
        frames = audio.readframes(audio.getnframes())

    audio_data = np.frombuffer(frames, dtype=np.uint8)
    bits = ''.join(bin(byte & ((1 << num_lsb) - 1))[2:].zfill(num_lsb) for byte in audio_data)

    return bits_to_text(bits)
