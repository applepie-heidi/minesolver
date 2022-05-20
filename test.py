from keras.models import load_model

from brain_old1 import Brain


def main():
    model_name = input("What is the name of the model/model code? ")
    split = model_name.split("_")
    difficulty = split[0]
    name = split[1]
    model = load_model("models/" + model_name)
    brain = Brain(model, difficulty, name)
    games = int(input("How many games to test on? "))
    brain.test(games)


if __name__ == '__main__':
    main()
