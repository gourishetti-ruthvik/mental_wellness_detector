# 🧠 Mental Wellness Detector - Enhanced Version

An AI-powered emotional wellness companion with pre-trained models, test data, and file upload support.

## 🚀 Access the App

**Open in your browser:** http://localhost:8501

## ✨ New Features

### 1. 🤖 Pre-Trained AI Model (Optional)
- Uses DistilBERT emotion classification model
- 6 emotion categories: sadness, fear, anger, joy, love, surprise
- Confidence scores for predictions
- Fallback to enhanced keyword + sentiment analysis

### 2. 🧪 Test Data Support
Enable "Use Test Data" in the sidebar to access:

#### For Text Input:
- **10 Sample Messages** covering all emotion types
- **Random Selection** button for quick testing
- **Dropdown Selection** to choose specific samples
- **Or Enter Your Own** message

#### For File Upload:
- **Sample CSV File** with 10 test messages
- **Sample TXT File** with 10 test messages
- **One-Click Loading** of test data
- **Or Upload Your Own** files

### 3. 📁 Enhanced File Support
- **CSV Files** (.csv) - Auto-detects text columns
- **Excel Files** (.xlsx, .xls) - Full support
- **Text Files** (.txt) - One message per line
- **Batch Processing** up to 50 messages
- **Progress Tracking** with real-time updates

### 4. 📊 Advanced Visualizations
- **Interactive Gauge Charts** for sentiment metrics
- **Emotion Distribution** pie charts
- **Severity Distribution** histograms
- **AI Confidence Scores** display
- **Color-coded Results** by emotion type

### 5. 📥 Download & Export
- **Download Sample Files** (CSV, TXT) from sidebar
- **Export Analysis Results** as CSV with timestamps
- **Batch Results** include AI predictions and confidence

## 🎯 How to Use

### Option 1: Text Input with Test Data
1. Check "🧪 Use Test Data" in sidebar
2. Select a sample message from dropdown OR
3. Click "🔄 Random" for random sample OR
4. Type your own message
5. Click "🔍 Analyze My Emotions"

### Option 2: File Upload with Test Data
1. Check "🧪 Use Test Data" in sidebar
2. Click "📊 Use Sample CSV" or "📄 Use Sample TXT" OR
3. Upload your own file (CSV/Excel/TXT)
4. Click "🔍 Analyze File"
5. View batch results and download

### Option 3: Use Your Own Data
1. Uncheck "Use Test Data"
2. Enter text directly OR upload your file
3. Analyze and view results

## 📝 Test Data Samples

### Text Samples (10 messages):
1. Stress about exams (Depression)
2. Very happy day (Positive)
3. Feeling worthless (Depression - Critical)
4. Managing work well (Neutral)
5. Excited about project (Positive)
6. Anxious about presentation (Stress)
7. Life feels empty (Depression)
8. Amazing day with friends (Positive)
9. Exhausted and burnt out (Stress)
10. Feeling okay (Neutral)

### Sample Files Generated:
- `sample_data.csv` - 10 messages with timestamps and user IDs
- `sample_data.xlsx` - Same data in Excel format
- `sample_data.txt` - 10 messages, one per line

## 🔧 Installation

### Basic Version (No AI Model):
```bash
pip install streamlit textblob nltk pandas openpyxl plotly
python -m textblob.download_corpora
```

### With AI Model (Recommended):
```bash
pip install streamlit textblob nltk pandas openpyxl plotly transformers torch
python -m textblob.download_corpora
```

## 🎨 Features Overview

| Feature | Description |
|---------|-------------|
| 🤖 AI Model | Pre-trained DistilBERT emotion classifier |
| 🧪 Test Data | Built-in samples for quick testing |
| 📝 Text Input | Direct message entry |
| 📁 File Upload | CSV, Excel, TXT support |
| 📊 Batch Analysis | Process up to 50 messages |
| 📈 Visualizations | Interactive charts and gauges |
| 💾 Export | Download results as CSV |
| 🚨 Alerts | Emergency warnings for critical cases |
| 🎵 Music | Personalized recommendations |
| 💭 Quotes | Inspirational messages |
| ✨ Activities | Wellness suggestions |

## 📊 Emotion Categories

1. **Depression** (Critical/High/Moderate/Low)
   - Detects sadness, hopelessness, worthlessness
   - Emergency alerts for critical cases
   - Crisis helpline information

2. **Stress** (High/Moderate/Low)
   - Identifies anxiety, pressure, overwhelm
   - Relaxation recommendations

3. **Positive** (Good)
   - Recognizes happiness, joy, gratitude
   - Encouraging messages

4. **Neutral** (Normal)
   - Balanced emotional state

## 🔬 Detection Methods

### 1. AI Model (if available):
- DistilBERT-based emotion classification
- 6 emotion categories with confidence scores
- Trained on emotional text datasets

### 2. Keyword Analysis:
- 40+ emotion-specific keywords
- Weighted scoring system
- Context-aware detection

### 3. Sentiment Analysis:
- TextBlob polarity (-1 to +1)
- Subjectivity (0 to 1)
- Combined scoring

## 📱 User Interface

### Main Screen:
- Input method selector (Text/File)
- Test data toggle
- Analysis button
- Results display

### Sidebar:
- Model status indicator
- Input method selection
- Test data checkbox
- Download sample files
- About information
- Safety disclaimer

### Results Display:
- AI prediction with confidence
- Emotion type and severity
- Interactive gauge charts
- Sentiment/Subjectivity scores
- Personalized recommendations
- Emergency alerts (if needed)

## 🎓 Sample Test Scenarios

### Scenario 1: Test Stress Detection
1. Enable "Use Test Data"
2. Select: "I feel so stressed about work deadlines"
3. Analyze → Should detect: Stress (Moderate)

### Scenario 2: Test Depression Alert
1. Enable "Use Test Data"
2. Select: "I feel worthless and alone..."
3. Analyze → Should trigger: Critical Alert

### Scenario 3: Test Positive Emotions
1. Enable "Use Test Data"
2. Select: "I'm so happy today..."
3. Analyze → Should detect: Positive (Good)

### Scenario 4: Batch Analysis
1. Enable "Use Test Data"
2. Click "Use Sample CSV"
3. Analyze → View 10 results with charts

## ⚠️ Important Notes

- This tool is for wellness support ONLY
- NOT a replacement for professional help
- Emergency services available 24/7
- AI model is optional (works without it)
- Test data helps verify functionality

## 🆘 Crisis Resources

- **National Suicide Prevention Lifeline:** 988
- **Crisis Text Line:** Text HOME to 741741
- **SAMHSA Helpline:** 1-800-662-4357

## 🚀 Quick Start

```bash
# 1. Navigate to project directory
cd "Mental-wellness detector"

# 2. Run the app
streamlit run streamlit_app.py

# 3. Open browser
# http://localhost:8501
```

## 💡 Tips

1. Use test data first to understand the app
2. Try different sample messages
3. Test batch processing with sample files
4. Download and modify sample files
5. Install transformers for AI model (optional)

---

**Made with ❤️ for mental wellness support**
