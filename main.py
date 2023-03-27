from simpletransformers.classification import ClassificationModel, ClassificationArgs
from sklearn.metrics import accuracy_score
import pandas as pd
import logging
import os
import matplotlib.pyplot as plt

TRAINING_DATA = 'i2kdata/i2k_dataset.csv'
EVALUATE_DATA = 'i2kdata/i2k_dataset.csv'

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Load in to main dataFrame
main_dataFrame = pd.read_csv(TRAINING_DATA, usecols=[0,1], delimiter=',')
main_df = pd.DataFrame(main_dataFrame)

# Shuffle the dataset with sample(). Random_state -> 23 is to have reproducability
main_df = main_dataFrame.sample(frac=1, random_state=23).reset_index(drop=True)

# Create a train dataframe for training derived from main_dataframe, shuffle
train_dataFrame = main_df.sample(frac=0.7, random_state=23).reset_index(drop=True)

# Create a evaluation dataframe and fill with everything that wasnt stuffed into train dataframe
eval_dataFrame = main_df.drop(train_dataFrame.index)

# Optional model configuration
model_args = ClassificationArgs(num_train_epochs=1, overwrite_output_dir=True, use_multiprocessing=False, use_multiprocessing_for_evaluation=False)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Create a ClassificationModel
model = ClassificationModel(
   "roberta", "roberta-base", use_cuda=False, args=model_args
)

# Train the model with batch of 16
#model.train_model(train_dataFrame, batch_size=16)

# Evaluate the model
result, model_outputs, wrong_predictions = model.eval_model(eval_dataFrame, acc=accuracy_score)

#print("Accuracy: {:.2f}%".format(result['acc']*100))

# Make predictions with the model, lets wait to predict for now
#predictions, raw_outputs = model.predict(["The food was good"])

#print(predictions)

