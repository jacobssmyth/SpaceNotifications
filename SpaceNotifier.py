import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
from datetime import datetime, timedelta
#uses gmail servers, requires gmail, app password, along with recipient address
sender_email = ""
app_password = ""
recipient_email = ""


url = "https://www.astronomy.com/tags/news/"


def scrape_latest_news(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

           
            latest_headline = soup.find("h2", class_="entry-title card-title")
            latest_link = latest_headline.find("a")["href"]

            return latest_headline.text, latest_link

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Function to send email notifications
def send_notification(news_summaries):
    message = MIMEText("Weekly Astronomical News Update:\n\n" + "\n\n".join(news_summaries))
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Weekly Astronomical News Update"

 
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
       
        server.login(sender_email, app_password)
        
      
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Weekly email sent successfully.")
        
        
        server.quit()
    except Exception as e:
        print(f"An error occurred while sending the weekly email: {e}")

if __name__ == "__main__":
    weekly_news_summaries = [] 
    last_week_start_date = datetime.now() - timedelta(days=datetime.now().weekday() + 7)

    while True:
       
        latest_headline, latest_link = scrape_latest_news(url)

        if latest_headline:
            print("New News Found!")
            print("Headline:", latest_headline)
            print("Link:", latest_link)
            
            # Append the latest news to the weekly summaries
            weekly_news_summaries.append(f"{latest_headline}\n{latest_link}")

        else:
            print("No new news found.")

        # Check if it's the end of the week
        current_date = datetime.now()
        if current_date - last_week_start_date >= timedelta(7):
            # Send a weekly email with news summaries and reset the summaries
            if weekly_news_summaries:
                send_notification(weekly_news_summaries)
            weekly_news_summaries = []
            last_week_start_date = current_date

        # Wait for a specified interval before checking again
        time.sleep(604800)  
