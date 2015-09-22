import tweepy, time, sys, random, string


class Markov(object):

    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()


    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words


    def triples(self):
        """ Generates triples from the given data string. So if our string were
                "What a lovely day", we'd generate (What, a, lovely) and then
                (a, lovely, day).
        """

        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, size=10):
        seed = random.randint(0, self.word_size-3)
        while ( not (self.words[seed-1].endswith("."))):
                seed = random.randint(0, self.word_size-3)

        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        i = 0
        gen_words.append(w1)
        while ((not (gen_words[len(gen_words)-1].endswith("."))) or i < size):
            w1, w2 = w2, random.choice(self.cache[(w1, w2)])
            gen_words.append(w1)
            i += 1
        return ' '.join(gen_words)



consumer_key = "CONSUMERKEY"
consumer_secret = "CONSUMERSECRET"
access_key = "ACCESSKEY"
access_secret = "ACCESSSECRET"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

markov_file = open(sys.argv[1])
markov_obj = Markov(markov_file)

#loop forever
while True:
	#generate a random string.
	t = filter(lambda x: x in string.printable, markov_obj.generate_markov_text())
	
	#make sure it meets some conditions. if not, regenerate it.
	while((len(t) > 139) or ("http" in t) or ("www" in t) or t.startswith(".")):
		t = filter(lambda x: x in string.printable, markov_obj.generate_markov_text())
	
	print t
	print "\n"
	
        api.update_status(status=t)
        time.sleep(43200)#43200 = 12 hr
