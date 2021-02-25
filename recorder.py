import sounddevice
from scipy.io.wavfile import write
import soundfile as sf
import numpy as np

class recorder:

    def print_sound(self, indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        print(str(int(volume_norm)) + " | ")
        print ("*" * int(volume_norm), end='\r')

    def record(self, fs, second, filename):
        # fs = 44100
        # second = 5

        print("recording...")

        with sounddevice.Stream(callback=self.print_sound):
            record_voice = sounddevice.rec(int(second * fs), samplerate=fs, channels=2)
            sounddevice.wait()

        write(filename, fs, record_voice)

        print("berhasil direkam")

        # Extract data and sampling rate from file
        data, fs = sf.read(filename, dtype='float32')
        sounddevice.play(data, fs)
        sounddevice.wait()

    def play_rec(self, filename):
        try:
            data, fs = sf.read(filename, dtype='float32')
            sounddevice.play(data, fs)
            status = sounddevice.wait()
        except KeyboardInterrupt:
            print('\nInterrupted by user')
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))
        if status:
            print('Error during playback: ' + str(status))

if __name__ == '__main__':

    confirm_text = ['y', 'n']

    rc = recorder()
    filename = "output.wav"
    confirm = ""
    while confirm not in confirm_text:
        confirm = input("Apakah ingin merekam suara ? y/n ")
        if confirm == 'y':
            rc.record(44100, 5, filename)
            listen = ""
            while listen not in confirm_text:
                listen = input("Apakah ingin mendengar lagi? y/n ")
                if listen == 'y':
                    listen = ""
                    rc.play_rec(filename)

            confirm_record = ""
            while confirm_record not in confirm_text:
                confirm_record = input("Apakah ingin menggunakan sample ini? y/n ")
                if confirm_record == 'y':
                    print("oke sip")
                else:
                    confirm = ""
        elif confirm == 'n':
            get_sample = input("Masukan sample path : ")
            break




