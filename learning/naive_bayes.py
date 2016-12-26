from functools import reduce
import numpy as np
from . import learning_utils

def learn_label_priors(samples):
    priors = {}
    for sample in samples:
        if sample["label"] not in priors:
            # initialize to 1 for laplace smoothing in numerator
            priors[sample["label"]] = 1
        priors[sample["label"]] += 1
    total = sum(priors.values())
    for label in priors:
        # apply laplace smoothing in denominator
        priors[label] /= (total + len(priors))
    return priors

def learn_feature_priors(samples):
    # applies laplace smoothing
    features = np.array(list(map(lambda x: x["data"], samples))) + np.ones(len(samples[0]["data"]))
    return (sum(features) / (len(samples) + 2).tolist())

def learn_feature_posteriors(samples):
    feature_posteriors = {}
    labels = set()
    for sample in samples:
        labels.add(sample["label"])
    for label in labels:
        relevant_samples = list(filter(lambda x: x["label"] == label, samples))
        # laplace smoothing is applied in learn_feature_priors
        feature_posteriors[label] = learn_feature_priors(relevant_samples)
    return feature_posteriors

def train(samples):
    label_priors = learn_label_priors(samples)
    feature_priors = learn_feature_priors(samples)
    feature_posteriors = learn_feature_posteriors(samples)
    return (label_priors, feature_priors, feature_posteriors)

def test(sample, training_data):
    label_priors, feature_priors, feature_posteriors = training_data
    ret = {}
    for label in label_priors:
        posterior = reduce(
            lambda x, y: x * y,
            map(lambda x: abs(x[0] - 1 + x[1]),
                zip(sample, feature_posteriors[label])),
            1)
        denom = reduce(
            lambda x, y: x * y,
            map(lambda x: abs(x[0] - 1 + x[1]),
                zip(sample, feature_priors)),
            1)
        ret[label] = label_priors[label] * posterior / denom
    return ret

if __name__ == "__main__":
    import json
    data = learning_utils.read_samples()
    training_data = train(data)
    with open("learning/nb_training_data.json", "w") as f:
        f.write(json.dumps(training_data))
