# DataBoomer

A Jupyter tool for seamlessly transferring complex Python objects between notebooks. DataBoomer serializes your objects as base64 string and creates self-contained code snippets that can perfectly recreate them in any notebook.

## Key Features
- One-click copying of serialized objects to clipboard
- Handles complex Python objects using `dill`
- Creates self-contained, portable code snippets
- Automatically detects variable names
- Preserves object state exactly as it was

## Install
```bash
pip install databoomer
```

## Usage in Jupyter
```python
from databoomer import DataBoomer
import pandas as pd

# Save a complex DataFrame with custom processing
df = pd.DataFrame({'values': [1, 2, 3]})
df['processed'] = df['values'] * 2
DataBoomer(df, comment="Preprocessed dataset")
# Copies to clipboard:
# # comment: Preprocessed dataset
# payload = '''[encoded_data]'''
# df = dill.loads(codecs.decode(payload.encode(), 'base64'))

# Custom variable names
model = train_complex_model()
DataBoomer(model, obj_name="trained_model", comment="Model trained on XYZ dataset")

# The copied code can be pasted into any notebook to recreate the exact object
```

## Why DataBoomer?
- **Share Objects**: Easily transfer complex objects between notebooks
- **Session Recovery**: Save important objects in a format that survives kernel restarts
- **Collaboration**: Share exact object states with colleagues
- **State Preservation**: Captures complete object state, including custom attributes and processing

Remember: DataBoomer creates portable, self-contained code snippets that recreate your objects exactly as they were. Just boom it, switch notebooks, paste, and you're ready to go.

Note: This tool is particularly useful when working with objects that are:
- Result of complex processing
- Trained models or fitted transformers
- Custom class instances with specific state
- Image snippets, selfcontained in the jupyter lab
