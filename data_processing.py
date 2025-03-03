import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preprocess_data(data):
    """
    Cleans, encodes, and scales the dataset.
    Expects 'outbreak_label' as the target column.
    """
    # Drop rows with missing target labels
    data = data.dropna(subset=['outbreak_label'])

    # Encode categorical variables (One-Hot Encoding)
    data = pd.get_dummies(data, drop_first=True)
    
    # Split features and target variable
    X = data.drop(columns=['outbreak_label'])
    y = data['outbreak_label']
    
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return train_test_split(X_scaled, y, test_size=0.2, random_state=42)

if __name__ == "__main__":
    # Example dataset for testing
    sample_data = pd.DataFrame({
        "pathogen": ["Syphilis", "HPV", "HSV", "HIV"],
        "location": ["USA", "Canada", "Mexico", "UK"],
        "outbreak_label": [1, 0, 1, 0]
    })

    X_train, X_test, y_train, y_test = preprocess_data(sample_data)
    print("Processed Data Shapes:", X_train.shape, X_test.shape)
