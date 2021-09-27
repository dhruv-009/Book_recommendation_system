from django.shortcuts import render
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn import neighbors


def func():
    features_df = pd.read_csv('static/features.csv')
    min_max_scaler = MinMaxScaler()
    features = min_max_scaler.fit_transform(features_df)
    model = neighbors.NearestNeighbors(n_neighbors=6, algorithm='ball_tree')
    model.fit(features)
    dist, idlist = model.kneighbors(features)
    return idlist


def BookRecommender(book_name,idlist):
    book_df = pd.read_csv('static/books.csv')
    book_list = []
    book_id = book_df[book_df['title'] == book_name].index
    book_id = book_id[0]
    for newid in idlist[book_id]:
         book_list.append(newid)
    return book_list

def index(requests):
    df = pd.read_csv('static/books.csv')
    context ={'bname': list(df['title']),'bsearch':''}
    if requests.method == 'POST':
        book_name = requests.POST.get('search')
        context['bsearch'] = book_name
        idlist=func()
        try:
            books_list = BookRecommender(book_name,idlist)
            books =[]
            book_features = df.columns
            for book_id in books_list:
                temp = {}
                for feature in book_features:
                    temp[feature] = df.loc[book_id][feature]
                books.append(temp)
            context['books'] = books
        except:
            print('No Books!')
        return render(requests,'books/index.html',context=context)
    return render(requests,'books/index.html',context=context)






