# AI-Projects
📧 Spam Email Classification System
A production-grade Machine Learning system designed to classify emails as Spam or Ham (legitimate). This project uses a modular pipeline architecture for training and inference and integrates a modern Streamlit web interface for easy interaction.
🚀 Key Features
* Advanced ML Pipeline Modular design separating:
   * Data ingestion
   * Data transformation
   * Model training
* Multiple Model Support Supports and evaluates:
   * SVM
   * Logistic Regression
   * Decision Trees
   * Random Forest
* Interactive Web UI Built using Streamlit for:
   * Real-time email classification
   * Batch processing
* MBOX Support Ability to process entire .mbox email archives
* Detailed Analytics Provides:
   * Precision
   * Recall
   * F1-Score
   * Logging and performance tracking
🛠️ Tech Stack
* Language: Python 3.10+
* Frontend: Streamlit
* ML Framework: Scikit-learn
* Data Processing: Pandas, NumPy
* Text Processing: BeautifulSoup4
* Project Management: uv / pip
📂 Project Structure

Spam-Email-Detection/

├── app.py                  # Main Streamlit Web Application
├── requirements.txt        # Project dependencies
├── main.py                 # Optional entry point

├── src/
│   ├── components/         # Data ingestion & transformation
│   ├── pipeline/           # Training & prediction pipelines
│   ├── config/             # Configuration settings
│   └── utils/              # Helper functions & logging

├── data/                   # Dataset storage
├── outputs/                # Saved models & vectorizers
└── logs/                   # Runtime logs
⚡ Installation
1. Clone the Repository

git clone <repository_url>
cd Spam-Email-Detection
Create Virtual Environment
python -m venv .venv
Activate Environment
* Windows:

.venv\Scripts\activate
Mac/Linux:
source .venv/bin/activate
Install Dependencies
pip install -r requirements.txt
🖥️ Usage
1. Run Web Application

streamlit run app.py
Features inside UI:
✅ Single Email Tab
* Paste email content
* Get:
   * Spam / Ham prediction
   * Confidence score
✅ Batch Processing Tab
* Upload .mbox file
* Download results as CSV
2. Train the Model (Optional)
Step 1: Add Dataset

data/dataset/dataset.csv
Step 2: Run Training Pipeline

python -m src.pipeline.training_pipeline
Step 3: Output
Generated files:
* Model → outputs/
* Vectorizer → outputs/
⚠️ Important
If paths change, update:

src/config/config.py
⚙️ Configuration
Modify settings in:

src/config/config.py
You can customize:
* Model hyperparameters (Grid Search)
* Input/Output paths
* Training parameters (Cross-validation folds, etc.)
📊 Model Performance
* Uses 5-fold cross-validation
* Evaluates:
   * Accuracy
   * Precision
   * Recall
   * F1-Score
👉 Automatically selects the best-performing model (usually SVM or Random Forest)
🤝 Contributing
1. Fork the project
2. Create a branch

git checkout -b feature/AmazingFeature
Commit changes
git commit -m "Add some AmazingFeature"
Push to GitHub
git push origin feature/AmazingFeature
Open a Pull Request 📝 License This project is licensed under the MIT License. See the LICENSE file for details. 🎯 Summary
Email → Processing → Vectorization → Model → Prediction (Spam / Ham)
can you give me one .mbox file to verify my project
