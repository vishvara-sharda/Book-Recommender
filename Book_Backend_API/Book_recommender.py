#!/usr/bin/env python
# coding: utf-8

# In[25]:


import pandas as pd
import numpy as np


# In[26]:


df_books=pd.read_csv('books.csv', low_memory=False)
df_users=pd.read_csv('users.csv')
df_ratings=pd.read_csv('ratings.csv')


# In[27]:


df_books.head()


# In[28]:


df_users.head()


# In[29]:


df_ratings.head()


# In[30]:


df_books.head(1)['Image-URL-M'].values


# In[31]:


print(df_books.shape)
print(df_users.shape)
print(df_ratings.shape)


# In[32]:


df_books.isnull().sum()


# In[33]:


df_users.isnull().sum()


# In[34]:


df_ratings.isnull().sum()


# In[35]:


df_books.duplicated().sum()


# In[36]:


df_ratings.duplicated().sum()


# In[37]:


df_users.duplicated().sum()


#   # Popularity Based Recommender System

# In[38]:


ratings = df_ratings.merge(df_books, on='ISBN', validate=None)
ratings


# In[39]:


ratings.shape


# In[40]:


rating_of_books=ratings.groupby('Book-Title').count()['Book-Rating'].reset_index()
rating_of_books.rename(columns={'Book-Rating':'Rating_of_Books'},inplace=True)
rating_of_books


# In[41]:


average_ratings=ratings.groupby('Book-Title').mean(numeric_only=True)['Book-Rating'].reset_index()
average_ratings.rename(columns={'Book-Rating':'Average_Ratings'},inplace=True)
average_ratings


# In[42]:


df_popularity=rating_of_books.merge(average_ratings,on='Book-Title')
df_popularity


# In[43]:


df_popularity


# In[44]:


df_popularity=df_popularity[df_popularity['Rating_of_Books']>=525].sort_values('Average_Ratings',ascending=False).head(30)
df_popularity


# In[45]:


df_popularity.shape


# In[46]:


df_popularity=df_popularity.merge(df_books, on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-M','Rating_of_Books','Average_Ratings']]



# In[47]:


df_books


# In[48]:


df_ratings


# In[49]:


df_books=df_books.merge(df_ratings,on='ISBN')


# In[50]:


df_books


# # Content Based Filtering

# In[51]:


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
            print(recom_books)
            return recom_books
                     
    else:
        
        return 'Cant find book in dataset, please check spelling'
# content_based_recommender('The Da Vinci Code', df_books)  s


# # Collobrative Filtering 

# In[52]:


y = ratings.groupby('User-ID').count()['Book-Rating'] > 200
users = y[y].index


# In[53]:


filtered_ratings = ratings[ratings['User-ID'].isin(users)]


# In[54]:


z = filtered_ratings.groupby('Book-Title').count()['Book-Rating']>=50
popular_book = z[z].index


# In[55]:


final_ratings = filtered_ratings[filtered_ratings['Book-Title'].isin(popular_book)]


# In[56]:


pt = final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')


# In[57]:


pt.fillna(0,inplace=True)


# In[58]:


pt


# In[59]:


from sklearn.metrics.pairwise import cosine_similarity


# In[60]:


similarity_scores = cosine_similarity(pt)


# In[61]:


def recommend(book_name):
    # index fetch
    index = np.where(pt.index==book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = df_books[df_books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    return data


# In[62]:


# recommend('1984')


# In[63]:


pt.index[545]


# In[64]:


import pickle
pickle.dump(df_popularity,open('popular.pkl','wb'))


# In[65]:


df_books.drop_duplicates('Book-Title')


# # Hybird Based Filtering

# In[66]:


# hybrid_recommendation

import itertools
import numpy as np

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
    print("Recommended Books:\n")
    bookList = []
    for book in recommended_books:
        if len(book) > 1:
            if not book.endswith("jpg"):
                print(book)
                bookList.append(book)
            if book in df_books['Book-Title'].values:
                image_url = df_books[df_books['Book-Title'] == book]['Image-URL-M'].values[0]
                print(image_url)
                bookList.append(image_url)

    return bookList

# Test the hybrid recommendation function
book_name = '1st to Die: A Novel'
# hybrid_recommendation(book_name)


# In[67]:


df_books


# In[68]:


df_users["Age"].isnull().sum()


# In[69]:


df_books.columns.unique()


# In[70]:


df_users


# In[71]:


df_users["Location"].isnull().sum()


# In[72]:


df_books["Year-Of-Publication"].unique()


# In[73]:


df_books["Year-Of-Publication"] = df_books["Year-Of-Publication"].map({'DK Publishing Inc' : "2001" , 'Gallimard' : "2005" })


# In[74]:


df_books["Year-Of-Publication"]


# In[75]:


df_books["Year-Of-Publication"].unique()

