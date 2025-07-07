import streamlit as st
import pandas as pd
import random
import time
import openai
import pymongo
import certifi

# --- OpenAI API Key ---
openai.api_key = "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"

# --- MongoDB Configuration ---
MONGO_URI = "mongodb+srv://root:knight2364@mycluster.ffompy0.mongodb.net/?retryWrites=true&w=majority&appName=mycluster"
DB_NAME = "pcbuilds"  # Change if your database name is different

@st.cache_resource
def get_mongo_client():
    return pymongo.MongoClient(MONGO_URI, tlsCAFile=certifi.where())

client = get_mongo_client()
db = client[DB_NAME]

# --- Collection Mapping ---
collection_map = {
    "Cases": "case_data",
    "Case Fans": "case_fan_data",
    "CPU Coolers": "cpu_cooler_data",
    "CPUs": "cpu_data",
    "Ethernet Cards": "ethernet_card_data",
    "External Hard Drives": "external_hard_drive_data",
    "Fan Controllers": "fan_controller_data",
    "GPUs": "gpu_data",
    "Headphones": "headphones_data",
    "Internal Hard Drives": "internal_hard_drive_data",
    "Keyboards": "keyboard_data",
    "RAMs": "memory_data",
    "Monitors": "monitor_data",
    "Motherboards": "motherboard_data",
    "Mouses": "mouse_data",
    "Optical Drives": "optical_drive_data",
    "PSUs": "psu_data",
    "Sound Cards": "sound_card_data",
    "Speakers": "speakers_data",
    "Thermal Paste": "thermal_paste_data",
    "UPS": "ups_data",
    "Wireless Cards": "wireless_card_data"
}

# --- Helper Function to Fetch Data from MongoDB ---
def fetch_collection_data(collection_name):
    try:
        collection = db[collection_name]
        data = list(collection.find())
        # Remove MongoDB's internal _id for display
        for doc in data:
            doc.pop("_id", None)
        return pd.DataFrame(data)
    except Exception as err:
        st.error(f"An error occurred while fetching data from MongoDB: {err}")
        return pd.DataFrame()

# --- OpenAI Assistant Function ---
def get_pc_assistant_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for PC building."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error occurred while fetching response from OpenAI: {e}")
        return "Sorry, I couldn't process your request. Please try again."

# --- Streamlit App Configuration ---
st.set_page_config(page_title="PC Perfect - AI-Powered PC Building Assistant", layout="wide")

# --- Session State for Full-Screen Table View ---
if "full_screen" not in st.session_state:
    st.session_state["full_screen"] = False

# --- Sidebar for Database Exploration ---
with st.sidebar:
    st.sidebar.header("Explore Our Database 📊")
    tables = list(collection_map.keys())
    selected_table = st.sidebar.selectbox("Select a Component Category 🧩", tables, key="component_category", index=0)

# --- Centered Title with Underline Animation ---
st.markdown(
    """
    <style>
        .center-title {
            text-align: center;
            font-size: 3rem;
            color: #ff6f61;
            font-weight: bold;
            margin-bottom: 0.5em;
            position: relative;
        }
        .center-title::after {
            content: "";
            display: block;
            width: 100%;
            height: 3px;
            background-color: #ff6f61;
            position: absolute;
            bottom: -5px;
            left: 0;
            animation: underline-animation 3s ease-out forwards;
        }
        @keyframes underline-animation {
            0% { width: 0; }
            100% { width: 100%; }
        }
        .center-subheading {
            text-align: center;
            font-size: 1.5rem;
            color: #1e90ff;
            font-weight: normal;
            margin-top: 0;
            position: relative;
            transition: all 0.3s ease;
        }
        .center-subheading::after {
            content: "";
            display: block;
            width: 100%;
            height: 2px;
            background-color: #1e90ff;
            position: absolute;
            bottom: -5px;
            left: 0;
            animation: underline-subheading 3s ease-out forwards;
        }
        @keyframes underline-subheading {
            0% { width: 0; }
            100% { width: 100%; }
        }
        .response-box {
            background-color: #f4f6f9;
            border: 2px solid #1e90ff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .response-box h3 {
            color: #1e90ff;
            margin-top: 0;
        }
        .response-box p {
            color: #333;
        }
    </style>
    <div class="center-title">PC Perfect 🖥️</div>
    """,
    unsafe_allow_html=True,
)

