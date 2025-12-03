"""
Simple ML model for anomaly detection in energy data.

This is a baseline Random Forest implementation - kept simple as requested.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
from pathlib import Path
import joblib
from typing import Tuple, Dict, Optional


class AnomalyDetector:
    """
    Simple Random Forest classifier for anomaly detection.

    Features used:
    - Energy load value
    - Temperature (mean, min, max)
    - Day of week
    - Month
    - Is weekend

    Target: is_anomaly (binary: 0 or 1)
    """

    def __init__(self, random_state: int = 42):
        """
        Initialize the anomaly detector.

        Args:
            random_state: Random seed for reproducibility
        """
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            class_weight='balanced'  # Handle class imbalance
        )
        self.feature_names: Optional[list] = None
        self.is_trained = False

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for training/prediction.

        Simple feature engineering - only basic features.

        Args:
            df: Raw dataframe with energy and weather data

        Returns:
            DataFrame with engineered features
        """
        features_df = pd.DataFrame()

        # Basic features
        features_df['load'] = df['val_cargaenergiamwmed']
        features_df['temp_mean'] = df['temp_mean']
        features_df['temp_min'] = df['temp_min']
        features_df['temp_max'] = df['temp_max']

        # Temporal features
        if 'date' in df.columns:
            features_df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
            features_df['month'] = pd.to_datetime(df['date']).dt.month
            features_df['is_weekend'] = (features_df['day_of_week'] >= 5).astype(int)

        # Regional encoding (simple label encoding)
        if 'region' in df.columns:
            region_map = {
                'Norte': 0,
                'Nordeste': 1,
                'Sudeste/Centro-Oeste': 2,
                'Sul': 3
            }
            features_df['region_code'] = df['region'].map(region_map)

        return features_df

    def train(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict:
        """
        Train the model on labeled data.

        Args:
            df: DataFrame with features and 'is_anomaly' target
            test_size: Proportion of data for testing (default 20%)

        Returns:
            Dictionary with training metrics
        """
        # Prepare features
        X = self.prepare_features(df)
        y = df['is_anomaly']

        # Store feature names
        self.feature_names = X.columns.tolist()

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate
        y_pred = self.model.predict(X_test)

        # Metrics
        precision, recall, f1, support = precision_recall_fscore_support(
            y_test, y_pred, average='binary', zero_division=0
        )

        cm = confusion_matrix(y_test, y_pred)

        metrics = {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'accuracy': (y_pred == y_test).mean(),
            'confusion_matrix': cm,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'n_features': len(self.feature_names),
            'classification_report': classification_report(y_test, y_pred)
        }

        print("\n=== Model Performance ===")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        print(f"Precision: {metrics['precision']:.3f}")
        print(f"Recall: {metrics['recall']:.3f}")
        print(f"F1-Score: {metrics['f1_score']:.3f}")
        print(f"\nConfusion Matrix:")
        print(cm)
        print(f"\nClassification Report:")
        print(metrics['classification_report'])

        return metrics

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predict anomalies for new data.

        Args:
            df: DataFrame with features

        Returns:
            Array of predictions (0 or 1)
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")

        X = self.prepare_features(df)
        return self.model.predict(X)

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        """
        Predict anomaly probabilities.

        Args:
            df: DataFrame with features

        Returns:
            Array of probabilities [P(normal), P(anomaly)]
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")

        X = self.prepare_features(df)
        return self.model.predict_proba(X)

    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from the trained model.

        Returns:
            DataFrame with features and their importance scores
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")

        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        return importance_df

    def save(self, path: str = "data/models/anomaly_detector.pkl") -> None:
        """
        Save the trained model to disk.

        Args:
            path: Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet. Call train() first.")

        # Create directory if needed
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self, path)
        print(f"Model saved to {path}")

    @classmethod
    def load(cls, path: str = "data/models/anomaly_detector.pkl") -> 'AnomalyDetector':
        """
        Load a trained model from disk.

        Args:
            path: Path to the saved model

        Returns:
            Loaded AnomalyDetector instance
        """
        model = joblib.load(path)
        print(f"Model loaded from {path}")
        return model
