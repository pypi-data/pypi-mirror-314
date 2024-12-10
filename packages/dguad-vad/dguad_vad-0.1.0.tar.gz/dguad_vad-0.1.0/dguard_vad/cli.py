# coding = utf-8
# @Time    : 2024-12-10  12:41:00
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: CLI for Dguard VAD.

import time
import wave
import click
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from dguard_vad import VAD, VADIterator

@click.command()
@click.argument("wav_path", type=click.Path(exists=True, file_okay=True))
@click.option("--denoise/--no-denoise", default=False, help="Denoise before vad")
@click.option("--streaming/--no-streaming", default=False, help="Streming mode")
@click.option("--save-path", help="Save path for output audio")
@click.option("--plot/--no-plot", default=False, help="Plot the vad probabilities")
def main(wav_path, version, denoise, streaming, save_path, plot):
    sample_rate = sf.info(wav_path).samplerate
    if not streaming:
        model = VAD(sample_rate, denoise=denoise)
        speech_timestamps = model.get_speech_timestamps(
            wav_path, return_seconds=True, save_path=save_path
        )
        print("[Dguard] None streaming result:", list(speech_timestamps))
        if plot:
            audio, sampling_rate = sf.read(wav_path, dtype=np.float32)
            x1 = np.arange(0, len(audio)) / sampling_rate
            outputs = list(model.get_speech_probs(wav_path))
            x2 = [i * 32 / 1000 for i in range(0, len(outputs))]
            plt.plot(x1, audio)
            plt.plot(x2, outputs)
            plt.show()
    else:
        print("[Dguard] Streaming result:", end=" ")
        audio, sampling_rate = sf.read(wav_path, dtype=np.float32)
        vad_iterator = VADIterator(sampling_rate)
        if save_path is not None:
            out_wav = wave.open(save_path, "w")
            out_wav.setnchannels(1)
            out_wav.setsampwidth(2)
            out_wav.setframerate(sampling_rate)
        # number of samples in a single audio chunk, 10ms per chunk
        window_size_samples = 10 * sampling_rate // 1000
        start_time = time.time()
        for i in range(0, len(audio), window_size_samples):
            chunk = audio[i : i + window_size_samples]
            is_last = i + window_size_samples >= len(audio)
            # print(chunk.shape)
            for speech_dict, speech_samples in vad_iterator(
                chunk, is_last, return_seconds=True
            ):
                if "start" in speech_dict or "end" in speech_dict:
                    print(speech_dict, end=" ")
                if save_path is not None and speech_samples is not None:
                    out_wav.writeframes((speech_samples * 32768).astype(np.int16))
        print(f"\nTime cost: {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    main()
