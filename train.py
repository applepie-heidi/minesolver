import imp

from keras.models import load_model

from brain import Brain


def main():
    choice = 1#int(input("1. Train a new model from scratch \n2. Keep training a pre-trained model\n<1/2>? "))
    model_name = 'intermediate_model-conv2d1.py'  # input("What is the name of the model/model code? ")
    sessions = 10000  # int(input("How many learning sessions [10000]? "))
    samples = 371  # int(input("How many game moves (clicks) per session [200]? "))
    epochs = 10  # int(input("How many training epochs? "))

    split = model_name.split("_")
    difficulty = split[0]
    name = split[1]

    if choice == 1:
        name = name[0:name.index('.')]
        source = imp.load_source(model_name, "fresh_models/" + model_name)
        model = source.model
    elif choice == 2:
        model = load_model("models/" + model_name)

    brain = Brain(model, difficulty, name)
    brain.learn(sessions, samples, epochs)
    print('finished')

    brain.model.save("models/" + difficulty + '_' + name)


if __name__ == "__main__":
    main()
