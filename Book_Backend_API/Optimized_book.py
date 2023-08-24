import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools

# Load data
df_books = pd.read_csv('data/books.csv', low_memory=False)
df_ratings = pd.read_csv('data/ratings.csv')

# Popularity-Based Recommender
rating_of_books = df_ratings.groupby('ISBN').count()['Book-Rating'].reset_index()
rating_of_books.rename(columns={'Book-Rating': 'Rating_of_Books'}, inplace=True)

average_ratings = df_ratings.groupby('ISBN').mean(numeric_only=True)['Book-Rating'].reset_index()
average_ratings.rename(columns={'Book-Rating': 'Average_Ratings'}, inplace=True)

df_popularity = rating_of_books.merge(average_ratings, on='ISBN')
df_popularity = df_popularity[df_popularity['Rating_of_Books'] >= 525].sort_values('Average_Ratings', ascending=False).head(30)
df_popularity = df_popularity.merge(df_books, on='ISBN')[['Book-Title', 'Book-Author', 'Image-URL-M', 'Rating_of_Books', 'Average_Ratings']]

# Content-Based Recommender

def content_based_recommender(book_title, df):
    
    book_title = str(book_title)
    if book_title in df_books['Book-Title'].values:
        rating_counts = pd.DataFrame(df_books['Book-Title'].value_counts())
        rare_books = rating_counts[rating_counts['count'] <= 5].index
        common_books = df_books[~df_books['Book-Title'].isin(rare_books)]
        print(rare_books.shape)
        print(common_books.shape)
        
        if book_title in rare_books:
            
            random = pd.Series(common_books['Book-Title'].unique()).sample(2).values
            print('There are no recommendations for this book')
            print('Try: \n')
            print('{}'.format(random[0]),'\n')
            print('{}'.format(random[1]),'\n')
        
        else:
            
            common_books = common_books.drop_duplicates(subset=['Book-Title'])
            common_books.reset_index(inplace= True)
            common_books['index'] = [i for i in range(common_books.shape[0])]
            target_cols = ['Book-Title', 'Book-Author','Publisher']
            common_books['combined_features'] = [' '.join(common_books[target_cols].iloc[i,].values) for i in range(common_books[target_cols].shape[0])]
            cv = CountVectorizer()
            count_matrix = cv.fit_transform(common_books['combined_features'])
            cosine_sim = cosine_similarity(count_matrix)
            index = common_books[common_books['Book-Title'] == book_title]['index'].values[0]
            sim_books = list(enumerate(cosine_sim[index]))
            sorted_sim_books = sorted(sim_books,key=lambda x:x[1],
                                      reverse=True)[1:6]
            
            recom_books = []
            for i in range(len(sorted_sim_books)):
                recom_books.append(common_books[common_books['index'] == sorted_sim_books[i][0]]['Book-Title'].item())
            return recom_books
                     
    else:
        
        return 'Cant find book in dataset, please check spelling'

# Collaborative Filtering
def recommend(book_name):
    if book_name in pt.index:
        index = np.where(pt.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        data = []
        for i in similar_items:
            item = []
            temp_df = df_books[df_books['ISBN'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        return data
    else:
        return []

y = df_ratings.groupby('User-ID').count()['Book-Rating'] > 200
users = y[y].index

filtered_ratings = df_ratings[df_ratings['User-ID'].isin(users)]

z = filtered_ratings.groupby('ISBN').count()['Book-Rating'] >= 50
popular_books = z[z].index

final_ratings = filtered_ratings[filtered_ratings['ISBN'].isin(popular_books)]

pt = final_ratings.pivot_table(index='ISBN', columns='User-ID', values='Book-Rating')
pt.fillna(0, inplace=True)

similarity_scores = cosine_similarity(pt)

# Hybrid Recommender
# Hybrid Recommender
def hybrid_recommendation(book_name, num_recommendations=5):
    book_title = str(book_name)
    if book_title in df_books['Book-Title'].values:
        recommended_books_collab = recommend(book_name)
        recommended_books_content = content_based_recommender(book_name, df_books)

        if recommended_books_content is None:
            recommended_books_content = []

        recommended_books_collab_flat = list(itertools.chain.from_iterable(recommended_books_collab))
        recommended_books_content_flat = list(itertools.chain.from_iterable(recommended_books_content))

        recommended_books_collab_set = set(recommended_books_collab_flat)
        recommended_books_content_set = set(recommended_books_content_flat)

        print("recommended_books_collab_set:", recommended_books_collab_set)
        print("recommended_books_content_set:", recommended_books_content_set)

        combined_recommendations_set = recommended_books_collab_set.union(recommended_books_content_set)

        print("combined_recommendations_set:", combined_recommendations_set)
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

        ISBN = dict(sorted(dictISBN.items(), key=lambda x: x[1], reverse=True))

        recommended_books_with_images = []
        for x in ISBN.keys():
            if x in df_books['Book-Title'].values:
                image_url = df_books[df_books['Book-Title'] == x]['Image-URL-M'].values[0]
                recommended_books_with_images.append((x, image_url))

        return recommended_books_with_images[:num_recommendations]

    else:
        return "Book not found"

# Call the hybrid_recommendation function
recommended_books = hybrid_recommendation("1984")

for book_name, image_url in recommended_books:
    print("Book:", book_name)
    print("Image URL:", image_url)
    print("\n")
    
print(recommend("1984"))