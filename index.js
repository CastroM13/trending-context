const express = require('express');
const { Builder, By, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

const app = express();

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
})

app.get('/topic/:topic', (req, res) => {
  res.sendFile(__dirname + '/topic.html');
})

app.get('/trending', async (req, res) => {
  try {
    const options = new chrome.Options();
    options.addArguments('--window-size=1920,1080');
    options.addArguments('--headless'); // Run Chrome in headless mode (no GUI)

    const driver = await new Builder()
      .forBrowser('chrome')
      .setChromeOptions(options)
      .build();

    try {
      await driver.get('https://twitter.com/i/trends');

      await driver.wait(
        until.elementLocated(By.xpath('//section[contains(@role, "region")]')),
        10000
      );

      const trendingTopics = await driver.findElements(
        By.xpath('//div[@data-testid="trend"]//span')
      );

      const topics = [];
      for (let i = 0; i < trendingTopics.length; i++) {
        const topic = await trendingTopics[i].getText();
        if (!topic.includes('Assunto') && !topic.includes('Tweets') && !topic.includes('Trending')) {
          topics.push(topic);
        }
      }

      res.json({ topics });
    } finally {
      await driver.quit();
    }
  } catch (error) {
    console.error('An error occurred:', error);
    res.status(500).json({ error: 'An error occurred' });
  }
});
app.get('/topic/trending/:topic', async (req, res) => {
  try {
    const topic = req.params.topic;
    const options = new chrome.Options();
    options.addArguments('--window-size=1080,1920');
    options.addArguments('--user-data-dir=C:/Users/mathe/AppData/Local/Google/Chrome/User Data/');
    options.addArguments('--headless'); // Run Chrome in headless mode (no GUI)

    const driver = await new Builder()
      .forBrowser('chrome')
      .setChromeOptions(options)
      .build();

    try {
      await driver.get(`https://twitter.com/search?q=${topic}&src=typed_query`);
      
      await driver.sleep(3000);

      const articles = await driver.findElements(By.css("*[data-testid=tweetText]"))
      

      const tweets = [];
      for (let i = 0; i < articles.length; i++) {
        const tweet = await articles[i].getText();
        tweets.push(tweet);
      }

      res.json({ tweets });
    } finally {
      await driver.quit();
    }
  } catch (error) {
    console.error('An error occurred:', error);
    res.status(500).json({ error: 'An error occurred' });
  }
});

const forbidden = value =>
  ![
    "Replying to",
    "@"
  ].some(element => value.includes(element));

app.listen(3000, () => {
  console.log('Server is running on http://localhost:3000');
});
