import csv
import math
import argparse
from pathlib import Path
from random import sample
from datetime import timedelta
from matplotlib.colors import ListedColormap
from librosa.feature.inverse import mel_to_audio
from librosa.display import waveshow
from matplotlib import pyplot as plt
import soundfile as sf
import numpy as np


def vectorize_transcript(lines, start_time, end_time):
    duration = (end_time - start_time)
    output = np.zeros(
        math.ceil(duration.total_seconds()*1000), dtype=bool
    )
    for line in lines:
        t0, t1 = [
            line["start_time"], line["end_time"]
        ]
        x0, x1 = [
            math.floor((t - start_time).total_seconds()*1000)
            for t in (t0, t1)
        ]
        output[x0:x1] = True
    return output


def load_labels(label_root, file_id, start_time, end_time):
    label_path = label_root / f"{file_id}.csv"
    fields = ["start", "end", "label"]
    lines = []
    with open(label_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter='\t', fieldnames=fields):
            t0, t1 = [
                timedelta(seconds=float(s)) for s in (row["start"], row["end"])
            ]
            if t1 < start_time or t0 >= end_time:
                continue
            if row["label"] != "s":
                continue
            lines.append({
                "start_time": t0,
                "end_time": t1
            })
    return vectorize_transcript(lines, start_time, end_time)


def load_mel_files(
    root, transpose, sample_rate, hop_length,
    file_ids=[], language="en", genre="Documentaries",
    segment_seconds=10, fraction_per_source=1
):
    # Path to the input CSV file
    mel_root = root / "mel_features"
    csv_path = root / "TVSM-test_metadata.csv"
    
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=','):
            file_id = int(row['file_id'])
            if len(file_ids) != 0:
                if file_id not in file_ids:
                    continue
            elif row["genre"] != genre:
                continue
            elif row["language"] != language:
                continue
            mel_file = mel_root / f"{file_id}.npy"
            if not mel_file.is_file():
                continue
            # load the file
            mel = np.load(mel_file)
            mel = mel.T if transpose else mel
            n_seconds = round(
                mel.shape[1]*hop_length / sample_rate
            )
            # Break 5 minutes into 10 second clips
            n_samples = n_seconds//segment_seconds
            clip_times = sorted(sample(
                range(n_samples), round(
                    min(max(fraction_per_source,0),1)*n_samples
                )
            ))
            for offset in clip_times:
                start_time, end_time = [
                    i * segment_seconds for i in (offset, offset+1)
                ]
                start_hop, end_hop = [
                    t * sample_rate // hop_length
                    for t in (start_time, end_time)
                ]
                mel_clip = mel[:, start_hop:end_hop]
                labels = load_labels(
                    root / "labels", file_id, 
                    timedelta(seconds=start_time),
                    timedelta(seconds=end_time)
                )
                # Return filename and mel spectrogram
                yield f'{file_id}-{offset}', mel_clip, labels


class Parameters:
    '''
    github.com/biboamy/TVSM-dataset/blob/master/training_code/parameters.yaml
    '''
    n_fft=1024
    hop_length=512
    win_length=1024
    sample_rate=16000
    clip_seconds=60
    fraction_per_source=1
    file_ids=[]
    language="en"
    genre="Documentaries"

    def __init__(self, font_size, family):
        self.color = 'w'
        self.n_xticks = 3
        self.rc_font = {
            'size': font_size, 'family': family
        }


class Plotter:
    def __init__(self, audio, label_dict, parameters):
        plt.rc('font', **parameters.rc_font)
        self.clip_seconds = parameters.clip_seconds
        self.sample_rate = parameters.sample_rate
        self.n_xticks = parameters.n_xticks
        self.n_lists = len(label_dict)
        self.label_dict = label_dict
        self.color = parameters.color
        self.audio = audio
        self.gridspec_kw = {
            'height_ratios': [
                *(1,)*self.n_lists, 4
            ],
            'wspace':0, 'hspace':0
        }

    def __enter__(self):
        label_dict = self.label_dict
        fig, (*axes, ax1) = plt.subplots(
            1+self.n_lists, gridspec_kw=self.gridspec_kw,
            layout="constrained", figsize=(8, 3), sharex=True
        )
        cmap = ListedColormap([(0,0,0,0), 'w'])
        extent = [0, self.clip_seconds, -2/3, 2/3]
        waveshow(self.audio, sr=self.sample_rate, color=self.color, ax=ax1)
        for ax, y in zip(axes, label_dict.values()):
            ax.imshow(
                y[np.newaxis,:], cmap=cmap,
                aspect="auto", extent=extent
            )
        for ax in (*axes, ax1):
            ax.tick_params(axis='x', colors=self.color)
            ax.spines['bottom'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.tick_params(length=0)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlabel("")
            ax.set_ylabel("")
        for ax, label in zip(axes, label_dict.keys()):
            ax.set_title(label, color=self.color)
        # Add labels to x axis
        xticks = np.linspace(0, self.clip_seconds, self.n_xticks)
        xlabels = [ f'{x:.0f} seconds' for x in xticks ]
        ax1.set_xticks(xticks, labels=xlabels)
        return fig

    def __exit__(self, *args):
        plt.close()


def main_cli():
    mp3_root = Path("TVSM-extractor-audio")
    png_root = Path("TVSM-extractor-images")
    datasets = { "cuesheet", "test" }
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'root', metavar='dataset', choices=datasets,
        default="test", nargs='?',
        help = " | ".join(datasets)
    )
    parser.add_argument(
        'ids', metavar='file_id', type=int, nargs='*',
        help='an integer file id'
    )
    parsed = parser.parse_args()
    Parameters.file_ids = parsed.ids
    parameters = Parameters(16, 'serif')
    root = Path(f'TVSM-{parsed.root}')
    transpose = ({
        "TVSM-cuesheet": True
    }).get(
        root.name, False
    )
    mp3_root.mkdir(parents=True, exist_ok=True)
    png_root.mkdir(parents=True, exist_ok=True)
    mel_list = list(load_mel_files(
        root, transpose, parameters.sample_rate,
        parameters.hop_length, file_ids=parameters.file_ids,
        language=parameters.language, genre=parameters.genre,
        segment_seconds=parameters.clip_seconds,
        fraction_per_source=parameters.fraction_per_source
    ))
    print(f'Found {len(mel_list)}x {parameters.clip_seconds}s clips')
    for file_id, mel_clip, labels in mel_list:
        audio = mel_to_audio(
            mel_clip, sr=parameters.sample_rate, n_fft=parameters.n_fft,
            win_length=parameters.win_length,
            hop_length=parameters.hop_length
        )
        png_file = png_root / f"{file_id}.png"
        mp3_file = mp3_root / f"{file_id}.mp3"
        label_dict = {
            parsed.root: labels
        }
        sf.write(mp3_file, audio, parameters.sample_rate, subtype='MPEG_LAYER_III')
        with Plotter(sf.read(mp3_file)[0], label_dict, parameters) as fig: 
            fig.savefig(png_file, transparent=True)
        print(f"Saved {png_file} and {mp3_file}")
