# **Job Scraper (CLI, Python)**  
**GitHub:** [github.com/christianptc/job-scraper-cli](https://github.com/christianptc/job-scraper-cli)  
**Technologies:** Python (Requests, SQLite3, Rich) · Git/GitHub  

---

## **Goal**  
Automation of the job search  

Extracts new job advertisements from **arbeitsagentur.de** and saves them in a database.  

---

## **How to Run**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/christianptc/job-scraper-cli
cd job-scraper-cli
```

### **2. Install Requirements**  
```bash
pip install -r requirements.txt
```

### **3. Start the Application**  
```bash
python main.py
```

---

## **Project Status (as of 30th December 2025)**  
This is a **finished personal project**, created with the intent of learning and automating my own job search.  
It scrapes jobs from **arbeitsagentur.de** using specific search filters and stores them in a **SQLite3 database**.  
You can also **track the status of each job position** by manually updating its status.  

Feel free to use this for your own job search by changing the search filters in:  
`modules/scraper.py` → **line 10 + 11**  

---
