import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer

# Sample course data
courses_data = [
    {"course_id": 1, "name": "Python for Beginners", "rating": 4.5, "class": "5th Standard", "age_group": "10-12", 
     "duration": "5 months", "description": "A beginner's guide to Python.", "reviews": "Good practical sessions, theory is okay"},
    {"course_id": 2, "name": "Dance Basics", "rating": 4.7, "class": "3rd Standard", "age_group": "8-10", 
     "duration": "3 months", "description": "Basic dance moves and rhythm.", "reviews": "Fun classes, great energy, could use more structure"},
    {"course_id": 3, "name": "Advanced Physics", "rating": 4.8, "class": "10th Standard", "age_group": "14-16", 
     "duration": "1 year", "description": "In-depth study of physics.", "reviews": "Challenging but rewarding, theory-heavy"},
    {"course_id": 4, "name": "Photography", "rating": 4.6, "class": "9th Standard", "age_group": "12-14", 
     "duration": "6 months", "description": "Introduction to photography.", "reviews": "Creative lessons, very visual, wish for more theory"},
    {"course_id": 5, "name": "Data Science", "rating": 4.9, "class": "12th Standard", "age_group": "16-18", 
     "duration": "1 year", "description": "Learn data analysis techniques.", "reviews": "Great for beginners, practical aspects are solid"}
]

# Create DataFrame
df = pd.DataFrame(courses_data)

# Initialize Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to process and vectorize reviews for a course
def process_reviews(reviews):
    """Vectorize each review and return the average vector."""
    if reviews:  # If there are reviews
        review_list = reviews.split(',')  # Split reviews into individual comments
        review_vectors = model.encode(review_list)  # Vectorize each review separately
        review_vector = review_vectors.mean(axis=0)  # Calculate average of review vectors
        return review_vector
    else:
        return None  # No reviews available

# Function to combine course data and reviews to create a vector
def combine_course_data_with_reviews(course_data):
    """Combine course metadata and the review essence to generate a combined vector."""
    combined_text = f"Course Name: {course_data['name']}, Rating: {course_data['rating']}, " \
                    f"Class: {course_data['class']}, Age Group: {course_data['age_group']}, " \
                    f"Duration: {course_data['duration']}, Description: {course_data['description']}"
    
    course_vector = model.encode(combined_text)  # Vectorize the course metadata
    review_vector = process_reviews(course_data['reviews'])  # Vectorize the reviews
    
    if review_vector is not None:
        combined_vector = course_vector + review_vector  # Combine the course vector and review vector
    else:
        combined_vector = course_vector  # If no reviews, just use the course data

    
    
    return combined_vector

# Vectorize all courses with reviews
def vectorize_courses_with_reviews(df):
    """Vectorize all courses in the dataframe."""
    course_vectors = []
    for _, course in df.iterrows():
        course_vector = combine_course_data_with_reviews(course)
        course_vectors.append(course_vector)
    return course_vectors

# Vectorizing courses with reviews
course_vectors = vectorize_courses_with_reviews(df)

# Function to save course vectors
def save_course_vectors(course_vectors, course_ids, filename="course_vectors.pkl"):
    with open(filename, 'wb') as file:
        pickle.dump((course_ids, course_vectors), file)

# Save the course vectors with course_ids
save_course_vectors(course_vectors, df['course_id'].tolist())

print("Course vectors saved successfully!")
