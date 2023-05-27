import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/trending', methods=['GET'])
def get_trending():
    try:
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)

        driver = webdriver.Chrome(options=options)

        try:
            driver.get('https://twitter.com/i/trends')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//section[contains(@role, "region")]'))
            )

            trending_topics = driver.find_elements(By.XPATH, '//div[@data-testid="trend"]//span')

            topics = []
            for topic in trending_topics:
                topic_text = topic.text
                if 'Assunto' not in topic_text and 'Tweets' not in topic_text and 'Trending' not in topic_text:
                    topics.append(topic_text)

            return jsonify({'topics': topics})

        finally:
            driver.quit()

    except Exception as error:
        print('An error occurred:', error)
        return jsonify({'error': 'An error occurred'}), 500

@app.route('/trending/<topic>', methods=['GET'])
def get_topic_tweets(topic):
    try:
        options = Options()
        options.add_argument('--window-size=1920,1080')
        # options.add_argument('--headless') # Run Chrome in headless mode (no GUI)

        driver = webdriver.Chrome(options=options)

        try:
            driver.get('https://twitter.com/i/flow/login')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=text]'))
            )
            user = driver.find_element(By.CSS_SELECTOR, 'input[type=text]')
            user.send_keys('bottrendingco')
            driver.execute_async_script('Array.of(...document.querySelectorAll("span")).find(el => el.innerText === "Avançar").click()')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name=password]'))
            )
            password = driver.find_element(By.CSS_SELECTOR, 'input[name=password]')
            password.send_keys('5398Trending@')
            driver.execute_async_script('Array.of(...document.querySelectorAll("span")).find(el => el.innerText === "Entrar")?.click()')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
            )

            driver.get(f'https://twitter.com/search?q={topic}&src=typed_query')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
            )

            articles = driver.find_elements(By.CSS_SELECTOR, 'article')

            tweets = []
            for article in articles:
                tweet = article.text
                tweets.append(tweet)

            return jsonify({'tweets': tweets})

        finally:
            driver.quit()

    except Exception as error:
        print('An error occurred:', error)
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
    print('Server is running on http://localhost:3000')
