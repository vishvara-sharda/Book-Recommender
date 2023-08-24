# %%
import pandas as pd
import numpy as np
import itertools

# %%
df_books=pd.read_csv('data/books.csv', low_memory=False)
df_users=pd.read_csv('data/users.csv')
df_ratings=pd.read_csv('data/ratings.csv')

# %% [markdown]
#   # Popularity Based Recommender System

# %%
ratings = df_ratings.merge(df_books, on='ISBN', validate=None)

# %%
ratings.shape

# %%
rating_of_books=ratings.groupby('Book-Title').count()['Book-Rating'].reset_index()
rating_of_books.rename(columns={'Book-Rating':'Rating_of_Books'},inplace=True)

# %%
average_ratings=ratings.groupby('Book-Title').mean(numeric_only=True)['Book-Rating'].reset_index()
average_ratings.rename(columns={'Book-Rating':'Average_Ratings'},inplace=True)

# %%
df_popularity=rating_of_books.merge(average_ratings,on='Book-Title')
df_popularity
# %%
df_popularity=df_popularity[df_popularity['Rating_of_Books']>=525].sort_values('Average_Ratings',ascending=False).head(30)

# %%

# %%
df_popularity=df_popularity.merge(df_books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-M','Rating_of_Books','Average_Ratings']]

# %%
df_books=df_books.merge(df_ratings,on='ISBN')

# %% [markdown]
# # Content Based Filtering

# %%
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def content_based_recommender(book_title, df):
    book_title = str(book_title)
    recommendations = []

    if book_title in df['Book-Title'].values:
        rating_counts = pd.DataFrame(df['Book-Title'].value_counts())
        rare_books = rating_counts[rating_counts['count'] <= 5].index
        common_books = df[~df['Book-Title'].isin(rare_books)]

        if book_title in rare_books:
            random = pd.Series(common_books['Book-Title'].unique()).sample(2).values
            print('There are no recommendations for this book')
            print('Try: \n')
            print('{}'.format(random[0]), '\n')
            print('{}'.format(random[1]), '\n')
        else:
            common_books = common_books.drop_duplicates(subset=['Book-Title'])
            common_books.reset_index(inplace=True)
            common_books['index'] = [i for i in range(common_books.shape[0])]
            target_cols = ['Book-Author', 'Publisher']  # Consider using relevant features
            common_books['combined_features'] = common_books[target_cols].apply(lambda row: ' '.join(row), axis=1)
            
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(common_books['combined_features'])
            cosine_sim = cosine_similarity(tfidf_matrix)
            
            index = common_books[common_books['Book-Title'] == book_title]['index'].values[0]
            sim_books = list(enumerate(cosine_sim[index]))
            sorted_sim_books = sorted(sim_books, key=lambda x: x[1], reverse=True)[1:6]
            
            for i in range(len(sorted_sim_books)):
                recom_book_index = sorted_sim_books[i][0]
                recom_book_info = common_books.iloc[recom_book_index]
                recommendations.append([recom_book_info['Book-Title'], recom_book_info['Book-Author'], recom_book_info['Image-URL-M']])
            
    else:
        print('Cant find book in dataset, please check spelling')
    
    return recommendations

# %%
y = ratings.groupby('User-ID').count()['Book-Rating'] > 200
users = y[y].index

# %%
filtered_ratings = ratings[ratings['User-ID'].isin(users)]

# %%
z = filtered_ratings.groupby('Book-Title').count()['Book-Rating']>=50
popular_book = z[z].index

# %%
final_ratings = filtered_ratings[filtered_ratings['Book-Title'].isin(popular_book)]

# %%
pt = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')

# %%
pt.fillna(0,inplace=True)

# %%
pt

# %%
from sklearn.metrics.pairwise import cosine_similarity

# %%
similarity_scores = cosine_similarity(pt)

# %%
from fuzzywuzzy import process

def recommend(book_name):
    close_matches = process.extractBests(book_name, pt.index, score_cutoff=70)

    if not close_matches:
        print("No recommendations available for this book.")
        return []

    # Select the first match with the highest similarity score
    best_match, score = close_matches[0]

    index = np.where(pt.index == best_match)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = pt.index[i[0]]
        temp_df = df_books[df_books['Book-Title'] == item]
        item_data = [item, temp_df['Book-Author'].values[0], temp_df['Image-URL-M'].values[0]]
        data.append(item_data)

    return data


# %%
pt.index[545]

# %%
# recommend("1984")

# %%
df_books.drop_duplicates('Book-Title')


# %% [markdown]
# # Hybird Based Filtering

# %%
def hybrid_recommendation(book_name, num_recommendations=5):
    recommended_books_collab = recommend(book_name)
    recommended_books_content = content_based_recommender(book_name, df_books)

    if recommended_books_content is None:
        recommended_books_content = []

    recommended_books_collab_flat = list(itertools.chain.from_iterable(recommended_books_collab))
    recommended_books_content_flat = list(itertools.chain.from_iterable(recommended_books_content))

    recommended_books_collab_set = set(recommended_books_collab_flat)
    recommended_books_content_set = set(recommended_books_content_flat)

    combined_recommendations_set = recommended_books_collab_set.union(recommended_books_content_set)

    number = num_recommendations
    k = float(1 / number)
    hybrid_scores = [1 - k * x for x in range(len(combined_recommendations_set))]

    dictISBN = {}
    for x in recommended_books_collab_set:
        if x in combined_recommendations_set:
            dictISBN[x] = hybrid_scores[list(combined_recommendations_set).index(x)]

    for x in recommended_books_content_set:
        if x in combined_recommendations_set:
            if x not in dictISBN:
                dictISBN[x] = hybrid_scores[list(combined_recommendations_set).index(x)]
            else:
                dictISBN[x] += hybrid_scores[list(combined_recommendations_set).index(x)]

    ISBN = dict(sorted(dictISBN.items(), key=lambda x: abs(x[1]), reverse=True))
    recommended_books = list(ISBN.keys())

    books_list = []
    for book in recommended_books:
        if len(book) > 1 and not book.endswith("jpg"):
            book_info = df_books[df_books['Book-Title'] == book]
            if not book_info.empty:
                author_name = book_info['Book-Author'].values[0]
                image_url = book_info['Image-URL-M'].values[0]
                books_list.append([book, author_name, image_url])

    return books_list[:num_recommendations]



# %%
df_books

# %%
df_users["Age"].isnull().sum()

# %%
df_books.columns.unique()

# %%
df_users

# %%
df_users["Location"].isnull().sum()

# %%
df_books["Year-Of-Publication"].unique()

# %%
df_books["Year-Of-Publication"] = df_books["Year-Of-Publication"].map({'DK Publishing Inc' : "2001" , 'Gallimard' : "2005" })

# %%
df_books["Year-Of-Publication"]

# %%
df_books["Year-Of-Publication"].unique()

