import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask, render_template, url_for, request, redirect
from script_selenium_new import scraping, mongo_search
from yf_data import finance_data

dow_jones = pd.read_csv('data/dow_jones_companies.csv',sep=',')

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def selection():
    nb_posts = [25,50,75,100,150]
    list_entreprises = dow_jones['Companies']
    selected_nb_post = None
    selected_entreprise = None
    if request.method == 'POST':
        selected_nb_post = int(request.form.get('posts'))
        selected_entreprise = request.form.get('entreprise')
        return redirect(url_for('scrap',
                                nb_post=selected_nb_post,
                                entreprise=selected_entreprise))
    return render_template('Accueil.html', nb_posts=nb_posts,
                        list_entreprises=list_entreprises,
                        selected_nb_post=selected_nb_post,
                        selected_entreprise=selected_entreprise)

@app.route('/scrap/<nb_post>&<entreprise>')
def scrap(nb_post,entreprise):
    # Scraping
    scraping(nb_posts=nb_post)
    
    # Analyse des posts
    n_post, n_titre = mongo_search(dow_jones,entreprise)
    post_bool = False
    if n_post + n_titre >= 1 :
        post_bool = True
    
    # Analyse de bourse avec API Yahoo finance
    row = dow_jones.loc[dow_jones['Companies'] == entreprise]
    result = row['Symbols'].iloc[0]
    df,analyse = finance_data(result)
    
    # Graphique analyse 
    fig = px.scatter(x=analyse['Date'],y=analyse['Avg'])
    fig.update_layout(title = f'Graphique des actions de {entreprise} sur le dernier mois',
                      xaxis_title = 'Date',
                      yaxis_title = 'Valeur boursière en $')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Graphique court de l'entreprise
    fig2 = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'])])
    fig2.update_layout(
        title=f'Analyse des actions de {entreprise} sur la dernière année',
        yaxis_title=f'{result} Stocks',
        shapes = [dict(
            x0='2023-01-19', x1='2023-01-19', y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x='2023-01-19', y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='right', text="Début de l'analyse")])
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('scrap.html',nb_post=nb_post,
                           entreprise=entreprise,
                           graphJSON=graphJSON,
                           graphJSON2=graphJSON2,
                           post_bool = post_bool,
                           n_post = n_post+n_titre)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port="5066")