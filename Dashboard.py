import pandas as pd
from flask import Flask, render_template, url_for, request,redirect
from markupsafe import escape
from script_selenium_new import scraping, mongo_search
from yf_data import finance_data

dow_jones = pd.read_csv('data/dow_jones_companies.csv',sep=',')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test', methods=['GET','POST'])
def selection():
    nb_posts = [25,50,75,100,150]
    list_entreprises = dow_jones['Companies']
    selected_nb_post = None
    selected_entreprise = None
    if request.method == 'POST':
        selected_nb_post = int(request.form.get('posts'))
        selected_entreprise = request.form.get('entreprise')
        return redirect(url_for('scrap',nb_post=selected_nb_post,entreprise=selected_entreprise))
    return render_template('test.html', nb_posts=nb_posts,
                        list_entreprises=list_entreprises,
                        selected_nb_post=selected_nb_post,
                        selected_entreprise=selected_entreprise)

@app.route('/scrap/<nb_post>&<entreprise>')
def scrap(nb_post,entreprise):
    row = dow_jones.loc[dow_jones['Companies'] == entreprise]
    result = row['Symbols'].iloc[0]
    print(result)
    finance_data(result)
    scraping(nb_posts=nb_post)
    n_post,n_titre = mongo_search(dow_jones,entreprise)
    print(n_post)
    print(n_titre)
    
    return render_template('scrap.html',nb_post=nb_post,entreprise=entreprise)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port="5066")