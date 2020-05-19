from sklearn.feature_extraction.text import TfidfVectorizer 
from nltk import word_tokenize, pos_tag
from spacy import load
from textblob import TextBlob
from common import check_wordset

def get_only_entity(key, ner_model):
    plural = False
    key_nlp = ner_model(key)
    label = key_nlp.ents
    before, after = '', ''
    if not label:
       if key[-1] == 's':
           label = ner_model(key[:-1]).ents
           if label :
               plural = True
    if label:
        ent = label[0].text
        label = label[0].label_
        if plural:
          ent += 's'
#         print(key,'key', ent, 'ent')
        before = key[:key.index(ent)]
        after = key[key.index(ent)+len(ent):]
        key = ent
    return before, key, after, plural, label

def get_context(key, sentence):
    context_tags = []
    context = sentence[:sentence.index(key)] + "." +sentence[sentence.index(key)+len(key):]
    context = context.split(".")[0].split()[-2:] + context.split(".")[1].split()[:2]
    for word in context:
        tag = pos_tag(word_tokenize(word))[0][1] 
        context_tags.append(tag)
    return context_tags

def get_candidates(chapter_sentences, key, ner_model, key_label):
    distractor_candidates = []
    candidate_sentences = []
    if key_label:
        for sentence in chapter_sentences:
            sentence = sentence.lower()
            doc = ner_model(sentence)
            for ent in doc.ents:
                if ent.label_ == key_label:
                    distractor_candidates.append(ent.text)
                    candidate_sentences.append(sentence)
    else:
#         print("didnt find an entity in ",key)
        key_tags = [i[1] for i in pos_tag(word_tokenize(key))]
        for sentence in chapter_sentences:
            sentence = sentence.lower()
            doc = pos_tag(word_tokenize(sentence))
            for ent in doc:
                if ent[1] in key_tags:
                    distractor_candidates.append(ent[0])
                    candidate_sentences.append(sentence)
    return distractor_candidates, candidate_sentences

def get_tfidf(chapter_sentences, key):
    tfidf_vectorizer=TfidfVectorizer(tokenizer=word_tokenize)
    tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform([i.lower() for i in chapter_sentences])
    words = tfidf_vectorizer.get_feature_names()
    scores = tfidf_vectorizer_vectors.sum(axis=0).A1
    result = dict(zip(words,scores))
    key_score = sum([result[key.split()[i]] for i in range(len(key.split())) if key.split()[i] in result.keys()])/len(key.split())
    return result, key_score

def sentence_similarity(sentence, s_candidate):
    return sum([2 for i in s_candidate if i in sentence])/(len(sentence.split())+len(s_candidate.split()))

def context_similarity(key_context, sent_cand, cand):
    context_tags_similarity = 0
    context = sent_cand[:sent_cand.index(cand)] + "." +sent_cand[sent_cand.index(cand)+len(cand):]
    candidate_context = context.split(".")[0].split()[-2:] + context.split(".")[1].split()[:2]
    for word in [0,1,2,3]:
        if len(candidate_context) > word and len(key_context) > word:
            tag = pos_tag(word_tokenize(candidate_context[word]))[0][1]
            context_tags_similarity -= int(tag != key_context[word])    
    return context_tags_similarity
    
def tfidf_difference(result, key_score, cand):
    return (sum([result[cand.split()[i]] for i in range(len(cand.split())-1)])/len(cand.split()) - key_score + 1)/2   

def get_distractors(chapter_sentences, key, key_sent, ner_model, num_distractors=3):
    key_sent = key_sent.replace(".","")
    before_key, key, after_key, plural, key_label = get_only_entity(key, ner_model)
    new_key = [before_key, key, after_key]
    distractor_candidates, candidate_sentences = get_candidates(chapter_sentences, key, ner_model, key_label)
    try:
        key_context = get_context(key, key_sent)
    except:
        return 
    tfidf, key_score = get_tfidf(chapter_sentences, key)
    scores_final = []
    for cand, sent in zip(distractor_candidates, candidate_sentences):
        if ((cand not in key and key not in cand and any(i for i in cand if i 
            not in key_sent)) or key_label == 'mtrx') and check_wordset(cand) \
            and cand != key and cand not in key_sent:
            sent_simil = sentence_similarity(key_sent, sent)
            context_simil = context_similarity(key_context, sent, cand)
            diff_score = tfidf_difference(tfidf, key_score, cand)
            score = [sent_simil + context_simil/4 - diff_score, cand]
            scores_final.append(score)
    scores_final = sorted(scores_final,key=lambda x: x[0],reverse=True)
    max_scores = []
    for score in scores_final:
        if score[1] not in [j for i in max_scores for j in i.split()]\
             and score[1] not in max_scores:
            max_scores.append(score[1])
    for i in range(len(max_scores)):
        if plural:
            words = max_scores[i].split()
            max_scores[i] = ''
            if len(words) > 1:
                max_scores[i] = " ".join(words[:-1]) + " "
            max_scores[i] += str(TextBlob(words[-1]).words[0].pluralize())
    return max_scores[:num_distractors], new_key