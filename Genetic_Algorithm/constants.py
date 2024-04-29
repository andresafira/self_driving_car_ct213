# Reproduction Constants
MUT_SCALE = 0.5
CROSSOVER_SCALE = 0.3

# Network Storage Path
FILE_PATH = "best_classifier.txt"

# Classifier Parameters
LEAKY_ALPHA = 0.01  # This constant should be less than 1
THRESHOLD = 0.0  # If node value is greater than 0.5, then it activates, must be between -1 and 1

# Population Hyperparameters
N_WIN = 4
N_OF_MUTATED_SONS = 2
N_START = N_WIN * (N_OF_MUTATED_SONS + 2)  # This is a number of classifiers that stays constant
                                           # after selection and reproductions

