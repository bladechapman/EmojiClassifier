import json
from functools import reduce
from learning import naive_bayes
from learning.sample import Sample

def read_samples():
    """
    Reads samples from "samples.txt"
    :return: array of Sample objects
    """
    samples = []
    with open("samples.txt", "r") as f:
        for line in f:
            samples.append(Sample(line))
    return samples

def convert_data_to_2d(data):
    """
    Converts 1d data to 2d data. Length of given data must be the square of
    some dimension
    :param data: 1D data
    :return: 2D data
    """
    dimension = int(len(data) ** (1/2))
    return [data[i*dimension:(i+1)*dimension] for i in range(dimension)]

def convert_data_to_1d(data):
    """
    Converts  2d data to 1d data
    :param data: 2D data
    :return: 1D data
    """
    return list(reduce(lambda x, y: x + y, data, []))

def prod(l):
    """
    Analogous to sum, but for multiplication
    :param l: iterable containing numbers
    :return: the product of all the numbers in the list
    """
    return reduce(lambda x, y: x * y, l, 1)

def cross_validate(learning_model, num_folds=5, samples=read_samples()):
    """
    Cross validates a learning algorithm
    :param learning_model: A learning module that has test and train funcs
    :param num_folds: Cross validation folds
    :param samples: Samples for use in validation
    :return: A dictionary containing confusion values
    """
    model = learning_model()
    labels = set(map(lambda x: x.label, samples))
    folds = [samples[int(i*len(samples)/num_folds):int((i+1)*len(samples)/num_folds)] for i in range(num_folds)]
    confusion_values = {i:{l: 0 for l in labels} for i in labels}
    for i, test_data in enumerate(folds):
        training_data = sum(folds[:i] + folds[i+1:], [])
        model.train(training_data)
        for test_datum in test_data:
            guessed_label = model.test(test_datum.data)
            confusion_values[test_datum.label][guessed_label] += 1
    for label in confusion_values:
        total = sum(confusion_values[label].values())
        for sublabel in confusion_values[label]:
            confusion_values[label][sublabel] /= total
    return confusion_values

def normalize_2d(data):
    """
    Normalizes a 2D sample's data
    :param sample: 2D sample
    :return: normalized 2D sample
    """
    sd = data
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
    confusion_values = cross_validate(naive_bayes.NaiveBayes)
    for label in confusion_values:
        print (label, confusion_values[label])
