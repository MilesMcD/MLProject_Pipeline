import sys
sys.path.append('src')
from src.data import read_raw_data, preprocess_data, get_features, get_label
#initiate testing by opening a terminal in the project root and typing "python -m pytest src"
#this forces python to include the directory in PYTHON_PATH .

#test expected shape of database
def test_raw_shape():
    dframe = read_raw_data()
    assert dframe.shape == (150, 5)

#ensure we don't get labels.
def test_get_features_shape():
    dframe = read_raw_data()
    processed = preprocess_data(dframe)
    features = get_features(processed)
    label = get_label(processed)

    assert features.shape == (150, 4)
    assert label.shape == (150,)
