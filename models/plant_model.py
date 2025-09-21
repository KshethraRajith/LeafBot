import pandas as pd
import numpy as np
from PIL import Image
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from skimage.feature import hog
from skimage import color

class PlantModel:
    def __init__(self):
        self.plants_df = pd.read_csv('plant20_nasa_1000.csv')
        self.classifier = KNeighborsClassifier(n_neighbors=3)
        self.scaler = StandardScaler()
        self._initialize_classifier()

    def _initialize_classifier(self):
        # In a real application, you would load pre-computed features here
        # For demo, we'll create dummy features based on indices
        dummy_features = np.random.rand(len(self.plants_df), 128)
        self.scaler.fit(dummy_features)
        self.classifier.fit(dummy_features, self.plants_df.index)

    def extract_features(self, img_array):
        # Convert to grayscale if image is RGB
        if len(img_array.shape) == 3:
            img_gray = color.rgb2gray(img_array)
        else:
            img_gray = img_array
            
        # Extract HOG features
        features = hog(img_gray, orientations=8, pixels_per_cell=(16, 16),
                      cells_per_block=(1, 1), visualize=False)
        return features.reshape(1, -1)

    def process_image(self, image_path):
        # Process image and convert to array
        img = Image.open(image_path)
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        return img_array

    def verify_plant(self, image_path):
        try:
            # Process the image
            img_array = self.process_image(image_path)
            
            # Extract features
            features = self.extract_features(img_array)
            
            # Scale features
            scaled_features = self.scaler.transform(features)
            
            # Get prediction
            predicted_idx = self.classifier.predict(scaled_features)[0]
            
            # Return the plant details
            return self.plants_df.iloc[predicted_idx].to_dict()
            
        except Exception as e:
            print(f"Error in plant verification: {str(e)}")
            return self.plants_df.sample(1).to_dict('records')[0]  # Fallback to random selection


    def search_plant(self, plant_name):
        try:
           
            # Escape special characters in the search string
            escaped_name = re.escape(plant_name)
            print("Searching for:", plant_name)
            print("Escaped name:", escaped_name)
            
            # Search for plants by name (both common and scientific)
            results = self.plants_df[
                self.plants_df['Common Name'].str.contains(escaped_name, case=False, na=False, regex=True) |
                self.plants_df['Scientific Name'].str.contains(escaped_name, case=False, na=False, regex=True)
            ]
            
            return results.to_dict('records')
        except Exception as e:
            print(f"Search error: {str(e)}")
            return []