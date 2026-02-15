import pandas as pd
import requests
import io
import sys
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

def download_data():
    """Downloads the Sports vs Politics dataset from your provided raw link."""
    print("Downloading dataset from your provided GitHub link...")
    url = "https://raw.githubusercontent.com/priyadip/sports-politics-classifier/refs/heads/main/data/sports_politics_dataset.csv"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        
        # Determine the correct column names 
        label_col = 'label' if 'label' in df.columns else ('category' if 'category' in df.columns else None)
        text_col = 'text' if 'text' in df.columns else ('content' if 'content' in df.columns else None)

        if not label_col or not text_col:
            raise KeyError(f"Missing required columns. Found: {df.columns.tolist()}")

        # Ensure we only have Sport and Politics (handling case sensitivity)
        df[label_col] = df[label_col].str.lower()
        df = df[df[label_col].isin(['sport', 'politics'])]
        
        print(f"Dataset loaded: {df.shape[0]} samples found.")
        return df, text_col, label_col

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def train_and_compare(df, text_col, label_col):
    """Trains and compares three ML techniques as required by Assignment-1."""
    # Feature Representation: TF-IDF with Bi-grams
    tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=4000)
    X = tfidf.fit_transform(df[text_col])
    y = df[label_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Required comparison of three techniques
    models = {
        "Multinomial Naive Bayes": MultinomialNB(),
        "SVM (Linear)": SVC(kernel='linear'),
        "Logistic Regression": LogisticRegression(max_iter=1000)
    }

    results = {}
    for name, model in models.items():
        print(f"\n--- {name} Performance ---")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        print(classification_report(y_test, preds))

        import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import confusion_matrix

    
    cm = confusion_matrix(y_test, preds)
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=['politics', 'sport'], yticklabels=['politics', 'sport'])
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix for SVM')
    plt.savefig('confusion_matrix.png')

    return results

if __name__ == "__main__":
    # Ensure standard libraries are installed: pip install pandas scikit-learn requests
    data, text_field, label_field = download_data()
    comparison_scores = train_and_compare(data, text_field, label_field)
    
    print("\n" + "="*40)
    print("QUANTITATIVE COMPARISON SUMMARY")
    print("="*40)
    for model_name, score in comparison_scores.items():
        print(f"{model_name:25}: {score:.4f} Accuracy")
