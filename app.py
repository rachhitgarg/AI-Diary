import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from PIL import Image
import io
import base64
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Page configuration
st.set_page_config(
    page_title="AI Student Diary",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .diary-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .mood-selector {
        display: flex;
        gap: 0.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .mood-btn {
        background: none;
        border: 2px solid #e0e0e0;
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .mood-btn:hover {
        transform: scale(1.1);
        border-color: #667eea;
    }
    
    .mood-btn.selected {
        border-color: #667eea;
        background-color: #667eea;
        color: white;
    }
    
    .insight-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .calendar-event {
        background: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

class StudentDiaryApp:
    def __init__(self):
        self.initialize_session_state()
        self.load_data()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'diary_entries' not in st.session_state:
            st.session_state.diary_entries = []
        if 'current_mood' not in st.session_state:
            st.session_state.current_mood = None
        if 'current_entry' not in st.session_state:
            st.session_state.current_entry = ""
        if 'calendar_events' not in st.session_state:
            st.session_state.calendar_events = []
        if 'mood_history' not in st.session_state:
            st.session_state.mood_history = []
        if 'ai_insights' not in st.session_state:
            st.session_state.ai_insights = []
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'name': 'Priya',
                'grade': 10,
                'school': 'Delhi Public School',
                'age': 15
            }
    
    def load_data(self):
        """Load data from local storage or create sample data"""
        # Load from local files if they exist
        if os.path.exists('diary_data.json'):
            try:
                with open('diary_data.json', 'r') as f:
                    data = json.load(f)
                    st.session_state.diary_entries = data.get('entries', [])
                    st.session_state.calendar_events = data.get('events', [])
                    st.session_state.mood_history = data.get('mood_history', [])
                    st.session_state.ai_insights = data.get('insights', [])
            except:
                self.create_sample_data()
        else:
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for demonstration"""
        # Sample diary entries
        sample_entries = [
            {
                'id': 1,
                'date': '2025-01-15',
                'content': 'Today was amazing! Finally understood quadratic equations in math class. Mr. Sharma explained it so well. Feeling really confident about the upcoming test.',
                'mood': 8,
                'topics': ['academic', 'math', 'confidence'],
                'word_count': 35
            },
            {
                'id': 2,
                'date': '2025-01-14',
                'content': 'Had a tough day. Physics test didn\'t go well, and I felt really stressed about it. Mom tried to cheer me up with my favorite food.',
                'mood': 4,
                'topics': ['academic', 'physics', 'stress', 'family'],
                'word_count': 42
            },
            {
                'id': 3,
                'date': '2025-01-13',
                'content': 'Great time with friends at lunch! We planned a study group for the weekend. Priya and I are going to work on chemistry together.',
                'mood': 7,
                'topics': ['social', 'friends', 'academic', 'chemistry'],
                'word_count': 38
            }
        ]
        
        # Sample calendar events
        sample_events = [
            {
                'id': 1,
                'title': 'Math Test',
                'date': '2025-01-20',
                'description': 'Quadratic equations and functions',
                'type': 'academic',
                'priority': 'high'
            },
            {
                'id': 2,
                'title': 'Priya\'s Birthday',
                'date': '2025-01-25',
                'description': 'Birthday celebration at Priya\'s house',
                'type': 'social',
                'priority': 'medium'
            },
            {
                'id': 3,
                'title': 'Science Project Due',
                'date': '2025-01-30',
                'description': 'Physics project on electromagnetic induction',
                'type': 'academic',
                'priority': 'high'
            }
        ]
        
        # Sample mood history
        sample_mood_history = [
            {'date': '2025-01-10', 'mood': 6, 'note': 'Regular day'},
            {'date': '2025-01-11', 'mood': 7, 'note': 'Good study session'},
            {'date': '2025-01-12', 'mood': 5, 'note': 'A bit tired'},
            {'date': '2025-01-13', 'mood': 7, 'note': 'Fun with friends'},
            {'date': '2025-01-14', 'mood': 4, 'note': 'Tough physics test'},
            {'date': '2025-01-15', 'mood': 8, 'note': 'Math breakthrough!'}
        ]
        
        st.session_state.diary_entries = sample_entries
        st.session_state.calendar_events = sample_events
        st.session_state.mood_history = sample_mood_history
    
    def save_data(self):
        """Save data to local storage"""
        data = {
            'entries': st.session_state.diary_entries,
            'events': st.session_state.calendar_events,
            'mood_history': st.session_state.mood_history,
            'insights': st.session_state.ai_insights
        }
        
        try:
            with open('diary_data.json', 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            st.error(f"Error saving data: {e}")
    
    def analyze_entry(self, entry_text, mood):
        """Perform basic AI analysis on diary entry"""
        analysis = {
            'sentiment': 'neutral',
            'topics': [],
            'stress_level': 'low',
            'insights': []
        }
        
        text_lower = entry_text.lower()
        
        # Sentiment analysis
        positive_words = ['happy', 'excited', 'great', 'amazing', 'wonderful', 'proud', 'success', 'love', 'enjoy', 'fun', 'good', 'nice']
        negative_words = ['sad', 'angry', 'frustrated', 'worried', 'scared', 'lonely', 'tired', 'stress', 'fail', 'hate', 'bad', 'terrible']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            analysis['sentiment'] = 'positive'
        elif negative_count > positive_count:
            analysis['sentiment'] = 'negative'
        
        # Topic detection
        topics = {
            'academic': ['test', 'exam', 'homework', 'study', 'class', 'teacher', 'school', 'grade', 'assignment', 'project', 'math', 'physics', 'chemistry'],
            'social': ['friend', 'group', 'party', 'invite', 'lunch', 'play', 'talk', 'share', 'help', 'support'],
            'family': ['mom', 'dad', 'parent', 'family', 'home', 'house', 'sister', 'brother'],
            'cultural': ['diwali', 'holi', 'rakhi', 'ganesh', 'festival', 'celebration', 'tradition', 'culture']
        }
        
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                analysis['topics'].append(topic)
        
        # Stress level
        if mood and mood <= 3:
            analysis['stress_level'] = 'high'
        elif negative_count > 2:
            analysis['stress_level'] = 'medium'
        
        # Generate insights
        if analysis['sentiment'] == 'negative':
            analysis['insights'].append("It's okay to have difficult days. Remember that your feelings are valid and temporary.")
        
        if 'academic' in analysis['topics']:
            analysis['insights'].append("You're showing dedication to your studies. Consider breaking large tasks into smaller steps.")
        
        if 'social' in analysis['topics']:
            analysis['insights'].append("Human connections are important. Remember that you have people who care about you.")
        
        if 'cultural' in analysis['topics']:
            analysis['insights'].append("Your cultural heritage is a beautiful part of who you are. Celebrate it with joy!")
        
        return analysis
    
    def create_morning_reflection(self, yesterday_entry):
        """Create morning reflection based on yesterday's entry"""
        if not yesterday_entry:
            return {
                'greeting': 'Good morning!',
                'message': 'A new day begins with endless possibilities.',
                'encouragement': 'Your thoughts and feelings matter.',
                'action': 'Today\'s focus: Write about what\'s on your mind.'
            }
        
        analysis = self.analyze_entry(yesterday_entry['content'], yesterday_entry.get('mood'))
        
        if analysis['sentiment'] == 'negative':
            return {
                'greeting': 'Good morning!',
                'message': 'Yesterday\'s challenges show your strength in facing difficulties.',
                'encouragement': 'Remember, every challenge you face makes you stronger.',
                'action': 'Today\'s focus: Take one step at a time.'
            }
        elif analysis['sentiment'] == 'positive':
            return {
                'greeting': 'Good morning!',
                'message': 'Yesterday\'s positive energy is still with you today!',
                'encouragement': 'Keep that momentum going - you\'re doing great!',
                'action': 'Today\'s focus: Build on yesterday\'s success.'
            }
        else:
            return {
                'greeting': 'Good morning!',
                'message': 'A new day brings new opportunities.',
                'encouragement': 'You have the power to make today amazing.',
                'action': 'Today\'s focus: What would make you proud?'
            }
    
    def detect_calendar_events(self, entry_text):
        """Detect calendar events from diary entry"""
        events = []
        text_lower = entry_text.lower()
        
        # Date patterns
        date_patterns = [
            r'tomorrow',
            r'next week',
            r'next month',
            r'in \d+ days?',
            r'january \d+',
            r'february \d+',
            r'march \d+',
            r'april \d+',
            r'may \d+',
            r'june \d+',
            r'july \d+',
            r'august \d+',
            r'september \d+',
            r'october \d+',
            r'november \d+',
            r'december \d+'
        ]
        
        # Event patterns
        event_keywords = ['test', 'exam', 'quiz', 'assignment', 'project', 'birthday', 'party', 'celebration', 'festival', 'meeting', 'appointment']
        
        # Simple event detection
        for keyword in event_keywords:
            if keyword in text_lower:
                # Find associated date
                for pattern in date_patterns:
                    if pattern in text_lower:
                        event = {
                            'id': len(st.session_state.calendar_events) + 1,
                            'title': keyword.title(),
                            'date': self.parse_date_from_text(text_lower),
                            'description': f'Detected from diary entry: "{entry_text[:100]}..."',
                            'type': 'academic' if keyword in ['test', 'exam', 'quiz', 'assignment', 'project'] else 'personal',
                            'priority': 'high' if keyword in ['test', 'exam', 'quiz'] else 'medium'
                        }
                        events.append(event)
                        break
        
        return events
    
    def parse_date_from_text(self, text):
        """Parse date from text (simplified)"""
        # This is a simplified date parser
        # In a real application, you'd use more sophisticated NLP
        if 'tomorrow' in text:
            tomorrow = datetime.now() + timedelta(days=1)
            return tomorrow.strftime('%Y-%m-%d')
        elif 'next week' in text:
            next_week = datetime.now() + timedelta(days=7)
            return next_week.strftime('%Y-%m-%d')
        else:
            # Default to a week from now
            next_week = datetime.now() + timedelta(days=7)
            return next_week.strftime('%Y-%m-%d')
    
    def run(self):
        """Main application runner"""
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>📚 AI Student Diary</h1>
            <p>Your Personal Reflection Space - Powered by AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown("### 🧭 Navigation")
            selected = option_menu(
                menu_title=None,
                options=["📖 Write Entry", "📊 Insights", "📅 Calendar", "📈 Mood Tracking", "⚙️ Settings"],
                icons=["pen", "chart", "calendar", "heart", "gear"],
                menu_icon="cast",
                default_index=0,
            )
            
            st.markdown("---")
            
            # User profile
            st.markdown("### 👤 Profile")
            st.write(f"**Name:** {st.session_state.user_profile['name']}")
            st.write(f"**Grade:** {st.session_state.user_profile['grade']}")
            st.write(f"**School:** {st.session_state.user_profile['school']}")
            
            # Quick stats
            st.markdown("### 📊 Quick Stats")
            st.write(f"**Total Entries:** {len(st.session_state.diary_entries)}")
            st.write(f"**Current Streak:** {self.calculate_streak()} days")
            st.write(f"**Average Mood:** {self.calculate_average_mood():.1f}/10")
        
        # Main content based on selection
        if selected == "📖 Write Entry":
            self.write_entry_page()
        elif selected == "📊 Insights":
            self.insights_page()
        elif selected == "📅 Calendar":
            self.calendar_page()
        elif selected == "📈 Mood Tracking":
            self.mood_tracking_page()
        elif selected == "⚙️ Settings":
            self.settings_page()
    
    def write_entry_page(self):
        """Diary entry writing page"""
        st.markdown("## ✍️ Write Your Diary Entry")
        
        # Date display
        today = datetime.now().strftime("%A, %B %d, %Y")
        st.markdown(f"**Today:** {today}")
        
        # Mood selector
        st.markdown("### 😊 How are you feeling today?")
        mood_labels = ["😢", "😔", "😐", "🙂", "😊", "😄", "🤩", "🥳", "😍", "🤯"]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        
        for i, (mood, label) in enumerate(zip(range(1, 11), mood_labels)):
            col_idx = i % 5
            with cols[col_idx]:
                if st.button(f"{label}\n{i+1}", key=f"mood_{i+1}", use_container_width=True):
                    st.session_state.current_mood = i + 1
                    st.success(f"Mood selected: {i+1}/10")
        
        # Current mood display
        if st.session_state.current_mood:
            st.info(f"**Current Mood:** {st.session_state.current_mood}/10")
        
        # Diary entry text area
        st.markdown("### 📝 What's on your mind today?")
        entry_text = st.text_area(
            "Write freely about your day, thoughts, feelings, or anything else...",
            value=st.session_state.current_entry,
            height=200,
            placeholder="Today I felt... I learned... I'm grateful for..."
        )
        
        # Update current entry
        st.session_state.current_entry = entry_text
        
        # Entry actions
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("💾 Save Entry", use_container_width=True):
                self.save_entry(entry_text)
        
        with col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.current_entry = ""
                st.session_state.current_mood = None
                st.rerun()
        
        # Recent entries
        if st.session_state.diary_entries:
            st.markdown("### 📚 Recent Entries")
            for entry in st.session_state.diary_entries[-3:]:
                with st.expander(f"{entry['date']} - Mood: {entry['mood']}/10"):
                    st.write(entry['content'])
                    st.caption(f"Topics: {', '.join(entry.get('topics', []))}")
    
    def save_entry(self, entry_text):
        """Save diary entry"""
        if not entry_text.strip() and not st.session_state.current_mood:
            st.error("Please write something or select a mood before saving.")
            return
        
        # Create new entry
        new_entry = {
            'id': len(st.session_state.diary_entries) + 1,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'content': entry_text.strip(),
            'mood': st.session_state.current_mood,
            'topics': [],
            'word_count': len(entry_text.split()),
            'timestamp': datetime.now().isoformat()
        }
        
        # Analyze entry
        analysis = self.analyze_entry(entry_text, st.session_state.current_mood)
        new_entry['topics'] = analysis['topics']
        
        # Add to entries
        st.session_state.diary_entries.append(new_entry)
        
        # Update mood history
        if st.session_state.current_mood:
            mood_entry = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'mood': st.session_state.current_mood,
                'note': entry_text[:50] + "..." if len(entry_text) > 50 else entry_text
            }
            st.session_state.mood_history.append(mood_entry)
        
        # Detect calendar events
        events = self.detect_calendar_events(entry_text)
        for event in events:
            if not any(existing['title'] == event['title'] and existing['date'] == event['date'] 
                      for existing in st.session_state.calendar_events):
                st.session_state.calendar_events.append(event)
        
        # Save data
        self.save_data()
        
        # Clear current entry
        st.session_state.current_entry = ""
        st.session_state.current_mood = None
        
        st.success("Entry saved successfully! Your AI reflection will be ready tomorrow morning.")
        st.rerun()
    
    def insights_page(self):
        """AI insights and analysis page"""
        st.markdown("## 🧠 AI Insights & Analysis")
        
        if not st.session_state.diary_entries:
            st.info("Write your first diary entry to see AI insights!")
            return
        
        # Latest entry analysis
        latest_entry = st.session_state.diary_entries[-1]
        analysis = self.analyze_entry(latest_entry['content'], latest_entry.get('mood'))
        
        # Display analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Entry Analysis")
            st.metric("Sentiment", analysis['sentiment'].title())
            st.metric("Stress Level", analysis['stress_level'].title())
            st.metric("Topics", len(analysis['topics']))
            st.metric("Word Count", latest_entry['word_count'])
        
        with col2:
            st.markdown("### 🏷️ Detected Topics")
            if analysis['topics']:
                for topic in analysis['topics']:
                    st.success(f"• {topic.title()}")
            else:
                st.info("No specific topics detected")
        
        # AI insights
        st.markdown("### 💡 AI Insights")
        if analysis['insights']:
            for insight in analysis['insights']:
                st.markdown(f"""
                <div class="insight-card">
                    <p>{insight}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Write more detailed entries to get personalized insights!")
        
        # Morning reflection
        if st.session_state.diary_entries:
            st.markdown("### 🌅 Morning Reflection")
            reflection = self.create_morning_reflection(latest_entry)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; padding: 1.5rem; border-radius: 10px;">
                <h4>{reflection['greeting']}</h4>
                <p><strong>{reflection['message']}</strong></p>
                <p>{reflection['encouragement']}</p>
                <p><em>{reflection['action']}</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    def calendar_page(self):
        """Calendar and events page"""
        st.markdown("## 📅 Calendar & Events")
        
        # Add new event
        with st.expander("➕ Add New Event"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                event_title = st.text_input("Event Title")
            with col2:
                event_date = st.date_input("Event Date")
            with col3:
                event_type = st.selectbox("Event Type", ["academic", "personal", "social", "cultural"])
            
            if st.button("Add Event"):
                if event_title and event_date:
                    new_event = {
                        'id': len(st.session_state.calendar_events) + 1,
                        'title': event_title,
                        'date': event_date.strftime('%Y-%m-%d'),
                        'description': f'Manually added event',
                        'type': event_type,
                        'priority': 'medium'
                    }
                    st.session_state.calendar_events.append(new_event)
                    self.save_data()
                    st.success("Event added successfully!")
                    st.rerun()
        
        # Display events
        if st.session_state.calendar_events:
            st.markdown("### 📋 Upcoming Events")
            
            # Sort events by date
            sorted_events = sorted(st.session_state.calendar_events, key=lambda x: x['date'])
            
            # Filter upcoming events (next 30 days)
            today = datetime.now().date()
            upcoming_events = []
            
            for event in sorted_events:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
                if event_date >= today:
                    days_until = (event_date - today).days
                    event['days_until'] = days_until
                    upcoming_events.append(event)
            
            # Display events
            for event in upcoming_events[:10]:  # Show next 10 events
                days_text = "Today" if event['days_until'] == 0 else f"In {event['days_until']} days"
                
                st.markdown(f"""
                <div class="calendar-event">
                    <h4>{event['title']}</h4>
                    <p><strong>Date:</strong> {event['date']} ({days_text})</p>
                    <p><strong>Type:</strong> {event['type'].title()}</p>
                    <p><strong>Priority:</strong> {event['priority'].title()}</p>
                    <p>{event['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No events scheduled. Add some events to get started!")
    
    def mood_tracking_page(self):
        """Mood tracking and visualization page"""
        st.markdown("## 📈 Mood Tracking & Trends")
        
        if not st.session_state.mood_history:
            st.info("Start writing diary entries to track your mood!")
            return
        
        # Mood chart
        st.markdown("### 📊 Mood Over Time")
        
        # Prepare data for plotting
        mood_df = pd.DataFrame(st.session_state.mood_history)
        mood_df['date'] = pd.to_datetime(mood_df['date'])
        mood_df = mood_df.sort_values('date')
        
        # Create mood chart
        fig = px.line(
            mood_df, 
            x='date', 
            y='mood',
            title='Your Mood Journey',
            labels={'mood': 'Mood Rating (1-10)', 'date': 'Date'},
            markers=True
        )
        
        fig.update_layout(
            yaxis=dict(range=[0, 10]),
            yaxis_tickvals=list(range(1, 11)),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Mood statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_mood = mood_df['mood'].mean()
            st.metric("Average Mood", f"{avg_mood:.1f}/10")
        
        with col2:
            best_mood = mood_df['mood'].max()
            st.metric("Best Mood", f"{best_mood}/10")
        
        with col3:
            worst_mood = mood_df['mood'].min()
            st.metric("Lowest Mood", f"{worst_mood}/10")
        
        with col4:
            mood_count = len(mood_df)
            st.metric("Days Tracked", mood_count)
        
        # Recent mood entries
        st.markdown("### 📝 Recent Mood Entries")
        recent_moods = mood_df.tail(7)  # Last 7 entries
        
        for _, mood_entry in recent_moods.iterrows():
            mood_emoji = "😢" if mood_entry['mood'] <= 3 else "😔" if mood_entry['mood'] <= 5 else "😐" if mood_entry['mood'] <= 7 else "😊"
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                <p><strong>{mood_entry['date'].strftime('%B %d, %Y')}</strong> {mood_emoji} <strong>Mood: {mood_entry['mood']}/10</strong></p>
                <p><em>{mood_entry['note']}</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    def settings_page(self):
        """Settings and configuration page"""
        st.markdown("## ⚙️ Settings & Configuration")
        
        # User profile settings
        st.markdown("### 👤 User Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Name", value=st.session_state.user_profile['name'])
            new_grade = st.number_input("Grade", min_value=1, max_value=12, value=st.session_state.user_profile['grade'])
        
        with col2:
            new_school = st.text_input("School", value=st.session_state.user_profile['school'])
            new_age = st.number_input("Age", min_value=10, max_value=20, value=st.session_state.user_profile['age'])
        
        if st.button("💾 Save Profile"):
            st.session_state.user_profile.update({
                'name': new_name,
                'grade': new_grade,
                'school': new_school,
                'age': new_age
            })
            st.success("Profile updated successfully!")
        
        # Data management
        st.markdown("### 💾 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Data"):
                self.export_data()
        
        with col2:
            if st.button("🗑️ Clear All Data"):
                if st.checkbox("I understand this will delete all my data permanently"):
                    self.clear_all_data()
        
        # Export data as JSON
        if st.button("📄 Download Data Backup"):
            self.download_data_backup()
    
    def calculate_streak(self):
        """Calculate current writing streak"""
        if not st.session_state.diary_entries:
            return 0
        
        # Sort entries by date
        sorted_entries = sorted(st.session_state.diary_entries, key=lambda x: x['date'])
        
        streak = 0
        current_date = datetime.now().date()
        
        for entry in reversed(sorted_entries):
            entry_date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
            days_diff = (current_date - entry_date).days
            
            if days_diff == streak:
                streak += 1
            else:
                break
        
        return streak
    
    def calculate_average_mood(self):
        """Calculate average mood from recent entries"""
        if not st.session_state.mood_history:
            return 0
        
        recent_moods = [entry['mood'] for entry in st.session_state.mood_history[-7:]]  # Last 7 days
        return sum(recent_moods) / len(recent_moods) if recent_moods else 0
    
    def export_data(self):
        """Export data to JSON file"""
        data = {
            'user_profile': st.session_state.user_profile,
            'diary_entries': st.session_state.diary_entries,
            'calendar_events': st.session_state.calendar_events,
            'mood_history': st.session_state.mood_history,
            'export_date': datetime.now().isoformat()
        }
        
        # Convert to JSON string
        json_str = json.dumps(data, indent=2, default=str)
        
        # Create download button
        st.download_button(
            label="📥 Download Data",
            data=json_str,
            file_name=f"diary_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    def clear_all_data(self):
        """Clear all application data"""
        st.session_state.diary_entries = []
        st.session_state.calendar_events = []
        st.session_state.mood_history = []
        st.session_state.ai_insights = []
        st.session_state.current_entry = ""
        st.session_state.current_mood = None
        
        # Remove data file
        if os.path.exists('diary_data.json'):
            os.remove('diary_data.json')
        
        st.success("All data cleared successfully!")
        st.rerun()
    
    def download_data_backup(self):
        """Download data backup"""
        self.export_data()

# Main application
if __name__ == "__main__":
    app = StudentDiaryApp()
    app.run()
