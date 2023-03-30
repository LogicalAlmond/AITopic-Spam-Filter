from simpletransformers.classification import Classification


# Load the model
model = Classification(
    'roberta', 'outputs/', use_cuda=False, args='config.json'
)


# Predict with the model
predictions, raw_outputs = model.predict([])
print(predictions[0])