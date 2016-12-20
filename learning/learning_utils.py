
def save_sample(json_str):
    with open("samples.txt", "a") as f:
        f.write(json_str + "\n")
