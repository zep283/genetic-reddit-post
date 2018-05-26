import numpy
import praw
from genetic import *

'''
    TODO:
    Implement loading from file
'''
class Memebot:
    def __init__(self):
        self.reddit = praw.Reddit(user_agent='memebot (by /u/zep283)',
                         client_id='_-BKvPKiIi10aQ', client_secret='aw5dMF0K5iOTytmHufySTDwfhg4',
                         username='zep283', password='iwillescape')
        self.subreddit = self.reddit.subreddit('circlejerk')
        self.titles = []
        self.scores = []
        self.text = []
        self.vocab = dict()
        self.average_len = 0

    def read_posts(self, sample_size=10):
        genny = self.subreddit.hot()
        for i in range(0, sample_size):
            post = genny.next()
            self.titles.append(post.title)
            self.scores.append(post.score)
            self.text.append(post.selftext)
        
    def create_data(self):
        vocab = []
        lengths = []
        num_titles = len(self.titles)
        for i in range(0, num_titles):
            sublist = self.titles[i].split(" ")
            num_words = len(sublist)
            lengths.append(num_words)
            for j in range(0, num_words):
                vocab.append(sublist[j])
        self.vocab = dict((c, i) for i, c in enumerate(vocab))
        self.average_len = int(round(numpy.array(lengths).mean()))
        #self.write_csv(word_freq)
        
    def write_csv(self, word_freq):
        with open('titles.csv', 'a', newline='') as csvfile:
            for key in word_freq: 
                line = key + ' : ' + str(word_freq[key]) + '\n'             
                csvfile.write(line)
                
    def run_genetics(self):
        #print(parse_grammar(self.titles))
        childs = run_evolution(10, self.vocab, self.average_len)
        
    
def main():
    agent = Memebot()
    agent.read_posts(20)
    agent.create_data()
    agent.run_genetics()
if __name__ == '__main__':
    main()                         
 
