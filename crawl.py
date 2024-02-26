import requests
from bs4 import BeautifulSoup
import csv

# Define an empty list to hold the strings
product_urls = []

# Open the text file in read mode ('r')
with open('urls.txt', 'r') as file:
    # Iterate over each line in the file
    for line in file:
        # Strip any leading/trailing whitespace from the line and append it to the list
        product_urls.append(line.strip())

def scrape_amazon_product(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "DNT": "1",  # Do Not Track Request Header
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data using BeautifulSoup (e.g., product name, price)
        product_name = soup.find('span', id='productTitle').text.strip()
        review_count = soup.find('span', id='acrCustomerReviewText').text.strip().split()[0]
        review_avg = soup.find('span', attrs={'data-hook': 'rating-out-of-text'}).text.strip().split()[0]
        review_avg = float(review_avg.replace(",", "."))

        return {
            "name": product_name,
            "review_count": review_count,
            "review_average": review_avg,
        }
    else:
        return None

def save_to_csv(data, filename="product_data.csv"):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Write headers if file is empty
            writer.writerow(["Name", "Number of Reviews", "Average Rating"])
        for product_data in data:
            writer.writerow([product_data["name"], product_data["review_count"], product_data["review_average"]])

if __name__ == "__main__":
    all_product_data = []
    for url in product_urls:
        product_data = scrape_amazon_product(url)
        if product_data:
            all_product_data.append(product_data)
    
    all_product_data.sort(key=lambda x: int(x["review_count"].replace(",", "")), reverse=True)  # Assuming 'number_of_reviews' is a string, replace commas for conversion

    if all_product_data:
        save_to_csv(all_product_data)