import time
import yfinance as yf
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By


def finance_data(quote='AAPL', interval = '1d'):
    # Récupération des données sur un an 
    quote = yf.Ticker(quote)
    hist = quote.history(period='1y', interval=interval)
    hist.drop(['Dividends','Stock Splits'], axis = 1, inplace = True)
    hist = hist.reset_index()
    
    date=[]
    for i in hist['Date']:
        date.append(i.date())
    hist['Date']=date
    
    # Récupération des données sur le dernier mois
    hist_analyse = quote.history(period='1mo', interval=interval)
    hist_analyse.drop(['Dividends','Stock Splits'], axis = 1, inplace = True)
    hist_analyse = hist_analyse.reset_index()
    
    date_temp = []
    avg = []
    for i in range(len(hist_analyse)):
        date_temp.append(hist_analyse['Date'][i].date())
        avg.append((hist_analyse['High'][i]+hist_analyse['Low'][i])/2)
    hist_analyse['Avg'] = avg
    
    var = []
    for i in hist_analyse['Avg']:
        var.append(((i/(hist_analyse['Avg'].sum()/hist_analyse.shape[0]))-1)*100)
        
    hist_analyse['Var'] = (var)
    return hist, hist_analyse

def scraping(nb_posts):
    start_time = time.time()
    #initialise mongo
    client = MongoClient('mongo')
    db = client["reddit_db"]
    reddit = db["reddit"]
    # reddit.delete_many({}) 
        
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("start-maximized")
    driver = webdriver.Remote(command_executor='http://192.168.65.4:4444',options=options)

    print ('driver created')
    driver.get("https://www.reddit.com/r/trading/")
    time.sleep(2)
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1
    print ('into the first loop')
    size_db = 0
    posts=driver.find_elements(By.XPATH, "//div[starts-with(@class, '_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh  Post')]")

    for post in posts:
        if size_db >= int(nb_posts): 
            break
        post_id = post.get_attribute('id')
        title = post.find_elements(By.XPATH, f"//div[@class='_2FCtq-QzlfuN-SwVMUZMM3 _3wiKjmhpIpoTE2r5KCm2o6 {post_id}']//div[@class='y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE']")[0].text
        if title != '' and len(post_id) < 15: #check if the title is not empty (if the post charged well), and if it's not an ad
            categorys = post.find_elements(By.XPATH, f"//div[@class='_2FCtq-QzlfuN-SwVMUZMM3 _3wiKjmhpIpoTE2r5KCm2o6 {post_id}']//span[@class='_1jNPl3YUk6zbpLWdjaJT1r _2VqfzH0dZ9dIl3XWNxs42y aJrgrewN9C8x1Fusdx4hh _1Dl-kvSxyJMWO9nuoTof8N ']")
            texts = post.find_elements(By.XPATH, f"//div[@id='{post_id}']//div[@class='_292iotee39Lmt0MkQZ2hPV RichTextJSON-root']")
            
        
            if len(categorys) >0: 
                category = categorys [0].text
            else:
                category = ''
                
            if len(texts) >0: 
                text = texts [0].text
            else:
                text = ''

            reddit.insert_one({
                'post_id':post_id,
                'title': title,
                'category': category,
                'text':text
        })
            last_elem = post
            size_db +=1
            
    print("end of first loop")
    print("into second loop")
    # print (last_elem.text)
    while size_db < int(nb_posts):
    #     print (i)
        # scroll one screen height each time
        driver.execute_script(f"window.scrollTo(0, {screen_height *i});")  
        # i += 0.5
        time.sleep(0.5)    
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    #     print (scroll_height)
    #     print (f"     {screen_height *i}")
        # if (i %5 ==0) :
        #     time.sleep(2)
        #     posts=driver.find_elements(By.XPATH, "//div[starts-with(@class, '_1oQyIsiPHYt6nx7VOmd1sz _1RYN-7H8gYctjOQeL8p2Q7 scrollerItem _3Qkp11fjcAw9I9wtLo8frE _1qftyZQ2bhqP62lbPjoGAh  Post')]")

        index_previous_last = posts.index(last_elem)
        for post in posts[index_previous_last:]:
            post_id = post.get_attribute('id')
            title = post.find_elements(By.XPATH, f"//div[@class='_2FCtq-QzlfuN-SwVMUZMM3 _3wiKjmhpIpoTE2r5KCm2o6 {post_id}']//div[@class='y8HYJ-y_lTUHkQIc1mdCq _2INHSNB8V5eaWp4P0rY_mE']")[0].text
            
            if title != '' and len(post_id) < 15: #check if the title is not empty (if the post charged well), and if it's not an ad
                categorys = post.find_elements(By.XPATH, f"//div[@class='_2FCtq-QzlfuN-SwVMUZMM3 _3wiKjmhpIpoTE2r5KCm2o6 {post_id}']//span[@class='_1jNPl3YUk6zbpLWdjaJT1r _2VqfzH0dZ9dIl3XWNxs42y aJrgrewN9C8x1Fusdx4hh _1Dl-kvSxyJMWO9nuoTof8N ']")
                texts = post.find_elements(By.XPATH, f"//div[@id='{post_id}']//div[@class='_292iotee39Lmt0MkQZ2hPV RichTextJSON-root']")
                if len(categorys) >0: 
                    category = categorys [0].text
                else:
                    category = ''
                    
                if len(texts) >0: 
                    text = texts [0].text
                else:
                    text = ''
                    
                reddit.insert_one({
                    'post_id':post_id,
                    'title': title,
                    'category': category,
                    'text':text
                })
                last_elem = post
                size_db +=1
                
                if size_db%10 ==0 : 
                    print(size_db)

        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break 
    
    driver.quit()
    print ('end of scraping')
    
    
def mongo_search(liste_entreprise, entreprise):
    
    #declaration variables
    n_post=0
    n_titre=0
    
    #selection entreprise
    row = liste_entreprise.loc[liste_entreprise['Companies'] == entreprise]
    result = row['Symbols'].iloc[0]
    
    #ouverture bdd monngo
    client = MongoClient('mongo')
    db = client["reddit_db"]
    reddit = db["reddit"]
    
    #creation index, recherche de terme, suppression index pour le Texte
    reddit.create_index([("text","text")])
    cur = reddit.find( { "$text": { "$search": result+" "+entreprise , "$caseSensitive": False} } )
    for i in cur:
        print(i)
        n_post+=1
    reddit.drop_index("text_text")
    
    #creation index, recherche de terme, suppression index pour le titre
    reddit.create_index([("title","text")])
    cur = reddit.find( { "$text": { "$search": result+" "+entreprise , "$caseSensitive": False} } )
    for i in cur:
        print(i)
        n_titre+=1
    reddit.drop_indexes()
    reddit.delete_many({}) 
    
    return n_post, n_titre