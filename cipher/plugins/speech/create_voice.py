#!/usr/bin/env python3
import argparse
import os
import sys

# Ensure this is only run when torch and neucodec are available (dev environment)
try:
    import torch
    import numpy as np
    from librosa import load
    from neucodec import NeuCodec
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("This script requires 'torch', 'librosa', and 'neucodec'.")
    print("Please ensure you are running it in the dev environment: pixi run -e dev python cipher/plugins/speech/create_voice.py ...")
    sys.exit(1)

# Get the path to the voices directory relative to this script
VOICES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voices')

def main():
    parser = argparse.ArgumentParser(description="Create a NeuTTS voice reference from an audio file.")
    parser.add_argument("--wav", type=str, required=True, help="Path to the reference audio file (.wav)")
    parser.add_argument("--text", type=str, required=True, help="Exact text spoken in the reference audio")
    parser.add_argument("--name", type=str, required=True, help="Name to give to the new voice (e.g. 'juliette')")
    parser.add_argument("--device", type=str, default="cpu", help="Device to run the encoder on (default: cpu)")
    
    args = parser.parse_args()

    if not os.path.exists(args.wav):
        print(f"Error: Audio file not found at '{args.wav}'")
        sys.exit(1)

    # Ensure voices directory exists
    os.makedirs(VOICES_DIR, exist_ok=True)

    out_npy_path = os.path.join(VOICES_DIR, f"{args.name}.npy")
    out_txt_path = os.path.join(VOICES_DIR, f"{args.name}.txt")

    print(f"Loading NeuCodec on {args.device}...")
    codec = NeuCodec.from_pretrained("neuphonic/neucodec")
    codec.eval().to(args.device)

    print(f"Loading reference audio '{args.wav}'...")
    # NeuCodec expects 16kHz mono audio
    wav, _ = load(args.wav, sr=16000, mono=True)
    
    # Convert to tensor [B, C, T] -> [1, 1, T]
    wav_tensor = torch.from_numpy(wav).float().unsqueeze(0).unsqueeze(0).to(args.device)

    print("Encoding audio...")
    with torch.no_grad():
        ref_codes = codec.encode_code(audio_or_path=wav_tensor)
        # Squeeze to get [1, 1, F] -> [F] or however it's structured in neutts_lite
        # NeuTTS expects the reference codes to be a numpy array.
        ref_codes = ref_codes.squeeze(0).squeeze(0)
    
    ref_codes_np = ref_codes.cpu().numpy()

    print(f"Saving voice '{args.name}'...")
    np.save(out_npy_path, ref_codes_np)
    
    with open(out_txt_path, "w", encoding="utf-8") as f:
        f.write(args.text.strip())

    print("\nSuccess!")
    print(f"Voice '{args.name}' has been created in:")
    print(f"  - {out_npy_path}")
    print(f"  - {out_txt_path}")
    print("\nYou can now select it in the CIPHER web interface.")

if __name__ == "__main__":
    main()
