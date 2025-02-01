# AI-Powered Diary


The **AI-Powered Diary** is a personal journal application built with **Streamlit**, **Python**, and **MongoDB**, featuring sentiment analysis and AI-driven mood enhancement suggestions. The diary provides users with a **secure, private** space to log their emotions and track their mental well-being over time.

## Features
- **Password Protection**: Ensures privacy by requiring a password to access the diary.
- **Sentiment Analysis**: Uses **HuggingFace's sentiment analysis model** to classify user input as **positive, negative, or neutral**.
- **AI-Powered Chatbot**: Utilizes **Mistral AI** to provide **personalized responses and mood-enhancing suggestions**.
- **Mood Log Tracking**: Stores journal entries, sentiment scores, and chatbot responses in **MongoDB**.
- **Calendar View**: Displays a **visual history** of logged moods, helping users track their mental state over time.
- **Custom Styling**: Styled with **CSS** for an aesthetically pleasing dark-themed UI.

## Tech Stack
- **Frontend**: Streamlit, CSS
- **Backend**: Python, Mistral AI API, Hugging Face Transformers
- **Database**: MongoDB

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- MongoDB (running locally or hosted)
- Required Python libraries

### Steps
1. **Clone the repository**
```sh
 git clone https://github.com/your-repo/ai-powered-virtual-diary.git
 cd ai-powered-virtual-diary
```

2. **Install dependencies**
```sh
pip install -r requirements.txt
```

3. **Start MongoDB (if running locally)**
```sh
mongod --dbpath /path/to/mongodb/data
```

4. **Run the application**
```sh
streamlit run diary.py
```

## Usage
1. **Login** with the preset password.
2. **Enter a journal entry**, and the AI will analyze your sentiment.
3. **Receive chatbot recommendations** based on your mood.
4. **View past entries** and track your mood on the calendar.

## Configuration
- **Modify password**: Change the default password in `diary.py`.
- **Mistral AI Key**: Replace `API_KEY` with your **Mistral API key** in `diary.py`.
- **MongoDB Connection**: Update `MONGO_URI` if using a remote database.


## Below are the output snapshots:


<img width="956" alt="image" src="https://github.com/user-attachments/assets/98af3496-35c4-4d12-a055-fd2f288a620d" />



<img width="955" alt="image" src="https://github.com/user-attachments/assets/c5020235-2640-4e60-98f3-56a2cb75c656" />



<img width="953" alt="image" src="https://github.com/user-attachments/assets/71e30faa-089d-404b-a19b-1f5f4a61e977" />


## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please contact priyadharshinikameswaran@gmail.com