# --- Subheading with Animation ---
subheading_messages = [
    "Start your dream PC journey today! 🚀",
    "Need advice? Let’s find your perfect PC configuration! 🛠️",
    "Ready to build the best gaming rig? Let’s go! 🎮",
    "Unlock the power of custom PC builds! ⚡",
    "Upgrade your PC with AI-powered recommendations! 💡"
]
selected_subheading = random.choice(subheading_messages)
st.markdown(f"""
    <div class="center-subheading">{selected_subheading}</div>
""", unsafe_allow_html=True)

# --- Custom Styles ---
st.markdown(""" 
    <style>
        .main {background-color: #F4F4F9;}
        .sidebar .sidebar-content {background-color: #30336b;}
        h1 {color: #ff6f61;}
        h2 {color: #1e90ff;}
        .stButton>button {background-color: #1e90ff; color: white; border-radius: 10px;}
        .stTextArea textarea {background-color: #e3f2fd;}
    </style>
""", unsafe_allow_html=True)

# --- User Input Section for Custom PC Build ---
st.write("### Enter Your PC Building Requirements ⚡")
user_prompt = st.text_area(
    "Describe your ideal PC configuration 💡",
    placeholder="E.g., I need a gaming PC with RTX 3080 and 16GB RAM.",
    height=150
)

# --- PC Building Suggestions ---
if st.button("Let's Build Your PC 🚀"):
    if user_prompt.strip():
        st.write("### Your Input 🤔")
        st.write(f"**Your Requirements:** {user_prompt}")
        st.write("### Suggested PC Build 🛠️")
        with st.spinner("Generating your perfect PC build... ⏳"):
            time.sleep(2)
        # You can use OpenAI to generate actual builds here
        st.markdown("""
            <div class="response-box">
                <h3>Here's a suggested build based on your preferences:</h3>
                <ul>
                    <li><strong>CPU:</strong> Intel Core i9-13900K 🧠</li>
                    <li><strong>GPU:</strong> Nvidia RTX 4080 🎮</li>
                    <li><strong>RAM:</strong> 32GB DDR5 🧰</li>
                    <li><strong>Storage:</strong> 1TB NVMe SSD 💾</li>
                    <li><strong>Case:</strong> NZXT H510 💡</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Please provide a valid input describing your PC needs!")

# --- Chatbot Input Section for PC Building Assistant ---
st.write("### Ask the PC Building Assistant for help 💬")
assistant_input = st.text_area(
    "Type your question here! (e.g., 'What CPU is best for gaming?')",
    placeholder="Ask for advice, suggestions, or info about PC building.",
    height=150
)
if st.button("Ask PC Assistant 🧑‍💻"):
    if assistant_input.strip():
        st.write("### Assistant's Response 🤖")
        with st.spinner("Thinking... ⏳"):
            assistant_response = get_pc_assistant_response(assistant_input)
            st.markdown(f"""
                <div class="response-box">
                    <h3>Assistant's Reply:</h3>
                    <p>{assistant_response}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please ask a valid question!")

# --- Footer ---
st.write("### Ready to start building your dream PC? 🌟")
st.write("Explore components like CPU, GPU, RAM, and more to create your perfect PC build! 🖱️")

# --- Show Data from the Selected Collection ---
if st.session_state["full_screen"]:
    selected_collection = collection_map[selected_table]
    data = fetch_collection_data(selected_collection)
    if not data.empty:
        st.write(f"### {selected_table} Database 📂 (Full Screen)")
        st.dataframe(data, use_container_width=True, height=800)
    else:
        st.warning(f"No data available in the **{selected_table}** category!")
    if st.button("Back to Home"):
        st.session_state["full_screen"] = False
        st.rerun()
else:
    st.write("### Welcome to PC Perfect!")
    st.write("Explore the database or build your dream PC with AI-powered suggestions.")
    if st.sidebar.button("Show Data"):
        st.session_state["full_screen"] = True
        st.rerun()
