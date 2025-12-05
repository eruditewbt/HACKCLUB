import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import joblib # For saving/loading the trained model
import csv
import os

class SupervisedDSSModel:
    def __init__(self, data_path='project_data.csv'):
        self.data_path = data_path
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.preprocessor = None
        self.target_encoders = {} # To store encoders for each target variable
        self.target_names = ["Life Cycle", "Methodology", "Language", "Model (Architectural)", "Timeframe Management", "Risk Management", "Testing Strategy", "Deployment", "Documentation", "Collaboration Tools"]

    def load_data(self):
        """Loads the project data from a CSV file."""
        # try:
        df = pd.read_csv(self.data_path)
        print(f"Data loaded successfully from {self.data_path}. Shape: {df.shape}")
        return df
        # except FileNotFoundError:
        #     print(f"Error: The file '{self.data_path}' was not found.{FileNotFoundError.__str__}")
        #     return None

    def preprocess_data(self, df):
        """
        Preprocesses the data:
        - Separates features (X) and targets (y).
        - Applies one-hot encoding to categorical features.
        - Applies label encoding to each target variable.
        """
        # Define features and targets
        features = [
            "Project Size", "Project Complexity", "Requirements Clarity", "Team Size", "Stakeholder Involvement", "Budget",
            "Regulatory Compliance", "Innovation Level", "Risk Tolerance", "Urgency/Time-to-Market", "Project Type (Implicit)", "DevOps Implemented"
        ]
        targets = self.target_names

        X = df[features]
        y = df[targets]

        # Identify categorical features for encoding
        categorical_features = X.select_dtypes(include=['object']).columns

        # Create a preprocessor using ColumnTransformer for features
        # OneHotEncoder is suitable for nominal categorical features
        # drop='first' avoids multicollinearity for OHE
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), categorical_features)
            ],
            remainder='passthrough' # Keep other (e.g., numerical) columns as they are
        )

        # Apply LabelEncoder to each target variable and store them
        y_encoded = pd.DataFrame()
        for col in targets:
            le = LabelEncoder()
            y_encoded[col] = le.fit_transform(y[col])
            self.target_encoders[col] = le
            print(f"LabelEncoder fitted for target '{col}'. Classes: {le.classes_}")

        return X, y_encoded

    def split_data(self, X, y_encoded, test_size=0.2, random_state=42):
        """Splits data into training and testing sets."""
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y_encoded, test_size=test_size, random_state=random_state
        )
        print(f"Data split into training ({len(self.X_train)} samples) and testing ({len(self.X_test)} samples).")

    def train_model(self):
        """Trains a MultiOutputClassifier model."""
        # Use a pipeline to combine preprocessing and model training
        # RandomForestClassifier is a good choice for multi-output classification
        # You could also try GradientBoostingClassifier, DecisionTreeClassifier, etc.
        self.model = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('classifier', MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42)))
            # ('classifier', MultiOutputClassifier(GradientBoostingClassifier(n_estimators=100, random_state=42)))
        ])

        print("Training model...")
        self.model.fit(self.X_train, self.y_train)
        print("Model training complete.")

    def evaluate_model(self):
        """Evaluates the trained model on the test set."""
        if self.model is None:
            print("Error: Model not trained yet. Call train_model() first.")
            return

        print("\n--- Model Evaluation ---")
        y_pred = self.model.predict(self.X_test)

        # Evaluate performance for each target
        for i, target_name in enumerate(self.target_names):
            print(f"\nEvaluating for Target: {target_name}")
            # Decode predictions and true labels for better readability in report
            y_test_decoded = self.target_encoders[target_name].inverse_transform(self.y_test.iloc[:, i])
            y_pred_decoded = self.target_encoders[target_name].inverse_transform(y_pred[:, i])

            accuracy = accuracy_score(self.y_test.iloc[:, i], y_pred[:, i])
            print(f"Accuracy for {target_name}: {accuracy:.4f}")
            print(classification_report(y_test_decoded, y_pred_decoded, zero_division=0))

            # Additional insights:
            # print(f"Sample of true labels: {y_test_decoded[:5]}")
            # print(f"Sample of predicted labels: {y_pred_decoded[:5]}")

    def save_model(self, filename='dss_model.joblib'):
        """Saves the trained model and encoders to disk."""
        if self.model:
            joblib.dump({
                'model': self.model,
                'target_encoders': self.target_encoders,
                'target_names': self.target_names
            }, filename)
            print(f"Model and encoders saved to {filename}")
        else:
            print("No model to save.")

    def load_saved_model(self, filename='dss_model.joblib'):
        """Loads a trained model and encoders from disk."""
        try:
            saved_data = joblib.load(filename)
            self.model = saved_data['model']
            self.target_encoders = saved_data['target_encoders']
            self.target_names = saved_data['target_names']
            self.preprocessor = self.model.named_steps['preprocessor'] # Re-extract preprocessor from pipeline
            print(f"Model and encoders loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"Error: Model file '{filename}' not found.")
            return False
        except KeyError:
            print("Error: Invalid model file format.")
            return False

    def predict_for_new_project(self, project_characteristics_dict):
        """
        Makes predictions for a new project based on user input.

        Args:
            project_characteristics_dict (dict): A dictionary of new project
                                                 characteristics (features).
                                                 e.g., {'Project Size': 'Small', ...}
        Returns:
            dict: A dictionary of recommended methods and plans.
        """
        if self.model is None:
            print("Error: Model not loaded or trained. Cannot make predictions.")
            return {}

        # Convert the input dictionary to a pandas DataFrame
        # Ensure column order matches the training data (important for OHE)
        # Create a DataFrame with a single row
        input_df = pd.DataFrame([project_characteristics_dict])

        # Preprocess the new data using the *fitted* preprocessor from the model
        # The pipeline handles this automatically if you're using it for prediction
        # preprocessed_input = self.preprocessor.transform(input_df) # No, the pipeline does it.

        # Make prediction
        predicted_encoded = self.model.predict(input_df)

        # Decode the numerical predictions back to original labels
        decoded_predictions = {}
        for i, target_name in enumerate(self.target_names):
            predicted_label_encoded = predicted_encoded[0, i] # Get the single prediction for this target
            decoded_label = self.target_encoders[target_name].inverse_transform([predicted_label_encoded])[0]
            decoded_predictions[target_name] = decoded_label

        return decoded_predictions

# --- Main execution block for training and saving ---
if __name__ == "__main__":

    # file_exists = os.path.isfile('C:/Users/eruditewbt/OneDrive/Desktop/HACKCLUB/project_data.csv')
    # if not file_exists:
    #            print(f"Error: The file 'project_data.csv' was not found.")
    # dss_trainer = SupervisedDSSModel(data_path='C:/Users/eruditewbt/OneDrive/Desktop/HACKCLUB/project_data.csv')

 
    # # 1. Load Data
    # df = dss_trainer.load_data()
    # if df is None:
    #     exit()

    # # 2. Preprocess Data
    # X, y = dss_trainer.preprocess_data(df)

    # # 3. Split Data
    # dss_trainer.split_data(X, y)

    # # 4. Train Model
    # dss_trainer.train_model()

    # # 5. Evaluate Model
    # dss_trainer.evaluate_model()

    # # 6. Save Model
    # dss_trainer.save_model()

    # --- Example of loading and making a prediction ---
    print("\n--- Testing the saved model with a new project ---")
    dss_predictor = SupervisedDSSModel() # Create a new instance for prediction
    dss_predictor.evaluate_model()
    if dss_predictor.load_saved_model():
        new_project_data = {
            'Project Size': 'Medium',
            'Project Complexity': 'High',
            'Requirements Clarity': 'Unclear',
            'Team Size': 'Very Large (50+)',
            'Stakeholder Involvement': 'Low',
            'Budget': 'Very High',
            'Regulatory Compliance': 'Medium',
            'Innovation Level': 'High',
            'Risk Tolerance': 'High',
            'Urgency/Time-to-Market': 'Low',
            'Project Type (Implicit)': 'Other',
            'DevOps Implemented': 'Yes'
        }
        recommendations = dss_predictor.predict_for_new_project(new_project_data)
        print("\nRecommendations for the new project:")
        for category, recommendation in recommendations.items():
            print(f"  {category}: {recommendation}")

        new_project_data_2 = {
            'Project Size': 'Large',
            'Project Complexity': 'High',
            'Requirements Clarity': 'Evolving',
            'Team Size': 'Large (21-50)',
            'Stakeholder Involvement': 'High',
            'Budget': 'Very High',
            'Regulatory Compliance': 'Medium',
            'Innovation Level': 'High',
            'Risk Tolerance': 'High',
            'Urgency/Time-to-Market': 'High',
            'Project Type (Implicit)': 'Desktop App',
            'DevOps Implemented': 'Yes'
        }
        recommendations_2 = dss_predictor.predict_for_new_project(new_project_data_2)
        print("\nRecommendations for another new project:")
        for category, recommendation in recommendations_2.items():
            print(f"  {category}: {recommendation}")
    else:
        print("Could not load model for prediction.")