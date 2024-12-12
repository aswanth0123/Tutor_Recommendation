import pickle
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the saved course vectors
def load_course_vectors(filename="course_vectors.pkl"):
    with open(filename, 'rb') as file:
        print(file)
        course_ids, course_vectors = pickle.load(file)
    return course_ids, course_vectors

# Function to vectorize user input
def vectorize_user_input(user_input):
    """Vectorize the user input for recommendation."""
    return model.encode(user_input)

# Function to recommend courses
def recommend_courses(user_input, course_vectors, course_ids, top_n=3):
    """Recommend courses based on user input."""
    user_vector = vectorize_user_input(user_input)
    similarities = util.cos_sim(user_vector, course_vectors)
    
    # Ensure similarity scores are a NumPy array
    similarity_scores = similarities[0].cpu().numpy()  # Convert to NumPy array
    
    # Sort courses by similarity
    sorted_indices = np.argsort(similarity_scores)[::-1]  # Descending sort
    recommended_courses = [(course_ids[idx], similarity_scores[idx]) for idx in sorted_indices[:top_n]]
    
    return recommended_courses

# Load saved course vectors and convert to tensor
course_ids, course_vectors = load_course_vectors()

# Fix: Convert list of NumPy arrays to one big NumPy array before converting to a PyTorch tensor
course_vectors = np.array(course_vectors)  # Combine list of NumPy arrays to one array
course_vectors = torch.tensor(course_vectors)  # Convert NumPy array to PyTorch tensor

# Example user input
user_input = "python"

# Recommend courses
recommended_courses = recommend_courses(user_input, course_vectors, course_ids, top_n=3)

print("Recommended Courses:", recommended_courses)
