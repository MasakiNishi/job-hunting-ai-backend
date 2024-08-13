# Job Hunting AI Tool: recommender.py
# Members: Masaki Nishi, Christian McKinnon, Susan Joh, and Alexander Wong
# Project Partner: Professor Gates
# CS 467 Portfolio Project
#
# Job Recommendation Model using TF-IDF and Cosine Similarity
#
# Description:
# Implements a simple content-filtering based approach using
# Cosine Similarity with TF-IDF (term frequency-inverse document
# frequency) Vectorizer to recommend jobs based on a user's input
# and job listings found in cleaned_listings.json.
#
# This model works by "vectorzing" user inputs and job listings
# using the sklearn's TfidfVectorizer. We then use pairwise
# distances to calculate the cosine of the angle between these
# vectors. This metric can range from -1 (completely dissimilar)
# to 1 (completely identical). Our model frames user input vectors
# against their corresponding variables in the job listings matrx.
# We then assign a similarity score, and return the top 5 items based
# on ranking.
#
# Sources:
# 1.) Scikit-learn: https://scikit-learn.org/stable/modules/generated/
# sklearn.feature_extraction.text.TfidfVectorizer.html
#
# 2.) Chan`s Jupyter, GitHub IO: https://goodboychan.github.io/python/
# datacamp/natural_language_processing/2020/07/17/
# 04-TF-IDF-and-similarity-scores.html#The-recommender-function
#
# 3.) Capital One: https://www.capitalone.com/tech/machine-learning/
# understanding-tf-idf/

# Import sklearn module for TfidfVectorizer and cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Import pandas the create the matrix using pandas dataframe
import pandas as pd


def job_recommender(user_data, job_listings):
    """This function is called in the submit() method of app.py and it
    takes in user input as the vector and the structured data from
    cleaned_listings.json, as the matrix (a Pandas dataframe), then
    calculates a cosine similarity score, which returns a ranking
    of the top 5 best matches according to the user's requirements."""

    # Ensure the model recognizes all incoming data in array format
    if not isinstance(user_data['experience'], list):
        user_data['experience'] = [user_data['experience']]
    if not isinstance(user_data['textInput'], list):
        user_data['textInput'] = [user_data['textInput']]

    # Create our features based off user input:
    job_types = ', '.join(user_data['jobType'])
    arrangements = ', '.join(user_data['arrangement'])
    sectors = ', '.join(user_data['sector'])
    experience = ', '.join(user_data['experience'])
    text_input = ', '.join(user_data['textInput'])

    # Convert job listings into a Pandas DataFrame
    corpus_df = pd.DataFrame(job_listings)

    # Concantenate the data into a matrix that comprised of the jobType,
    # arrangement, sector, experience, description, title, company, and
    # location as features from the cleaned_listing.json file. axis=1,
    # represents the columns
    corpus_df['combined'] = corpus_df.apply(
        lambda row: ' '.join(
            [row['jobType'], row['arrangement'], row['sector'],
             row['experience'], row['description'], row['title'],
             row['company'], row['location']]), axis=1)

    # Feature Engineering:
    # Use TF-IDF Vectorizer to transform text data to feature vectors
    # stop_words = 'english' removes common words with little meaning from
    # our calculation. max_df removes words that appear more than 90%
    # and min_df removes that appear less than 1%
    vec_sector = TfidfVectorizer(stop_words='english',
                                 max_df=0.9, min_df=0.01)
    vec_exp = TfidfVectorizer(stop_words='english',
                              max_df=0.9, min_df=0.01)
    vec_jt = TfidfVectorizer(stop_words='english',
                             max_df=0.9, min_df=0.01)
    vec_arr = TfidfVectorizer(stop_words='english',
                              max_df=0.9, min_df=0.01)
    vec_desc = TfidfVectorizer(stop_words='english',
                               max_df=0.85, min_df=0.01)
    vec_text = TfidfVectorizer(stop_words='english')

    # Fit and transform user input with data from cleaned_listing.json
    mtx_sector = vec_sector.fit_transform(corpus_df['sector'])
    mtx_exp = vec_exp.fit_transform(corpus_df['experience'])
    mtx_jt = vec_jt.fit_transform(corpus_df['jobType'])
    mtx_arr = vec_arr.fit_transform(corpus_df['arrangement'])
    mtx_desc = vec_desc.fit_transform(corpus_df['description'])
    mtx_text = vec_text.fit_transform(corpus_df['combined'])

    # Next we call transform() on the above vectors with user input
    # These all correspond except for experience vs. job descriptions
    input_vec_sec = vec_sector.transform([sectors])
    input_vec_exp = vec_exp.transform([experience])
    input_vec_jt = vec_jt.transform([job_types])
    input_vec_arr = vec_arr.transform([arrangements])
    # Here we vectorize input experience against the job listings description
    input_vec_desc = vec_desc.transform([experience])
    # We vectorize any potential text input across the entire corpus
    input_vec_text = vec_text.transform([text_input])

    # Calculate cosine similarity between user vectors and job matrices
    # .flatten() converts the 2D array into a 1D array with CS scores
    cs_sector = cosine_similarity(input_vec_sec, mtx_sector).flatten()
    cs_exp = cosine_similarity(input_vec_exp, mtx_exp).flatten()
    cs_jt = cosine_similarity(input_vec_jt, mtx_jt).flatten()
    cs_arr = cosine_similarity(input_vec_arr, mtx_arr).flatten()
    cs_desc = cosine_similarity(input_vec_desc, mtx_desc).flatten()
    cs_text = cosine_similarity(input_vec_text, mtx_text).flatten()

    # Assign cosine similarity: sector: 0.3, experience: 0.25, jobType: 0.1,
    # arrangement: 0.175, description: 0.1, cs_text: 0.075 (might change)
    cs_combined = (0.3 * cs_sector + 0.25 * cs_exp + 0.1 * cs_jt + 0.175
                   * cs_arr + 0.1 * cs_desc + 0.075 * cs_text)

    # Use index slicing to get the top 5 recommended lists
    top_indices = cs_combined.argsort()[-5:][::-1]

    # Return the top 5 job listings
    top_jobs = corpus_df.iloc[top_indices]
    # Convert the top 5 job listings from corpus_df to dictionary with
    # parameter orient = 'records" so each row represents a dictionary entry
    return top_jobs.to_dict(orient='records')
