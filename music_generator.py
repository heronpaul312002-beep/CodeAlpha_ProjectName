import os
import glob
import pickle
import numpy as np
from music21 import converter, instrument, note, chord, stream
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Activation
from tensorflow.keras.utils import to_categorical

# ==============================================================================
# PHASE 1: DATA COLLECTION & PREPROCESSING
# ==============================================================================

def get_notes_from_midi(midi_dir):
    """ Parses a directory of MIDI files and extracts notes and chords. """
    notes = []
    
    # Ensure you have a folder named 'midi_songs' filled with MIDI files (.mid)
    if not os.path.exists(midi_dir) or len(os.listdir(midi_dir)) == 0:
        raise FileNotFoundError(f"Please create a '{midi_dir}' directory and add MIDI files.")

    print("Parsing MIDI files...")
    for file in glob.glob(os.path.join(midi_dir, "*.mid")):
        try:
            midi = converter.parse(file)
            print(f"Parsing: {file}")
            
            notes_to_parse = None
            try: # Given files with multiple instrument parts
                parts = instrument.partitionByInstrument(midi)
                notes_to_parse = parts.parts[0].recurse()
            except: # Given flat structures
                notes_to_parse = midi.flat.notes

            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    # Represent chords by joining string integers of pitches with dots
                    notes.append('.'.join(str(n) for n in element.normalOrder))
        except Exception as e:
            print(f"Failed to parse {file}: {e}")
            
    return notes

# ==============================================================================
# PHASE 2: PREPARE SEQUENCES FOR TRAINING
# ==============================================================================

def prepare_sequences(notes, sequence_length=100):
    """ Maps note strings to integers and builds input/output patterns. """
    # Get all unique pitch elements
    pitches = sorted(list(set(notes)))
    n_vocab = len(pitches)

    # Create mapping dictionary to map pitches to integers
    note_to_int = {note: num for num, note in enumerate(pitches)}

    network_input = []
    network_output = []

    # Generate input sequences and their corresponding targeted next notes
    for i in range(0, len(notes) - sequence_length):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # Reshape input pattern data into formats compatible with LSTM layers
    # Shape: [samples, time steps, features]
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    
    # Normalize input vector data
    network_input = network_input / float(n_vocab)

    # One-hot encode target output tracking arrays
    network_output = to_categorical(network_output, num_classes=n_vocab)

    return network_input, network_output, pitches, n_vocab

# ==============================================================================
# PHASE 3: BUILD THE DEEP LEARNING MODEL (LSTM)
# ==============================================================================

def create_network(network_input, n_vocab):
    """ Structural architecture layout configurations of the LSTM network. """
    model = Sequential()
    
    # Layer 1: LSTM layer to analyze input sequences
    model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
    model.add(Dropout(0.3)) # Prevents overfitting
    
    # Layer 2: Second LSTM layer for deeper pattern abstraction
    model.add(LSTM(256))
    model.add(Dropout(0.3))
    
    # Layer 3: Fully Connected Dense Layer mapping down to the categorical dimensions
    model.add(Dense(n_vocab))
    model.add(Activation('softmax')) # Outputs probability configurations

    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
    return model

# ==============================================================================
# PHASE 4: MUSIC SEED GENERATION
# ==============================================================================

def generate_notes(model, network_input, pitches, n_vocab, num_notes_to_gen=200):
    """ Uses a trained model to generate a raw numerical note array sequence. """
    # Re-extract integer maps
    note_to_int = {note: num for num, note in enumerate(pitches)}
    int_to_note = {num: note for num, note in enumerate(pitches)}

    # Pick a random starting point pattern from inputs as a composition seed
    start = np.random.randint(0, len(network_input)-1)
    pattern = list(network_input[start])
    # Ensure it's a flat list of integers rather than scaled array vectors
    pattern = [int(p * n_vocab) for p in pattern]

    prediction_output = []

    print(f"Generating {num_notes_to_gen} notes...")
    for note_index in range(num_notes_to_gen):
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        # Query model predictive outputs
        prediction = model.predict(prediction_input, verbose=0)
        index = np.argmax(prediction) # Find index item matching highest probability 
        
        result = int_to_note[index]
        prediction_output.append(result)

        # Shift sequence window down by appending output and trimming the oldest entry
        pattern.append(index)
        pattern = pattern[1:]

    return prediction_output

# ==============================================================================
# PHASE 5: CONVERT BACK TO MIDI & SAVE
# ==============================================================================

def save_midi(prediction_output, filename='output_song.mid'):
    """ Re-encodes string tracking variables back down to MIDI tracks. """
    offset = 0
    output_notes = []

    # Reconstruct structural data streams
    for pattern in prediction_output:
        # Pattern represents a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # Pattern represents a single isolated note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # Adjust offsets cleanly so elements don't stack on top of each other
        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp=filename)
    print(f"Success! Saved generated music to: {filename}")

# ==============================================================================
# PIPELINE EXECUTION DRIVER ENTRYPOINT
# ==============================================================================

if __name__ == '__main__':
    MIDI_FOLDER = "midi_songs"
    
    # 1. Pipeline initialization
    if not os.path.exists(MIDI_FOLDER):
        os.makedirs(MIDI_FOLDER)
        print(f"Created a folder named '{MIDI_FOLDER}'. Drop your training .mid tracks into it, then run again.")
    else:
        # Extract and parse
        raw_notes = get_notes_from_midi(MIDI_FOLDER)
        
        # Prepare tracking datasets
        X, y, pitches, vocab_len = prepare_sequences(raw_notes)
        
        # Initialize model layers
        ai_model = create_network(X, vocab_len)
        
        # Train model (using small epochs/batches as an initial baseline execution setup)
        print("Training model...")
        ai_model.fit(X, y, epochs=15, batch_size=64)
        
        # Generate new data patterns
        generated_melody = generate_notes(ai_model, X, pitches, vocab_len)
        
        # Map output structures
        save_midi(generated_melody, 'generated_composition.mid')
