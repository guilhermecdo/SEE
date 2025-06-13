import csv
import random
import os

def split_data(input_file, train_file, eval_file, train_percentage=0.8):
    """
    Splits a text file containing data paths into training and evaluation files.

    Args:
        input_file (str): Path to the input text file.
        train_file (str): Path to the output training text file.
        eval_file (str): Path to the output evaluation text file.
        train_percentage (float, optional): Percentage of data to use for training (default: 0.8).
    """
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_file}")
        return

    # Remove leading/trailing whitespace and shuffle the lines
    lines = [line.strip() for line in lines]
    random.shuffle(lines)

    # Calculate the split index
    split_index = int(len(lines) * train_percentage)

    # Split the data into training and evaluation sets
    train_lines = lines[:split_index]
    eval_lines = lines[split_index:]

    # Write the training data to the training file
    try:
        with open(train_file, 'w') as f_train:
            f_train.write('\n'.join(train_lines) + '\n') # Add a newline at the end
        print(f"Training data written to {train_file}")
    except Exception as e:
        print(f"Error writing to training file: {e}")
        return

    # Write the evaluation data to the evaluation file
    try:
        with open(eval_file, 'w') as f_eval:
            f_eval.write('\n'.join(eval_lines) + '\n') # Add a newline at the end
        print(f"Evaluation data written to {eval_file}")
    except Exception as e:
        print(f"Error writing to evaluation file: {e}")
        return

if __name__ == "__main__":
    missions=[1,2,3,4]
    sonar_model="P900"
    for m in missions:
        with open(f"/home/guilherme/Documents/SEE-Dataset/mission{m}.csv", newline='') as f:
            reader = csv.reader(f)
            mission_metadata = list(reader)
            mission_metadata.pop(0)
        #mission_met=[mission_metadata[12],mission_metadata[18],mission_metadata[36]]
        #mission_met=[mission_metadata[12]]
        for mission in mission_metadata:
            for i in range((int(mission[6])-1)):
                with open("files.txt", 'a') as f:
                    f.write(f"/home/guilherme/Documents/SEE-Dataset/Sonar-Dataset-mission-{m}-{sonar_model}/auv-{mission[0]}/GT-bin/{i}.npy /home/guilherme/Documents/SEE-Dataset/Sonar-Dataset-mission-{m}-{sonar_model}/auv-{mission[0]}/Raw-data/{i}.npy\n")
                    #f.write(f"/home/guilherme/Documents/SEE-Dataset/Sonar-Dataset-mission-{m}-{sonar_model}/auv-{mission[0]}/Cartesian-images/{i}.png\n")
    
    # Get the file paths from the user
    input_file = "files.txt"
    train_file = "train.txt"
    eval_file = "val.txt"

    train_percentage = 0.8
    
    # Call the split_data function
    split_data(input_file, train_file, eval_file, train_percentage)
    print("Data splitting complete.")
