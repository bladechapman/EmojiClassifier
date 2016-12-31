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

if __name__ == "__main__":
    confusion_values = five_fold_cross_validate(naive_bayes)
    for label in confusion_values:
        print (label, confusion_values[label])
