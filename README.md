# 📌 QueryPilot

🚀 **QueryPilot** is an AI-powered SQL query generator that allows users to **input natural language queries** and get **automatically generated SQL queries** along with **database results**. The project is built using **Flask**, **SQLite3**, and **TailwindCSS** for an interactive web interface.

---

## **🔹 Features**
- 🧠 **NLP to SQL Conversion** – Converts natural language queries into SQL queries.  
- 🔎 **Execute Queries on SQLite** – Runs queries on a selected SQLite database.  
- 📊 **Interactive Data Display** – Displays query results in a structured table format.  
- 🎨 **Modern UI with TailwindCSS** – Fully responsive and visually appealing.  
- ⚡ **Keyboard & Click Support** – Works with both the "Enter" key and the "Generate SQL" button.  
- 📌 **Pagination for Large Results** – Displays limited rows with a "See More" option.  

---

## **🛠 Tech Stack**
- **Backend:** Flask, SQLite3, Pandas  
- **Frontend:** HTML, TailwindCSS, JavaScript  
- **Database:** SQLite (Supports MySQL with minor modifications)  
- **NLP Model:** Google Gemini AI (for SQL query generation)  

---

## **📂 Project Structure**
```
QueryPilot/
│── static/                  # Static assets (CSS, JS, images)
│── templates/               # HTML templates for rendering UI
│── execute_query.py         # Executes SQL queries and returns results
│── generate_sql_query.py    # NLP-powered SQL query generator
│── app.py                   # Flask backend server
│── requirements.txt         # Required Python packages
│── README.md                # Project documentation
│── college.db               # SQLite database (generated from CSV files)
│── datasets/                # CSV files (converted into SQLite tables)
```

---

## **🚀 Installation & Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/NaturalLanguageToSQLQueryUsingGoogleGemini.git
cd QueryPilot
```

### **2️⃣ Set Up Virtual Environment (Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Start the Flask Application**
```sh
python app.py
```

### **5️⃣ Open in Browser**
Go to:  
```
http://127.0.0.1:5000
```

---

## **📌 Usage**
1. **Login / Sign Up**  
   - Create an account or log in using an existing one (User data is stored in SQLite/MySQL).  

2. **Select a Database**  
   - Choose from the available databases (auto-loaded from CSV files).  

3. **Enter a Natural Language Query**  
   - Example: *"Show all students from the Computer Science department."*  

4. **Click "Generate SQL Query" or Press Enter**  
   - The system will generate the SQL query and display it in the UI.  

5. **View Results**  
   - The first few rows will be displayed, with an option to "See More" for large datasets.  

---


