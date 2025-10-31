# This file contains the code responsible
# for the creation of the subliminal audio.

from gtts import gTTS
from pydub import AudioSegment
from librosa import get_duration
import os

def sub_creator(title, affs_path, bg_path, repetitions=8):
    """
    Creates a subliminal audio file by repeating a block of affirmations.

    Args:
        title (str): The name for the output audio file.
        affs_path (str): The path to the .txt file containing affirmations.
        bg_path (str): The path to the background audio file (e.g., rain sounds).
        repetitions (int): The number of times the entire affirmation block is repeated.
    """
    # Create necessary directories if they don't exist
    os.makedirs('lib/.files', exist_ok=True)
    os.makedirs('subliminals/audios', exist_ok=True)

    # --- Step 1: Create the Affirmation Pulses in Text Form ---
    # Read the base affirmations from the file. This is considered one "block" or "pulse".
    with open(affs_path, 'r') as f:
        base_affs_txt = f.read().strip()

    # Duplicate the entire affirmation block 'repetitions' times to create one long string.
    # A space is added between each block for a natural pause.
    print(f"Preparing text block with {repetitions} repetitions of the affirmations.")
    affs_txt = (base_affs_txt + " ") * repetitions

    # --- Step 2: Generate a Single Audio File from the Repeated Text ---
    # Generates one continuous TTS audio file containing all the repeated pulses.
    print("Generating a single affirmations audio track from the repeated text...")
    gTTS(text=affs_txt, lang='en', slow=False).save('lib/.files/affs.wav')
    print("Affirmations audio track generated.")

    affs = AudioSegment.from_file('lib/.files/affs.wav')
    bg = AudioSegment.from_file(bg_path)

    length_affs = get_duration(path='lib/.files/affs.wav')
    length_bg = get_duration(path=bg_path)

    # --- Step 3: Match the Length of the Affirmations Track to the Background Track ---
    print(f"Affirmations track length: {length_affs:.2f}s | Background track length: {length_bg:.2f}s")

    # If the affirmations' audio file is SHORTER than the background's audio file,
    # REPEAT the entire affirmations track (which already contains N pulses)
    # until the two lengths are similar.
    if length_affs < length_bg:
        x = int(length_bg / length_affs)
        if x > 1:
            print(f"Repeating the full affirmations track {x} times to match background length...")
            affs = affs * x
        
        affs.export('lib/.files/affs.wav', format='wav')

    # If the affirmations' audio file is LONGER than the background's audio file,
    # SPEED UP the affirmations' audio file until the two lengths are similar.
    elif length_affs > length_bg:
        required_speed = length_affs / length_bg
        print(f"Affirmations are longer than background. Speeding up by a factor of {required_speed:.2f}...")
        
        affs = speed_change(affs, required_speed)
        affs.export('lib/.files/affs.wav', format='wav')
            
    # --- Step 4: Make Affirmations Subliminal and Overlay ---
    affs = AudioSegment.from_file('lib/.files/affs.wav')
    
    print("Lowering affirmations volume to a subliminal level...")
    affs = affs - 36 # Lower the volume by 36 dB.

    print("Overlaying affirmations onto background audio...")
    # Overlay the quieter affirmations onto the background.
    # The final audio will be the length of the background track.
    combined = bg.overlay(affs) 
    
    output_path = f'subliminals/audios/{title}.wav'
    combined.export(output_path, format='wav')
    print(f"Subliminal audio created successfully: {output_path}")

def speed_change(sound, speed=1.0):
    """
    Speeds up or slows down a pydub AudioSegment.
    """
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        'frame_rate': int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

# Example of how you might call this function from another file
if __name__ == '__main__':
    # Create dummy files for a self-contained example
    with open("my_affirmations.txt", "w") as f:
        f.write("I am love.\nI am joy.")
    
    # Create a silent 60-second background track for testing
    silent_bg = AudioSegment.silent(duration=60000) # 60 seconds
    silent_bg.export("background.mp3", format="mp3")

    print("\n--- RUNNING EXAMPLE ---")
    sub_creator(
        title="love_and_joy_subliminal_8_pulses",
        affs_path="my_affirmations.txt",
        bg_path="background.mp3",
        repetitions=8
    )
    print("--- EXAMPLE COMPLETE ---\n")
