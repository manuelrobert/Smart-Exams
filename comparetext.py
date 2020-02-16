import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy import spatial


nlp=spacy.load("en_core_web_sm")


def remove_stop_words(string1,string2):
	example_sent1 = string1
	example_sent2 = string2
	print(example_sent1)
	print(example_sent2)
	stop_words = set(stopwords.words('english'))

	word_tokens1 = word_tokenize(example_sent1)
	word_tokens2 = word_tokenize(example_sent2)

	filtered_sentence1 = [w for w in word_tokens1 if not w in stop_words]
	filtered_sentence1 = []

	for w in word_tokens1:
		if w not in stop_words:
			filtered_sentence1.append(w)

	print(example_sent1)
	print(word_tokens1)
	print(filtered_sentence1)



	filtered_sentence2 = [w for w in word_tokens2 if not w in stop_words]
	filtered_sentence2 = []

	for w in word_tokens2:
		if w not in stop_words:
			filtered_sentence2.append(w)

	print(example_sent2)
	print(word_tokens2)
	print(filtered_sentence2)

	pro_text={
	"f1":filtered_sentence1,
 	"f2":filtered_sentence2
 	}
	return pro_text



def get_cosine_similarity(string1,string2):
	c1 = len(string1)
	c2 = len(string2)
	vector1 = []
	vector2 = []

	if c1 == c2:
		for word in string1:
			print("string1",word)
			vector1 = vector1 + (list(nlp(word).vector))
		for word in string2:
			print("string2",word)
			vector2 = vector2 + list(nlp(word).vector)

	elif c1 < c2:
		for i in range(c1,c2):
			string1.append('none')
		for word in string1:
			print("string1",word)
			vector1 = vector1 + (list(nlp(word).vector))
		for word in string2:
			print("string2",word)
			vector2 = vector2 + list(nlp(word).vector)

	elif c2 < c1:
		for i in range(c2,c1):
			string2.append('none')
		for word in string1:
			print("string1",word)
			vector1 = vector1 + (list(nlp(word).vector))
		for word in string2:
			print("string2",word)
			vector2 = vector2 + list(nlp(word).vector)

	result= 1 - spatial.distance.cosine(vector1,vector2)
	print("Similarity",result)
	return result