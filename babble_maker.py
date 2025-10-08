import argparse
import random
from pathlib import Path
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

def create_babble_effect(
    input_file: str,
    output_file: str,
    num_voices: int = 15,
    max_delay_ms: int = 2500,
    min_volume_reduction_db: int = 15,
    max_volume_reduction_db: int = 5,
    pitch_variation: float = 0.08
):
    """
    Reads an audio file and duplicates it to create a "babbling crowd" effect.

    Args:
        input_file (str): Path to the source audio file.
        output_file (str): Path to save the resulting audio file.
        num_voices (int): The number of overlapping voices to create.
        max_delay_ms (int): The maximum random start delay for each voice in milliseconds.
        min_volume_reduction_db (int): The minimum dB to reduce a voice's volume.
                                       (Higher number means quieter).
        max_volume_reduction_db (int): The maximum dB to reduce a voice's volume.
                                       (Lower number means louder).
        pitch_variation (float): The maximum pitch variation. 0.05 means +/- 5%.
    """
    print(f"Loading source audio from: {input_file}")
    try:
        # 1. Load the source audio file
        source_audio = AudioSegment.from_file(input_file)
    except CouldntDecodeError:
        print(f"Error: Could not decode {input_file}. Make sure it's a valid audio file and FFmpeg is installed.")
        return
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return

    # 2. Create a silent 'canvas' to layer the voices onto.
    #    The canvas needs to be long enough to hold the original audio plus the max delay.
    output_duration = len(source_audio) + max_delay_ms
    final_output = AudioSegment.silent(duration=output_duration)

    print(f"Generating {num_voices} voices to create the babble effect...")

    # 3. Loop to create and layer each voice
    for i in range(num_voices):
        print(f"  Processing voice {i + 1}/{num_voices}...")
        
        # Create a copy to manipulate
        voice_copy = source_audio

        # --- Apply Random Variations ---

        # a) Volume: Make some voices quieter than others
        volume_reduction = random.uniform(max_volume_reduction_db, min_volume_reduction_db)
        voice_copy = voice_copy - volume_reduction # pydub uses dB for volume changes

        # b) Panning: Place the voice in the stereo field (left/right)
        #    -1.0 is full left, 0.0 is center, 1.0 is full right
        pan_position = random.uniform(-0.9, 0.9)
        voice_copy = voice_copy.pan(pan_position)

        # c) Pitch (and speed): Slightly alter the pitch to simulate different people
        #    We do this by changing the frame rate.
        original_rate = voice_copy.frame_rate
        pitch_change = random.uniform(1 - pitch_variation, 1 + pitch_variation)
        new_rate = int(original_rate * pitch_change)
        voice_copy = voice_copy._spawn(voice_copy.raw_data, overrides={'frame_rate': new_rate})

        # d) Delay: Randomize the start time of this voice
        start_delay = random.randint(0, max_delay_ms)

        # 4. Overlay the manipulated voice onto our final output canvas
        final_output = final_output.overlay(voice_copy, position=start_delay)

    # 5. Export the final audio
    print(f"\nExporting final audio to: {output_file}")
    try:
        # Determine format from output file extension
        output_format = Path(output_file).suffix.lstrip('.')
        if not output_format: # Default to wav if no extension
            output_format = "wav"
            output_file += ".wav"
        
        final_output.export(output_file, format=output_format)
        print("Done!")
    except Exception as e:
        print(f"An error occurred during export: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a 'babbling crowd' effect from a single audio file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_file", help="Path to the source audio file (e.g., speech.wav).")
    parser.add_argument("output_file", help="Path to save the output audio file (e.g., crowd.mp3).")
    parser.add_argument("-v", "--voices", type=int, default=15, help="Number of voices in the crowd.")
    parser.add_argument("-d", "--delay", type=int, default=2500, help="Maximum start delay in milliseconds.")
    parser.add_argument("--min_vol", type=int, default=15, help="Minimum volume reduction in dB (quieter voices).")
    parser.add_argument("--max_vol", type=int, default=5, help="Maximum volume reduction in dB (louder voices).")
    parser.add_argument("-p", "--pitch", type=float, default=0.08, help="Maximum pitch variation (e.g., 0.08 for +/- 8%%).")

    args = parser.parse_args()

    create_babble_effect(
        input_file=args.input_file,
        output_file=args.output_file,
        num_voices=args.voices,
        max_delay_ms=args.delay,
        min_volume_reduction_db=args.min_vol,
        max_volume_reduction_db=args.max_vol,
        pitch_variation=args.pitch
    )
