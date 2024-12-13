import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer

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
def process_search(search):
    if search:
        search_list = search.split(',')
        search_vectors = model.encode(search_list)
        search_vector = search_vectors.mean(axis=0)
        return search_vector

# Function to combine course data and reviews to create a vector
def combine_course_data_with_reviews(course_data):
    """Combine course metadata and the review essence to generate a combined vector."""
    combined_text = f"Course Name: {course_data['name']}, Rating: {course_data['rating']}, " \
                    f"Class: {course_data['class']}, " \
                    f"Duration: {course_data['duration']}, Description: {course_data['description']}"
    
    course_vector = model.encode(combined_text)  # Vectorize the course metadata
    review_vector = process_reviews(course_data['reviews'])  # Vectorize the reviews
    
    if review_vector is not None:
        combined_vector = course_vector + review_vector  # Combine the course vector and review vector
    else:
        combined_vector = course_vector  # If no reviews, just use the course data
    print(combined_vector)
    return combined_vector


def combine_student_with_search(student_data):
    combined_text = f"student_id: {student_data['student_id']},  " \
                    f"class: {student_data['class']}, " 
    student_vector = model.encode(combined_text)
    search_vector = process_search(student_data['search'])
    if search_vector is not None:
        combined_vector = student_vector + search_vector
    else:
        combined_vector = student_vector
    return combined_vector



# Vectorize all courses with reviews
def vectorize_courses_with_reviews(df):
    """Vectorize all courses in the dataframe."""
    course_vectors = []
    for _, course in df.iterrows():
        course_vector = combine_course_data_with_reviews(course)
        course_vectors.append(course_vector)
    return course_vectors


def vectorize_student_with_search(df): 
    student_vectors = []    
    for _, student in df.iterrows():
        student_vector = combine_student_with_search(student)
        student_vectors.append(student_vector)
    return student_vectors


# Function to save course vectors
# def save_course_vectors(course_vectors, course_ids, filename="course_vectors.pkl"):
#     with open(filename, 'wb') as file:
#         pickle.dump((course_ids, course_vectors), file)
