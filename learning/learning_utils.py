import json
from functools import reduce
from learning import naive_bayes

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

def convert_sample_to_2d(sample):
    data = sample["data"]
    label = sample["label"]
    dimension = int(len(data) ** (1/2))
    return {
        "data": [data[i*dimension:(i+1)*dimension] for i in range(dimension)],
        "label": label
    }

def convert_sample_to_1d(sample):
    data = sample["data"]
    label = sample["label"]
    return {
        "data": reduce(lambda x, y: x + y, data, []),
        "label": label
    }

def prod(l):
    return reduce(lambda x, y: x * y, l, 1)

def five_fold_cross_validate(learning_module):
    num_folds = 5
    samples = read_samples()
    labels = set(map(lambda x: x["label"], samples))
    folds = [samples[int(i*len(samples)/num_folds):int((i+1)*len(samples)/num_folds)] for i in range(num_folds)]
    confusion_values = {i:{l: 0 for l in labels} for i in labels}
    for i in range(len(folds)):
        test_data = folds[i]
        training_data = reduce(lambda x,y:x+y, folds[:i] + folds[i+1:], [])
        training_params = learning_module.train(training_data)
        for test_datum in test_data:
            actual_label = test_datum["label"]
            guessed_label = learning_module.test(test_datum["data"], training_params)
            confusion_values[actual_label][guessed_label] += 1
    return confusion_values

def normalize_sample(sample):
    s = convert_sample_to_2d(sample)
    sd = s["data"]
    dimension = len(sd)
    rd = [[int(sd[x][y]) for x in range(dimension)] for y in range(dimension)]
    min_y = None
    max_y = None
    min_x = None
    max_x = None

    for y in range(dimension):
        if sd[y] != [False] * dimension and min_y == None:
            min_y = y
        if sd[y] != [False] * dimension:
            max_y = y
    for x in range(dimension):
        if rd[x] != [False] * dimension and min_x == None:
            min_x = x
        if rd[x] != [False] * dimension:
            max_x = x
    min_y = 0 if min_y == None else min_y
    min_x = 0 if min_x == None else min_x
    max_y = dimension - 1 if max_y == None else max_y
    max_x = dimension - 1 if max_x == None else max_x

    new_width = max_x - min_x
    new_height = max_y - min_y

    normalized_sample = [[0 for i in range(dimension)] for j in range(dimension)]
    for y in range(dimension):
        for x in range(dimension):
            mapped_x = int(new_width / dimension * x) + min_x
            mapped_y = int(new_height / dimension * y) + min_y
            normalized_sample[y][x] = sd[mapped_y][mapped_x]

    return normalized_sample


if __name__ == "__main__":
    confusion_values = five_fold_cross_validate(naive_bayes)
    for label in confusion_values:
        print (label, confusion_values[label])
