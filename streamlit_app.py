import streamlit as st
from textblob import TextBlob
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Mental Wellness Detector",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Test Data Samples
TEST_DATA = {
    'text_samples': [
        "I feel extremely stressed about my upcoming exams and deadlines. The pressure is overwhelming.",
        "I'm so happy today! Everything is going great and I feel blessed.",
        "I feel worthless and alone. Nothing seems to matter anymore.",
        "Work is getting intense but I'm managing it well with breaks.",
        "I'm excited about my new project! Can't wait to see the results.",
        "Feeling anxious about the presentation tomorrow. Hope it goes well.",
        "Life feels empty and meaningless. I don't see the point anymore.",
        "Had an amazing day with friends! Feeling grateful and loved.",
        "The constant pressure is making me exhausted and burnt out.",
        "Just feeling okay today, nothing special happening."
    ],
    'csv_content': """text,timestamp,user_id
I feel so stressed about work deadlines,2025-10-27 09:00,user001
I'm having an amazing day full of joy!,2025-10-27 09:15,user002
Feeling lonely and depressed today,2025-10-27 09:30,user003
Everything is overwhelming me right now,2025-10-27 09:45,user004
Life is wonderful and I'm so grateful,2025-10-27 10:00,user005
Can't handle the pressure anymore,2025-10-27 10:15,user006
Feeling anxious about everything lately,2025-10-27 10:30,user007
Had a great workout! Feeling energized,2025-10-27 10:45,user008
I feel hopeless and worthless today,2025-10-27 11:00,user009
Pretty good day overall,2025-10-27 11:15,user010""",
    'txt_content': """I feel extremely stressed about my job
I'm so happy and excited about life
Feeling depressed and alone today
Work pressure is getting too much
Having an amazing day with family
I can't cope with this anxiety anymore
Feeling worthless and hopeless
Life is beautiful and full of joy
Overwhelmed with everything going on
Just a normal day nothing special"""
}

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .result-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 15px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
    }
    .alert-critical {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        animation: pulse 2s infinite;
    }
    .alert-warning {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
    }
    .positive-card {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.7); }
        50% { box-shadow: 0 0 0 20px rgba(255, 107, 107, 0); }
    }
    .recommendation-box {
        background: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    h1, h2, h3 {
        color: white !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Keywords and recommendations (same as before)
STRESS_KEYWORDS = ['stress', 'pressure', 'overwhelm', 'anxious', 'anxiety', 'worried', 'tense', 'panic', 'burden', 'exhausted']
DEPRESSION_KEYWORDS = ['depressed', 'sad', 'lonely', 'hopeless', 'worthless', 'empty', 'tired', 'suicide', 'die', 'harm', 'hate myself', 'give up', 'no point']
POSITIVE_KEYWORDS = ['happy', 'joy', 'excited', 'grateful', 'blessed', 'love', 'great', 'wonderful', 'amazing', 'fantastic', 'good']

MUSIC_RECOMMENDATIONS = {
    'stress': [
        '🎵 Weightless - Marconi Union',
        '🎵 Piano Concerto No. 23 - Mozart',
        '🎵 Clair de Lune - Debussy',
        '🎵 Ambient Music for Stress Relief',
        '🎵 Nature Sounds - Ocean Waves'
    ],
    'depression': [
        '🎵 Here Comes The Sun - The Beatles',
        '🎵 Three Little Birds - Bob Marley',
        '🎵 Beautiful Day - U2',
        '🎵 Don\'t Stop Me Now - Queen',
        '🎵 Uplifting Classical Music'
    ],
    'positive': [
        '🎵 Happy - Pharrell Williams',
        '🎵 Good Vibrations - The Beach Boys',
        '🎵 Walking on Sunshine - Katrina',
        '🎵 I Got You (I Feel Good) - James Brown',
        '🎵 Best Day of My Life - American Authors'
    ]
}

QUOTES = {
    'stress': [
        "You don't have to control your thoughts. You just have to stop letting them control you.",
        "Take a deep breath. It's just a bad day, not a bad life.",
        "You are braver than you believe, stronger than you seem, and smarter than you think."
    ],
    'depression': [
        "This too shall pass. You are stronger than you think.",
        "Every day may not be good, but there is something good in every day.",
        "You are not alone. Reach out, someone cares.",
        "The darkest nights produce the brightest stars.",
        "Your life is valuable. You matter."
    ],
    'positive': [
        "Keep shining! Your positive energy is contagious.",
        "Happiness looks gorgeous on you!",
        "Your positive attitude is your superpower!"
    ]
}

ACTIVITIES = {
    'depression': [
        '🚶 Take a 10-minute walk outside',
        '📞 Call a friend or family member',
        '🧘 Practice deep breathing exercises',
        '📝 Write down 3 things you\'re grateful for',
        '💬 Consider speaking with a mental health professional'
    ],
    'stress': [
        '🧘 Try a 5-minute meditation',
        '🤸 Do some light stretching',
        '🎵 Listen to calming music',
        '☕ Take a short break',
        '💆 Practice progressive muscle relaxation'
    ],
    'positive': [
        '😊 Share your happiness with someone',
        '📔 Journal your feelings',
        '🎨 Do something creative',
        '🤝 Help someone else today',
        '🎉 Celebrate your wins!'
    ]
}

def analyze_sentiment(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return polarity, subjectivity

def detect_emotion(text):
    """Detect emotions based on keywords and sentiment"""
    text_lower = text.lower()
    
    # Keyword-based detection
    critical_score = sum(1 for keyword in DEPRESSION_KEYWORDS if keyword in text_lower)
    stress_score = sum(1 for keyword in STRESS_KEYWORDS if keyword in text_lower)
    positive_score = sum(1 for keyword in POSITIVE_KEYWORDS if keyword in text_lower)
    
    polarity, subjectivity = analyze_sentiment(text)
    
    # Decision logic
    if critical_score >= 2 or (critical_score >= 1 and polarity < -0.3):
        emotion, severity = 'depression', 'critical'
    elif critical_score >= 1 or (stress_score >= 2 and polarity < -0.1):
        emotion, severity = 'depression', 'high'
    elif stress_score >= 2 or (polarity < -0.2 and subjectivity > 0.5):
        emotion, severity = 'stress', 'moderate'
    elif stress_score >= 1 or (polarity < 0 and polarity > -0.3):
        emotion, severity = 'stress', 'low'
    elif positive_score >= 2 or polarity > 0.3:
        emotion, severity = 'positive', 'good'
    elif polarity >= 0:
        emotion, severity = 'neutral', 'normal'
    else:
        emotion, severity = 'stress', 'low'
    
    return emotion, severity, polarity, subjectivity

def display_results(text, emotion, severity, polarity, subjectivity):
    """Display analysis results with beautiful UI"""
    
    # Emotion icons
    emotion_icons = {
        'depression': '😢',
        'stress': '😰',
        'positive': '😊',
        'neutral': '😐'
    }
    
    # Display emotion card based on type
    if emotion == 'depression' and severity in ['critical', 'high']:
        st.markdown(f"""
        <div class="alert-critical">
            <h2>{emotion_icons[emotion]} ALERT: {emotion.upper()} - {severity.upper()}</h2>
            <p style="font-size: 18px;">We detected signs of severe distress. Please reach out immediately!</p>
            <hr style="border: 1px solid white; margin: 15px 0;">
            <h3>🚨 Emergency Contacts:</h3>
            <ul style="font-size: 16px;">
                <li>National Suicide Prevention Lifeline: <strong>988</strong></li>
                <li>Crisis Text Line: Text <strong>HOME</strong> to <strong>741741</strong></li>
                <li>SAMHSA Helpline: <strong>1-800-662-4357</strong></li>
                <li>International Association for Suicide Prevention: <strong>iasp.info</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif emotion == 'stress':
        st.markdown(f"""
        <div class="alert-warning">
            <h2>{emotion_icons[emotion]} {emotion.upper()} Detected - {severity.upper()} Level</h2>
            <p style="font-size: 16px;">We noticed some stress. Take a moment to breathe and relax.</p>
        </div>
        """, unsafe_allow_html=True)
    elif emotion == 'positive':
        st.markdown(f"""
        <div class="positive-card">
            <h2>{emotion_icons[emotion]} {emotion.upper()} Vibes! - {severity.upper()}</h2>
            <p style="font-size: 16px;">Great! You're feeling positive. Keep up the good vibes!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{emotion_icons.get(emotion, '🤔')} {emotion.upper()} - {severity.upper()}</h2>
            <p style="font-size: 16px;">Your emotional state seems stable.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Metrics in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Sentiment Score")
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=polarity,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Polarity"},
            delta={'reference': 0},
            gauge={
                'axis': {'range': [-1, 1]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-1, -0.3], 'color': "#ffcdd2"},
                    {'range': [-0.3, 0.3], 'color': "#fff9c4"},
                    {'range': [0.3, 1], 'color': "#c8e6c9"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': polarity
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Subjectivity Score")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=subjectivity,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Subjectivity"},
            gauge={
                'axis': {'range': [0, 1]},
                'bar': {'color': "purple"},
                'steps': [
                    {'range': [0, 0.5], 'color': "#e1bee7"},
                    {'range': [0.5, 1], 'color': "#ce93d8"}
                ]
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.markdown("---")
    st.markdown("## 💡 Personalized Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎵 Music")
        music_list = MUSIC_RECOMMENDATIONS.get(emotion, MUSIC_RECOMMENDATIONS['stress'])
        for song in music_list:
            st.markdown(f"- {song}")
    
    with col2:
        st.markdown("### 💭 Quote")
        import random
        quote = random.choice(QUOTES.get(emotion, QUOTES['stress']))
        st.info(f'"{quote}"')
        
    with col3:
        st.markdown("### ✨ Activities")
        activities = ACTIVITIES.get(emotion, ACTIVITIES['stress'])
        for activity in activities:
            st.markdown(f"- {activity}")

def process_file(uploaded_file):
    """Process uploaded files and extract text"""
    texts = []
    
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            # Try to find text column
            text_cols = [col for col in df.columns if 'text' in col.lower() or 'message' in col.lower() or 'content' in col.lower()]
            if text_cols:
                texts = df[text_cols[0]].dropna().tolist()
            else:
                # Use first column
                texts = df.iloc[:, 0].dropna().tolist()
        
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
            text_cols = [col for col in df.columns if 'text' in col.lower() or 'message' in col.lower() or 'content' in col.lower()]
            if text_cols:
                texts = df[text_cols[0]].dropna().tolist()
            else:
                texts = df.iloc[:, 0].dropna().tolist()
        
        elif uploaded_file.name.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
            texts = [line.strip() for line in content.split('\n') if line.strip()]
        
        else:
            st.error("Unsupported file format. Please upload CSV, Excel, or TXT files.")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
    
    return texts

# Main app
def main():
    # Header
    st.markdown("<h1 style='text-align: center; font-size: 3em;'>🧠 Mental Wellness Detector</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.3em; color: white;'>Your AI-powered emotional wellness companion</p>", unsafe_allow_html=True)
    st.markdown("---")
    with st.sidebar:
        st.markdown("## ⚙️ Settings")
        
        # Model status - simplified
        st.success("✅ Ready")
        
        st.markdown("---")
        
        input_mode = st.radio(
            "Choose Input Method:",
            ["📝 Text Input", "📁 File Upload"],
            index=0
        )
        
        # Test data option
        use_test_data = st.checkbox("🧪 Use Test Data", value=False, 
                                     help="Load sample data for testing")
        
        st.markdown("---")
        st.markdown("## 📊 About")
        st.info("""
        **Features:**
        - Emotion Detection
        - Sentiment Analysis  
        - Batch Processing
        - Test Data Support
        """)
        
        # Download sample files
        st.markdown("---")
        st.markdown("## 📥 Sample Files")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📄 CSV",
                data=TEST_DATA['csv_content'],
                file_name="sample_data.csv",
                mime="text/csv"
            )
        with col2:
            st.download_button(
                label="📄 TXT",
                data=TEST_DATA['txt_content'],
                file_name="sample_data.txt",
                mime="text/plain"
            )
        
        st.markdown("---")
        st.warning("⚠️ For support only. Contact professionals for serious concerns.")
    
    # Main content
    if input_mode == "📝 Text Input":
        st.markdown("## 💬 Share Your Thoughts")
        
        # Test data selector for text input
        if use_test_data:
            st.info("🧪 **Test Mode Active** - Select from sample messages or enter your own")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_sample = st.selectbox(
                    "Choose a test message:",
                    [""] + TEST_DATA['text_samples'],
                    format_func=lambda x: x[:80] + "..." if len(x) > 80 else x if x else "-- Select a sample --"
                )
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Random", use_container_width=True):
                    import random
                    selected_sample = random.choice(TEST_DATA['text_samples'])
                    st.rerun()
            
            user_text = st.text_area(
                "Or enter your own message:",
                value=selected_sample,
                placeholder="Type your message here... e.g., 'I feel stressed about work' or 'I'm having a great day!'",
                height=150
            )
        else:
            user_text = st.text_area(
                "How are you feeling today?",
                placeholder="Type your message here... e.g., 'I feel stressed about work' or 'I'm having a great day!'",
                height=150
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button("🔍 Analyze My Emotions", use_container_width=True)
        
        if analyze_button and user_text:
            if len(user_text.strip()) < 5:
                st.error("Please enter a longer message (at least 5 characters)")
            else:
                with st.spinner("🤖 Analyzing your emotions..."):
                    emotion, severity, polarity, subjectivity = detect_emotion(user_text)
                    
                    st.markdown("---")
                    st.markdown("## 📋 Analysis Results")
                    st.markdown(f"**Analyzed Text:** _{user_text}_")
                    st.markdown(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    display_results(user_text, emotion, severity, polarity, subjectivity)
        elif analyze_button:
            st.error("Please enter some text to analyze!")
    
    else:  # File Upload Mode
        st.markdown("## 📁 Upload Your File")
        
        # Test data option for file upload
        if use_test_data:
            st.info("🧪 **Test Mode Active** - Use sample files or upload your own")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📊 Use Sample CSV", use_container_width=True):
                    st.session_state['test_file'] = 'csv'
                    st.session_state['test_data'] = TEST_DATA['csv_content']
            with col2:
                if st.button("📄 Use Sample TXT", use_container_width=True):
                    st.session_state['test_file'] = 'txt'
                    st.session_state['test_data'] = TEST_DATA['txt_content']
            with col3:
                if st.button("🗑️ Clear Test Data", use_container_width=True):
                    st.session_state['test_file'] = None
                    st.session_state['test_data'] = None
            
            st.markdown("---")
        
        # Check if test data is loaded
        if use_test_data and 'test_file' in st.session_state and st.session_state.get('test_file'):
            file_type = st.session_state['test_file']
            test_data = st.session_state['test_data']
            
            st.success(f"✅ Sample {file_type.upper()} file loaded")
            
            with st.expander("📄 View Test Data"):
                st.text(test_data[:500] + "..." if len(test_data) > 500 else test_data)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                process_button = st.button("🔍 Analyze Test Data", use_container_width=True)
            
            if process_button:
                # Process test data
                if file_type == 'csv':
                    df = pd.read_csv(io.StringIO(test_data))
                    text_cols = [col for col in df.columns if 'text' in col.lower() or 'message' in col.lower()]
                    texts = df[text_cols[0]].dropna().tolist() if text_cols else df.iloc[:, 0].dropna().tolist()
                else:  # txt
                    texts = [line.strip() for line in test_data.split('\n') if line.strip()]
                
                if texts:
                    st.markdown(f"### 📊 Found {len(texts)} messages to analyze")
                    process_texts(texts)
                else:
                    st.error("No valid messages found in test data.")
        else:
            # Normal file upload
            uploaded_file = st.file_uploader(
                "Upload a CSV, Excel, or TXT file containing messages",
                type=['csv', 'xlsx', 'xls', 'txt']
            )
            
            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    process_button = st.button("🔍 Analyze File", use_container_width=True)
                
                if process_button:
                    texts = process_file(uploaded_file)
                    
                    if texts:
                        st.markdown(f"### 📊 Found {len(texts)} messages to analyze")
                        process_texts(texts)
                    else:
                        st.error("Could not extract messages from the file.")

def process_texts(texts):
    """Process and analyze a list of texts"""
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, text in enumerate(texts[:50]):  # Limit to 50 for performance
        if len(str(text).strip()) > 5:
            emotion, severity, polarity, subjectivity = detect_emotion(str(text))
            results.append({
                'Message': text[:100] + '...' if len(str(text)) > 100 else text,
                'Emotion': emotion,
                'Severity': severity,
                'Polarity': round(polarity, 2),
                'Subjectivity': round(subjectivity, 2)
            })
        
        progress_bar.progress((idx + 1) / min(len(texts), 50))
        status_text.text(f"Analyzing message {idx + 1} of {min(len(texts), 50)}...")
    
    status_text.empty()
    progress_bar.empty()
    
    if results:
        st.markdown("---")
        st.markdown("## 📊 Batch Analysis Results")
        
        df_results = pd.DataFrame(results)
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>😢 Depression</h3>
                <h2>{len(df_results[df_results['Emotion'] == 'depression'])}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>😰 Stress</h3>
                <h2>{len(df_results[df_results['Emotion'] == 'stress'])}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>😊 Positive</h3>
                <h2>{len(df_results[df_results['Emotion'] == 'positive'])}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>😐 Neutral</h3>
                <h2>{len(df_results[df_results['Emotion'] == 'neutral'])}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Emotion Distribution")
            fig = px.pie(df_results, names='Emotion', title='Emotion Distribution', 
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Severity Distribution")
            fig = px.histogram(df_results, x='Severity', title='Severity Levels',
                             color='Emotion', barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed results
        st.markdown("### 📋 Detailed Results")
        st.dataframe(df_results, use_container_width=True)
        
        # Download results
        csv = df_results.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"mental_wellness_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("No valid messages found to analyze.")

if __name__ == "__main__":
    main()
