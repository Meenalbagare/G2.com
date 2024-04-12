import spacy
from collections import defaultdict
from nltk.corpus import stopwords
import string
import requests


nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

def extract_requested_features(reviews):
    requested_features = defaultdict(list)

    for idx, review in enumerate(reviews):
        dislike_text = review['attributes']['comment_answers']['hate']['value']

       
        doc = nlp(dislike_text.lower().translate(str.maketrans('', '', string.punctuation)))

        actionable_insights = set()
        named_entities = set()
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG'] and ent.text.lower() != 'g2' and ent.text.lower() != "g2 marketing solutions'":
                named_entities.add(ent.text)
        for token in doc:
            if token.pos_ == "VERB":
                for child in token.children:
                    if child.pos_ == "NOUN":
                        actionable_insights.add(f"{token.lemma_} {child.text}")
        
        features = extract_features_from_review(dislike_text)

        dislike_number = idx + 1 
        requested_features[dislike_number].extend(list(actionable_insights))
        requested_features[dislike_number].extend(list(named_entities))
        requested_features[dislike_number].extend(features)

    return requested_features

def extract_features_from_review(text):
    
    doc = nlp(text.lower().translate(str.maketrans('', '', string.punctuation)))

   
    features = []

  
    for chunk in doc.noun_chunks:
       
        if len(chunk.text.split()) > 1 and any(token.dep_ in ['amod', 'nsubj', 'dobj', 'attr'] for token in chunk.root.head.children):
           
            filtered_chunk = ' '.join([token.text for token in chunk if token.text not in stop_words])
            if filtered_chunk and len(filtered_chunk.split()) > 1:
                features.append(filtered_chunk)

    return features

def fetch_reviews():
    url = "https://data.g2.com/api/v1/survey-responses"
    headers = {
        "Authorization": "Token token=785a71e4ec4ade9fd282aa7479541e171d150e1d8e4f6cba4db414ec8d746aef",
        "Content-Type": "application/vnd.api+json"
    }
    params = {
        "filters[product_name]": "G2 Marketing Solutions",
        "page[size]": 100
    }

    reviews = []

    while True:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            reviews.extend(data['data'])
            next_page = data['links'].get('next')
            if next_page:
                url = next_page
            else:
                break
        else:
            print("Failed to fetch reviews:", response.text)
            break

    dislikes = [review for review in reviews if 'hate' in review['attributes']['comment_answers']]

    return dislikes

def main():
    dislikes = fetch_reviews()
    if dislikes:
        print(f"Total dislikes fetched: {len(dislikes)}")
        features = extract_requested_features(dislikes)

        # Print extracted features for analysis
        for dislike_number, items in features.items():
            print(f"Features requested in dislike {dislike_number}:")
            for item in items:
                print(f" - {item}")
            if not items:
                print("No features")
    else:
        print("No dislikes fetched")

if __name__ == "__main__":
    main()
