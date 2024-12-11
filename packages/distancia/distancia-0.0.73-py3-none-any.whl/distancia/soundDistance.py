from .mainClass import *
from .lossFunction import MeanSquaredError


import cmath
from typing import List, Tuple

class SpectralConvergence(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        """
        Compute the Spectral Convergence between two signals.

        :param signal1: The first signal as a list of floats.
        :param signal2: The second signal as a list of floats.
        :return: The spectral convergence between the two signals as a float.
        """
        # Compute the FFT for both signals
        fft1: List[complex] = Sound().FFT(signal1)
        fft2: List[complex] = Sound().FFT(signal2)

        # Compute magnitudes of the spectrums
        mag1: List[float] = Sound.magnitude(fft1)
        mag2: List[float] = Sound.magnitude(fft2)

        # Ensure both spectrums are of the same length
        if len(mag1) != len(mag2):
            raise ValueError("Both signals must have the same length.")

        # Compute the Spectral Convergence
        numerator: float = sum(abs(m1 - m2) for m1, m2 in zip(mag1, mag2))
        denominator: float = sum(mag1)

        # To avoid division by zero
        if denominator == 0:
            return float('inf')

        return numerator / denominator

import math
import cmath

class MFCCProcessor(Distance):
    def __init__(self, sample_rate: int = 16000, n_mfcc: int = 13, n_fft: int = 2048, n_mels: int = 26)-> None:
        super().__init__()
        self.type='sound'

        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.n_mels = n_mels

    def _mel_to_hz(self, mel: float) -> float:
        return 700 * (10 ** (mel / 2595) - 1)

    def _hz_to_mel(self, hz: float) -> float:
        return 2595 * math.log10(1 + hz / 700)

    def _mel_filterbank(self) -> List[List[float]]:
        low_freq_mel = self._hz_to_mel(0)
        high_freq_mel = self._hz_to_mel(self.sample_rate / 2)
        mel_points = [low_freq_mel + i * (high_freq_mel - low_freq_mel) / (self.n_mels + 1) for i in range(self.n_mels + 2)]
        hz_points = [self._mel_to_hz(mel) for mel in mel_points]
        bin_points = [int(round((self.n_fft + 1) * hz / self.sample_rate)) for hz in hz_points]

        fbank = [[0.0] * (self.n_fft // 2 + 1) for _ in range(self.n_mels)]
        for m in range(1, self.n_mels + 1):
            f_m_minus = bin_points[m - 1]
            f_m = bin_points[m]
            f_m_plus = bin_points[m + 1]

            for k in range(f_m_minus, f_m):
                fbank[m-1][k] = (k - f_m_minus) / (f_m - f_m_minus)
            for k in range(f_m, f_m_plus):
                fbank[m-1][k] = (f_m_plus - k) / (f_m_plus - f_m)

        return fbank

    def _dct(self, x: List[float]) -> List[float]:
        N = len(x)
        y = [0.0] * N
        for k in range(N):
            for n in range(N):
                y[k] += x[n] * math.cos(math.pi * k * (2 * n + 1) / (2 * N))
        return y

    def compute(self, signal1: List[float], signal2: List[float]) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Calcule les MFCC pour deux signaux audio.

        Args:
            signal1 (List[float]): Premier signal audio.
            signal2 (List[float]): Deuxième signal audio.

        Returns:
            Tuple[List[List[float]], List[List[float]]]: MFCC des deux signaux.
        """
        def process_signal(signal: List[float]) -> List[List[float]]:
            # Pré-accentuation
            pre_emphasis = 0.97
            emphasized_signal = [signal[i] - pre_emphasis * signal[i-1] for i in range(1, len(signal))]

            # Fenêtrage
            frame_length = self.n_fft
            frame_step = frame_length // 2
            frames = [emphasized_signal[i:i+frame_length] for i in range(0, len(emphasized_signal) - frame_length + 1, frame_step)]

            # Appliquer la fenêtre de Hamming
            hamming = [0.54 - 0.46 * math.cos(2 * math.pi * i / (frame_length - 1)) for i in range(frame_length)]
            windowed_frames = [[frame[i] * hamming[i] for i in range(len(frame))] for frame in frames]

            # FFT
            magnitude_frames = [[abs(x) for x in Sound().FFT(frame)] for frame in windowed_frames]

            # Mel filterbank
            mel_fb = self._mel_filterbank()
            mel_spectrum = [[sum(m * f for m, f in zip(mel_filter, frame[:len(mel_filter)])) for mel_filter in mel_fb] for frame in magnitude_frames]

            # Log
            log_mel_spectrum = [[math.log(x + 1e-8) for x in frame] for frame in mel_spectrum]

            # DCT
            mfcc = [self._dct(frame)[:self.n_mfcc] for frame in log_mel_spectrum]

            return mfcc

        mfcc1 = process_signal(signal1)
        mfcc2 = process_signal(signal2)

        return mfcc1, mfcc2

    def compare_mfcc(self, signal1: List[float], signal2: List[float]) -> List[float]:
        """
        Calcule et compare les MFCC de deux signaux audio.

        Args:
            signal1 (List[float]): Premier signal audio.
            signal2 (List[float]): Deuxième signal audio.

        Returns:
            List[float]: Distance euclidienne moyenne entre les MFCC des deux signaux.
        """
        mfcc1, mfcc2 = self.compute(signal1, signal2)

        # Assurez-vous que les deux MFCC ont le même nombre de trames
        min_frames = min(len(mfcc1), len(mfcc2))
        mfcc1 = mfcc1[:min_frames]
        mfcc2 = mfcc2[:min_frames]

        # Calculez la distance euclidienne moyenne
        distances = []
        for frame1, frame2 in zip(mfcc1, mfcc2):
            distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(frame1, frame2)))
            distances.append(distance)

        return sum(distances) / len(distances)
        
    def example(self):

      # Générer les signaux de test
      test_signal1, test_signal2 = Sound.generate_test_signals()

      # Afficher les 10 premiers échantillons de chaque signal
      print("10 premiers échantillons du signal 1:", test_signal1[:10])
      print("10 premiers échantillons du signal 2:", test_signal2[:10])

      print(f"Nombre d'échantillons dans chaque signal: {len(test_signal1)}")
      print(f"Fréquence d'échantillonnage: 16000 Hz")
      print(f"Durée de chaque signal: 1.0 seconde")


      # Créer une instance de MFCCProcessor
      processor = MFCCProcessor()

      # Calculer les MFCC pour les deux signaux
      mfcc1, mfcc2 = processor.compute(test_signal1, test_signal2)

      # Comparer les MFCC
      distance = processor.compare_mfcc(test_signal1, test_signal2)

      print(f"Nombre de trames MFCC pour chaque signal: {len(mfcc1)}")
      print(f"Nombre de coefficients MFCC par trame: {len(mfcc1[0])}")
      print(f"Distance moyenne entre les MFCC des deux signaux: {distance}")

      # Afficher les premiers coefficients MFCC de la première trame pour chaque signal
      print("Premiers coefficients MFCC du signal 1:", mfcc1[0][:5])
      print("Premiers coefficients MFCC du signal 2:", mfcc2[0][:5])
      
#claude ai fft
'''
from typing import List
import cmath

class SignalProcessor(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _fft(self, signal: List[float]) -> List[complex]:
        """
        Calcule la Transformée de Fourier Rapide (FFT) d'un signal sonore.

        Args:
            signal (List[float]): Le signal d'entrée sous forme de liste de nombres flottants.

        Returns:
            List[complex]: La FFT du signal sous forme de liste de nombres complexes.
        """
        n = len(signal)
        if n <= 1:
            return signal

        # Diviser le signal en pair et impair
        even = self._fft(signal[0::2])
        odd = self._fft(signal[1::2])

        # Combiner
        combined = [0] * n
        for k in range(n // 2):
            t = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
            combined[k] = even[k] + t
            combined[k + n // 2] = even[k] - t

        return combined

    @staticmethod
    def pad_to_power_of_two(signal: List[float]) -> List[float]:
        """
        Complète le signal avec des zéros pour atteindre une longueur qui est une puissance de 2.

        Args:
            signal (List[float]): Le signal d'entrée.

        Returns:
            List[float]: Le signal complété.
        """
        n = 1
        while n < len(signal):
            n *= 2
        return signal + [0.0] * (n - len(signal))

processor = SignalProcessor()
signal1 = [0.1, 0.2, 0.3, 0.4, 0.5]  # exemple de signal
signal2 = [0.2, 0.3, 0.4, 0.5, 0.6]  # autre exemple de signal
fft_difference = processor._fft(signal1)
print(fft_difference)
'''
##############"
import math
from typing import List

class PowerSpectralDensityDistance(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate = sample_rate

    def _psd(self, signal: List[float]) -> List[float]:
        fft_result = Sound().FFT(signal)
        magnitude_spectrum = [abs(freq) ** 2 for freq in fft_result[:len(fft_result) // 2]]
        return magnitude_spectrum

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        psd1 = self._psd(signal1)
        psd2 = self._psd(signal2)

        distance = sum((psd1[i] - psd2[i]) ** 2 for i in range(min(len(psd1), len(psd2))))
        return math.sqrt(distance)
    def example(self):
      test_signal1, test_signal2 = Sound.generate_test_signals()
      psd_calculator = PowerSpectralDensityDistance(sample_rate=16000)
      psd_distance = psd_calculator.compute(test_signal1, test_signal2)
      print("PSD Distance:", psd_distance)
      
import math
from typing import List

class CrossCorrelation(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _mean(self, signal: List[float]) -> float:
        return sum(signal) / len(signal)

    def _normalize(self, signal: List[float]) -> List[float]:
        mean_value: float = self._mean(signal)
        return [x - mean_value for x in signal]

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        signal1_normalized: List[float] = self._normalize(signal1)
        signal2_normalized: List[float] = self._normalize(signal2)

        numerator: float = sum(signal1_normalized[i] * signal2_normalized[i] for i in range(min(len(signal1_normalized), len(signal2_normalized))))
        denominator_signal1: float = math.sqrt(sum(x ** 2 for x in signal1_normalized))
        denominator_signal2: float = math.sqrt(sum(x ** 2 for x in signal2_normalized))

        denominator: float = denominator_signal1 * denominator_signal2

        return numerator / denominator if denominator != 0 else 0.0
        
#ai claude

from typing import List, Tuple
import math
import cmath

class PhaseDifferenceCalculator(Distance):

    def __init__(self, sample_rate: int=16000, window_size: int= 1024, hop_size: int=512) -> None:
        """
        Initialise le calculateur de différence de phase.

        Args:
            sample_rate (int): Taux d'échantillonnage des signaux.
            window_size (int): Taille de la fenêtre pour l'analyse.
            hop_size (int): Taille du saut entre les fenêtres successives.
        """
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate
        self.window_size: int = window_size
        self.hop_size: int = hop_size


    '''
    def _fft(self, signal: List[float]) -> List[complex]:
        """
        Calcule la Transformée de Fourier Rapide (FFT) du signal.

        Args:
            signal (List[float]): Signal d'entrée.

        Returns:
            List[complex]: FFT du signal.
        """
        n: int = len(signal)
        if n <= 1:
            return signal
        even: List[complex] = self._fft(signal[0::2])
        odd: List[complex] = self._fft(signal[1::2])
        combined: List[complex] = [0] * n
        for k in range(n // 2):
            t: complex = cmath.exp(-2j * math.pi * k / n) * odd[k]
            combined[k] = even[k] + t
            combined[k + n // 2] = even[k] - t
        return combined
    '''
    def compute(self, signal1: List[float], signal2: List[float]) -> List[float]:
        """
        Calcule la différence de phase entre deux signaux.

        Args:
            signal1 (List[float]): Premier signal.
            signal2 (List[float]): Deuxième signal.

        Returns:
            List[float]: Différence de phase pour chaque segment.
        """
        if len(signal1) != len(signal2):
            raise ValueError("Les signaux doivent avoir la même longueur")

        phase_differences: List[float] = []
        num_segments: int = (len(signal1) - self.window_size) // self.hop_size + 1

        for i in range(num_segments):
            start: int = i * self.hop_size
            end: int = start + self.window_size

            segment1: List[float] = Sound._apply_window(signal1[start:end])
            segment2: List[float] = Sound._apply_window(signal2[start:end])

            fft1: List[complex] = Sound().FFT(segment1)
            fft2: List[complex] = Sound().FFT(segment2)

            phase_diff: float = 0
            for f1, f2 in zip(fft1, fft2):
                if abs(f1) > 1e-6 and abs(f2) > 1e-6:  # Éviter la division par zéro
                    phase1: float = cmath.phase(f1)
                    phase2: float = cmath.phase(f2)
                    diff: float = phase2 - phase1
                    # Normaliser la différence de phase entre -pi et pi
                    phase_diff += (diff + math.pi) % (2 * math.pi) - math.pi

            phase_differences.append(phase_diff / len(fft1))

        return phase_differences

    def get_time_axis(self) -> List[float]:
        """
        Génère l'axe temporel pour les différences de phase calculées.

        Returns:
            List[float]: Axe temporel en secondes.
        """
        num_segments: int = len(self.compute([0] * self.window_size, [0] * self.window_size))
        return [i * self.hop_size / self.sample_rate for i in range(num_segments)]

    def analyze_signals(self, signal1: List[float], signal2: List[float]) -> Tuple[List[float], List[float]]:
        """
        Analyse deux signaux et retourne la différence de phase et l'axe temporel.

        Args:
            signal1 (List[float]): Premier signal.
            signal2 (List[float]): Deuxième signal.

        Returns:
            Tuple[List[float], List[float]]: Différence de phase et axe temporel.
        """
        phase_diff: List[float] = self.compute(signal1, signal2)
        time_axis: List[float] = self.get_time_axis()
        return phase_diff, time_axis
        
    def example(self):
      # Paramètres
      sample_rate: int = 44100  # Hz
      window_size: int = 1024   # échantillons
      hop_size: int = 512       # échantillons

      # Créer une instance du calculateur
      calculator: PhaseDifferenceCalculator = PhaseDifferenceCalculator(sample_rate, window_size, hop_size)

      # Supposons que nous ayons deux signaux signal1 et signal2
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 880 * t / 16000) for t in range(16000)]

      # Analyser les signaux
      phase_differences: List[float]
      time_axis: List[float]
      phase_differences, time_axis = calculator.analyze_signals(signal1, signal2)

      # Afficher les résultats
      print("Différences de phase:", phase_differences[:10])  # Affiche les 10 premières valeurs
      print("Axe temporel:", time_axis[:10])  # Affiche les 10 premières valeurs
      
from typing import List
import math

class TimeLagDistance(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _cross_correlation(self, signal1: List[float], signal2: List[float], lag: int) -> float:
        n: int = len(signal1)
        if lag > 0:
            shifted_signal2: List[float] = [0] * lag + signal2[:-lag]
        else:
            shifted_signal2: List[float] = signal2[-lag:] + [0] * (-lag)

        return sum(signal1[i] * shifted_signal2[i] for i in range(n))

    def compute(self, signal1: List[float], signal2: List[float], max_lag: int) -> int:
        best_lag: int = 0
        best_correlation: float = -float('inf')

        for lag in range(-max_lag, max_lag + 1):
            correlation: float = self._cross_correlation(signal1, signal2, lag)
            if correlation > best_correlation:
                best_correlation = correlation
                best_lag = lag

        return best_lag
    def example(self):
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 440 * (t - 100) / 16000) for t in range(16000)]  # signal2 is shifted

      time_lag_calculator = TimeLagDistance(sample_rate=16000)

      best_lag: int = time_lag_calculator.compute(signal1, signal2, max_lag=500)

      print("Optimal time lag:", best_lag)
      
from typing import List

class PESQ(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _preprocess(self, signal: List[float]) -> List[float]:
        # Placeholder preprocessing steps: normalization and filtering
        max_val: float = max(abs(x) for x in signal)
        return [x / max_val for x in signal] if max_val != 0 else signal

    def _compare_signals(self, reference: List[float], degraded: List[float]) -> float:
        # Placeholder function to simulate signal comparison
        mse: float = sum((reference[i] - degraded[i]) ** 2 for i in range(min(len(reference), len(degraded))))
        return mse / len(reference)

    def compute(self, reference_signal: List[float], degraded_signal: List[float]) -> float:
        reference_processed: List[float] = self._preprocess(reference_signal)
        degraded_processed: List[float] = self._preprocess(degraded_signal)

        comparison_score: float = self._compare_signals(reference_processed, degraded_processed)

        # Placeholder formula for PESQ score (the actual PESQ model is more complex)
        pesq_score: float = 4.5 - comparison_score  # 4.5 is the best score in PESQ scale

        return max(1.0, min(pesq_score, 4.5))  # PESQ scores typically range between 1.0 and 4.5
        
        
import cmath
from typing import List

class LogSpectralDistance(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _log_magnitude_spectrum(self, signal: List[float]) -> List[float]:
        fft_result: List[complex] = Sound().FFT(signal)
        return [20 * math.log10(abs(x)) if abs(x) != 0 else 0 for x in fft_result]

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        log_spectrum1: List[float] = self._log_magnitude_spectrum(signal1)
        log_spectrum2: List[float] = self._log_magnitude_spectrum(signal2)

        # Calculate the squared differences between the log-magnitude spectra
        squared_diffs: List[float] = [(log_spectrum1[i] - log_spectrum2[i]) ** 2 for i in range(min(len(log_spectrum1), len(log_spectrum2)))]

        # Compute the LSD value
        mean_squared_diff: float = sum(squared_diffs) / len(squared_diffs)
        return math.sqrt(mean_squared_diff)
        
import math
from typing import List

class BarkSpectralDistortion(Distance):

    def __init__(self, sample_rate: int=16000) -> None:
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate

    def _bark_scale(self, freq: float) -> float:
        return 13 * math.atan(0.00076 * freq) + 3.5 * math.atan((freq / 7500) ** 2)

    def _compute_bark_spectrum(self, signal: List[float]) -> List[float]:
        fft_result: List[complex] = Sound().FFT(signal)
        N: int = len(fft_result)
        bark_spectrum: List[float] = [0.0] * N

        for i in range(N):
            freq: float = i * (self.sample_rate / N)
            bark_freq: float = self._bark_scale(freq)
            magnitude: float = abs(fft_result[i])
            bark_spectrum[i] = 20 * math.log10(magnitude) if magnitude != 0 else 0

        return bark_spectrum

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        bark_spectrum1: List[float] = self._compute_bark_spectrum(signal1)
        bark_spectrum2: List[float] = self._compute_bark_spectrum(signal2)

        squared_diffs: List[float] = [(bark_spectrum1[i] - bark_spectrum2[i]) ** 2 for i in range(min(len(bark_spectrum1), len(bark_spectrum2)))]

        mean_squared_diff: float = sum(squared_diffs) / len(squared_diffs)
        return math.sqrt(mean_squared_diff)

import math
from typing import List

class ItakuraSaitoDistance(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _power_spectrum(self, signal: List[float]) -> List[float]:
        N: int = len(signal)
        power_spectrum: List[float] = [0.0] * N

        for i in range(N):
            power_spectrum[i] = signal[i] ** 2
        
        return power_spectrum

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        power_spectrum1: List[float] = self._power_spectrum(signal1)
        power_spectrum2: List[float] = self._power_spectrum(signal2)
        
        is_distance: float = 0.0
        for ps1, ps2 in zip(power_spectrum1, power_spectrum2):
            if ps2 > 0:
                is_distance += (ps1 / ps2) - math.log(ps1 / ps2) - 1
        
        return is_distance
        
import math
from typing import List

class SignalToNoiseRatio(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _power(self, signal: List[float]) -> float:
        power: float = sum(s ** 2 for s in signal) / len(signal)
        return power

    def compute(self, signal: List[float], noise: List[float]) -> float:
        if len(signal) != len(noise):
            raise ValueError("Signal and noise must have the same length.")

        signal_power: float = self._power(signal)
        noise_power: float = self._power(noise)

        if noise_power == 0:
            raise ValueError("Noise power is zero, cannot compute SNR.")

        snr: float = 10 * math.log10(signal_power / noise_power)
        return snr


import math

class PeakSignalToNoiseRatio(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def compute(self, signal1: List[float], signal2: List[float], max_signal_value: float) -> float:
        mse: float = MeanSquaredError().compute(signal1, signal2)
        if mse == 0:
            return float('inf')  # Signals are identical

        psnr: float = 10 * math.log10(max_signal_value ** 2 / mse)
        return psnr
        
    def example(self):
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 445 * t / 16000) for t in range(16000)]  # Slightly different frequency

      max_signal_value: float = 1.0  # Maximum possible value for a normalized signal

      psnr_value: float = self.compute(signal1, signal2, max_signal_value)

      print("Peak Signal-to-Noise Ratio (PSNR):", psnr_value)

class EnergyDistance(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _energy(self, signal: List[float]) -> float:
        energy: float = sum(s ** 2 for s in signal)
        return energy

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        energy1: float = self._energy(signal1)
        energy2: float = self._energy(signal2)

        energy_distance: float = abs(energy1 - energy2)
        return energy_distance
        
class EnvelopeCorrelation(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _envelope(self, signal: List[float]) -> List[float]:
        # Approximation of the envelope using the absolute value of the signal
        envelope: List[float] = [abs(s) for s in signal]
        return envelope

    def _mean(self, data: List[float]) -> float:
        return sum(data) / len(data)

    def _correlation(self, envelope1: List[float], envelope2: List[float]) -> float:
        mean1: float = self._mean(envelope1)
        mean2: float = self._mean(envelope2)

        numerator: float = sum((e1 - mean1) * (e2 - mean2) for e1, e2 in zip(envelope1, envelope2))
        denominator: float = math.sqrt(sum((e1 - mean1) ** 2 for e1 in envelope1) * sum((e2 - mean2) ** 2 for e2 in envelope2))

        if denominator == 0:
            return 0.0  # No correlation if denominator is zero

        return numerator / denominator

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        envelope1: List[float] = self._envelope(signal1)
        envelope2: List[float] = self._envelope(signal2)

        correlation: float = self._correlation(envelope1, envelope2)
        return correlation
        
class ZeroCrossingRateDistance(Distance):

    def __init__(self) -> None:
        super().__init__()
        self.type='sound'

    def _zero_crossing_rate(self, signal: List[float]) -> float:
        zero_crossings: int = 0
        for i in range(1, len(signal)):
            if (signal[i - 1] > 0 and signal[i] < 0) or (signal[i - 1] < 0 and signal[i] > 0):
                zero_crossings += 1

        zcr: float = zero_crossings / len(signal)
        return zcr

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        zcr1: float = self._zero_crossing_rate(signal1)
        zcr2: float = self._zero_crossing_rate(signal2)

        zcr_distance: float = abs(zcr1 - zcr2)
        return zcr_distance
        
class CochleagramDistance(Distance):

    def __init__(self, num_bands: int = 40)-> None:
        super().__init__()
        self.type='sound'

        self.num_bands: int = num_bands

    def _bandpass_filter(self, signal: List[float], band_index: int, total_bands: int) -> List[float]:
        # Simplified bandpass filter approximation
        filtered_signal: List[float] = [0.0] * len(signal)
        band_width: float = 0.5 / total_bands
        center_freq: float = (band_index + 0.5) * band_width
        for i in range(len(signal)):
            filtered_signal[i] = signal[i] * center_freq  # Simplified filter effect
        return filtered_signal

    def _cochleagram(self, signal: List[float]) -> List[List[float]]:
        cochleagram: List[List[float]] = []
        for band in range(self.num_bands):
            band_signal: List[float] = self._bandpass_filter(signal, band, self.num_bands)
            cochleagram.append(band_signal)
        return cochleagram

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        cochlea1: List[List[float]] = self._cochleagram(signal1)
        cochlea2: List[List[float]] = self._cochleagram(signal2)

        distance: float = Sound._mean_squared_error(cochlea1, cochlea2)
        return distance


from typing import List
import math

class ChromagramDistance(Distance):

    def __init__(self, num_bins: int = 12) -> None:
        super().__init__()
        self.type='sound'

        self.num_bins: int = num_bins

    def _frequency_to_bin(self, frequency: float) -> int:
        # Simple mapping of frequency to chroma bin
        if frequency>0:
           bin_index: int = int((12 * math.log2(frequency / 440.0) + 69) % 12)
           return bin_index
        else:
           return 0


    def _compute_chromagram(self, signal: List[float]) -> List[float]:
        chroma: List[float] = [0.0] * self.num_bins
        for sample in signal:
            # Simplified frequency estimation from signal sample (placeholder)
            frequency: float = abs(sample) * 1000.0
            bin_index: int = self._frequency_to_bin(frequency)
            chroma[bin_index] += 1

        # Normalize chromagram
        total_count: float = sum(chroma)
        if total_count > 0:
            chroma = [count / total_count for count in chroma]

        return chroma

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        chroma1: List[float] = self._compute_chromagram(signal1)
        chroma2: List[float] = self._compute_chromagram(signal2)

        distance: float = MeanSquaredError().compute(chroma1, chroma2)
        return distance

import cmath

class SpectrogramDistance(Distance):

    def __init__(self, window_size: int = 256, overlap: int = 128) -> None:
        super().__init__()
        self.type='sound'

        self.window_size: int = window_size
        self.overlap: int = overlap

    def _dft(self, signal: List[float]) -> List[complex]:
        N: int = len(signal)
        return [sum(signal[n] * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N)) for k in range(N)]

    def _spectrogram(self, signal: List[float]) -> List[List[float]]:
        step: int = self.window_size - self.overlap
        spectrogram: List[List[float]] = []

        for start in range(0, len(signal) - self.window_size + 1, step):
            windowed_signal: List[float] = signal[start:start + self.window_size]
            dft_result: List[complex] = self._dft(windowed_signal)
            magnitude: List[float] = [abs(freq) for freq in dft_result]
            spectrogram.append(magnitude)

        return spectrogram


    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        spectrogram1: List[List[float]] = self._spectrogram(signal1)
        spectrogram2: List[List[float]] = self._spectrogram(signal2)
        distance: float = Sound._mean_squared_error(spectrogram1, spectrogram2)
        return distance
        
    def example(self):
			
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 445 * t / 16000) for t in range(16000)]  # Slightly different frequency

      spectrogram_calculator = SpectrogramDistance(window_size=256, overlap=128)

      distance_value: float = spectrogram_calculator.compute(signal1, signal2)

      print("Spectrogram Distance:", distance_value)

import cmath

class CQTDistance(Distance):

    def __init__(self, num_bins: int = 24, window_size: int = 512) -> None:
        super().__init__()
        self.type='sound'

        self.num_bins: int = num_bins
        self.window_size: int = window_size

    def _dft(self, signal: List[float]) -> List[complex]:
        N: int = len(signal)
        return [sum(signal[n] * cmath.exp(-2j * cmath.pi * k * n / N) for n in range(N)) for k in range(N)]

    def _cqt(self, signal: List[float]) -> List[List[float]]:
        step: int = self.window_size
        cqt_matrix: List[List[float]] = []

        for start in range(0, len(signal) - self.window_size + 1, step):
            windowed_signal: List[float] = signal[start:start + self.window_size]
            dft_result: List[complex] = self._dft(windowed_signal)

            # Compute magnitude and split into bins
            magnitude: List[float] = [abs(freq) for freq in dft_result]
            cqt_bins: List[float] = [sum(magnitude[i] for i in range(self.num_bins))]  # Simplified CQT binning
            cqt_matrix.append(cqt_bins)

        return cqt_matrix

    def compute(self, signal1: List[float], signal2: List[float]) -> float:
        if len(signal1) != len(signal2):
            raise ValueError("Both signals must have the same length.")

        cqt1: List[List[float]] = self._cqt(signal1)
        cqt2: List[List[float]] = self._cqt(signal2)

        distance: float = Sound._mean_squared_error(cqt1, cqt2)
        return distance
    def example(self):
      signal1: List[float] = [0.1 * math.sin(2 * math.pi * 440 * t / 16000) for t in range(16000)]
      signal2: List[float] = [0.1 * math.sin(2 * math.pi * 445 * t / 16000) for t in range(16000)]  # Slightly different frequency

      cqt_calculator = CQTDistance(num_bins=24, window_size=512)

      distance_value: float = cqt_calculator.compute(signal1, signal2)

      print("CQT Distance:", distance_value)
      
import wave
from typing import Tuple

class CepstralDistance(Distance):

    def __init__(self, sample_rate: int = 16000, frame_size: int = 512, num_coefficients: int = 13) -> None:
        """
        Initializes the CepstralDistance class with the specified parameters.
        
        :param sample_rate: The sampling rate of the audio signal.
        :param frame_size: The size of each frame used for analysis.
        :param num_coefficients: The number of cepstral coefficients to extract.
        """
        super().__init__()
        self.type='sound'

        self.sample_rate: int = sample_rate
        self.frame_size: int = frame_size
        self.num_coefficients: int = num_coefficients



    def compute_cepstral_coefficients(self, signal: List[float]) -> List[float]:
        """
        Computes the cepstral coefficients of a given audio signal.
        
        :param signal: The input audio signal as a list of floats.
        :return: The cepstral coefficients as a list of floats.
        """
        # Compute the power spectrum (simplified for the example)
        power_spectrum: List[float] = [math.log(abs(s)) for s in signal if s!=0]

        # Apply the inverse Fourier transform to obtain cepstral coefficients
        cepstrum: List[float] = self.inverse_fft(power_spectrum)

        # Return only the first 'num_coefficients' coefficients
        return cepstrum[:self.num_coefficients]



    def compute(self, cepstral_1: List[float], cepstral_2: List[float]) -> float:
        """
        Computes the Euclidean distance between two sets of cepstral coefficients.
        
        :param cepstral_1: The first set of cepstral coefficients.
        :param cepstral_2: The second set of cepstral coefficients.
        :return: The cepstral distance as a float.
        """
        return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(cepstral_1, cepstral_2)))

    def compute_cepstral_distance(self, file1: str, file2: str) -> float:
        """
        Computes the Cepstral Distance between two audio files.
        
        :param file1: Path to the first audio file.
        :param file2: Path to the second audio file.
        :return: The Cepstral Distance as a float.
        """
        audio_data_1, sample_rate_1 = Sound.read_audio(file1)
        audio_data_2, sample_rate_2 = Sound.read_audio(file2)

        if sample_rate_1 != sample_rate_2:
            raise ValueError("Sample rates of the two audio files must be the same.")

        cepstral_1: List[float] = self.compute_cepstral_coefficients(audio_data_1)
        cepstral_2: List[float] = self.compute_cepstral_coefficients(audio_data_2)

        distance: float = self.calculate_distance(cepstral_1, cepstral_2)
        return distance

'''
les fichier ont été générés

if __name__ == "__main__":
    # Generate two different sine wave signals
    duration: float = 2.0  # seconds

    sine_wave1 = generate_sine_wave(frequency=440.0, duration=duration)  # A4 note (440 Hz)
    sine_wave2 = generate_sine_wave(frequency=523.25, duration=duration)  # C5 note (523.25 Hz)

    # Save the generated sine waves to two .wav files
    save_wave("../sample/audio1.wav", sine_wave1)
    save_wave("../sample/audio2.wav", sine_wave2)

    print("Two audio files 'audio1.wav' and 'audio2.wav' have been generated.")
'''
if __name__ == "__main__":
    # Example usage
    file1: str = "../sample/audio1.wav"
    file2: str = "../sample/audio2.wav"

    cepstral_distance_calculator = CepstralDistance()
    distance: float = cepstral_distance_calculator.compute_cepstral_distance(file1, file2)

    print(f"Cepstral Distance: {distance}")
