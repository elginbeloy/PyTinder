# PyTinder V.1.2

See the project [Youtube Video](https://www.youtube.com/watch?v=nsJ96oejfXI)

### About PyTinder

PyTinder is a fun side-project that aims to automate the entire Tinder lifecycle, from swiping right to the date being setup.

PyTinder uses Selenium to automate interaction with the Tinder web interface. It then uses Seq2Seq LSTMs to communicate (chatbot) with 
Tinder users that have been matched. 

The chatbot LSTM used is inspired by: (https://github.com/tensorlayer/seq2seq-chatbot)

PyTinder consists of three bots:

1. LoginBot: It uses phone authentication to login the user with their SMS number.
2. SwipeBot: It uses basic Selenium find functions to continually swipe right.
3. ChatBot: It uses the LSTM mentioned above to chat with matched users.

 
### Usage

Download [chromedriver](http://chromedriver.chromium.org/downloads) for selenium into the current directory.

```shell
# Setup enviornment
python -m venv env
source ./env/bin/activate 
python -m pip install -r requirements.txt

python pytinder.py
```

