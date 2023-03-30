from simpletransformers.classification import Classification, ClassificationArgs
from sklearn.metrics import accuracy_score
import pandas as pd
import logging
import os


DATA = 'i2kdata/i2k_dataset_v2.csv'


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger('transformers')
transformers_logger.setLevel(logging.WARNING)


# Load in dataset to initial dataFrame
init_data = pd.read_csv(DATA, usecols=[0,1], delimiter=',')


# Shuffle init_dataFrame data with shuffle()
# and a random state of 23 to have reproducability
init_dataFrame = init_data.sample(frac=1, random_state=23).reset_index(drop=True)


# Create a training dataFrame derived from 
# the initial dataFrame
training_dataFrame = init_dataFrame.sample(frac=0.7, random_state=23).reset_index(drop=True)


# Create an evaluation dataFrame and
# fill it with everything that wasnt included in 
eval_dataFrame = init_dataFrame.drop(training_dataFrame.index)


# Optional model configuration
model_args = ClassificationArgs(num_train_epochs=1, overwrite_output_dir=True, use_multiprocessing=False, use_multiprocessing_for_evaluation=False)
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# Create a ClassificationModel
model = Classification(
    'roberta', 'roberta-base', use_cuda=False, args=model_args
)


# Train the model with batch of 16
model.train_model(training_dataFrame, batch_size=16)


# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_dataFrame, acc=accuracy_score)