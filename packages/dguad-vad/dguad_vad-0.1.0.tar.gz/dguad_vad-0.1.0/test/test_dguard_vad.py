from dguard_vad import VAD, VADIterator

SR = 16000
WAV_PATH = "../data/test_16k.wav"
# Test the VAD class
def test_vad():
    vad = VAD(SR)
    timestamps = vad.get_speech_timestamps(WAV_PATH)
    for _ in timestamps:
        print(_)
    
    # {'segment': 0, 'start': 26560, 'end': 48704}
    # {'segment': 1, 'start': 71616, 'end': 106048}
    # {'segment': 2, 'start': 149952, 'end': 185920}
    
    probs = vad.get_speech_probs(WAV_PATH)
    for _ in probs:
        print(_)
    # 0.02
    # 0.01
    # 0.01
    # 0.01
    # 0.0
    print("VAD class is working correctly.")

def test_vad_iterator():
    vad_iterator = VADIterator(16000)
    assert vad_iterator is not None, "VADIterator class is not initialized correctly."
    # Test the __call__ method
    for speech_dict, speech_samples in vad_iterator("../data/test_16k.wav"):
        print(speech_dict, speech_samples)
    print("VADIterator class is working correctly.")

if __name__ == "__main__":
    test_vad()
    # test_vad_iterator()