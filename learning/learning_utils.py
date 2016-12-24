import json

def save_sample(json_str):
    with open("samples.txt", "a") as f:
        f.write(json_str + "\n")

def read_samples():
    samples = []
    with open("samples.txt", "r") as f:
        for line in f:
            sample = json.loads(line.strip("\n"))
            samples.append(sample)
    return samples
