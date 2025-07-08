# 📚 Books Recommendation System

A full-stack content-based recommendation system for books using Python, Flask, SQLite, and machine learning. This system recommends similar books based on genre, description, and user preferences.

---

## 🚀 Features

- 🔎 **Content-Based Filtering** using TF-IDF and Nearest Neighbors
- 📖 Recommends books with similar genres and descriptions
- 🌐 REST API with Flask for easy frontend integration
- 💾 Stores and retrieves user preferences using SQLite
- 🧑‍💼 Clerk authentication support (via API key)

---

## 📁 Project Structure

├── app.py # Flask backend server with Clerk & SQLite integration
├── content.py # Model training and recommendation logic
├── model.ipynb # Model building in Jupyter Notebook
├── books.ipynb # Additional analysis and exploration
├── collabrative.ipynb # (Optional) Collaborative filtering experiments
├── GoodReads_100k_books.csv # Dataset used for training (not pushed to GitHub)
├── requirements.txt # Python dependencies (create this if missing)

---

## 🧠 How It Works

- Text data (description + genres) is processed with `TfidfVectorizer`.
- Genres are one-hot encoded using `MultiLabelBinarizer`.
- Features are combined and fitted into a KNN model.
- Given a book title, similar books are recommended based on cosine similarity.

---

## 🔧 Setup Instructions

### 1. Clone the repo
git clone https://github.com/sahith2613/Books_Recommendation_System.git
cd Books_RecommendationSystem
2. Install Python dependencies
pip install -r requirements.txt
If requirements.txt is missing, install manually:
pip install flask pandas numpy scikit-learn matplotlib seaborn python-dotenv requests pillow
3. Run the Flask API
python app.py
The server will run at:
http://127.0.0.1:5000
