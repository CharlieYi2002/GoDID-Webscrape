import requests
from bs4 import BeautifulSoup

# URL of the initial page
url = "https://godid.io/marketplace"

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all rows in the table
rows = soup.find_all('div', {'data-index': True, 'data-item-index': True})

data = []

for row in rows:
    # Extract the domain
    domain_div = row.find('div', class_='chakra-stack css-1igwmid')
    domain = domain_div.get_text(strip=True) if domain_div else 'N/A'

    # Extract the name
    name_p = row.find('p', class_='chakra-text css-1wydx3c')
    name = name_p.get_text(strip=True) if name_p else 'N/A'

    # Extract the profile URL
    profile_a = row.find('a', href=True)
    profile_url = profile_a['href'] if profile_a else 'N/A'

    # Extract the price
    price_p = row.find('p', class_='chakra-text css-0')
    price = price_p.get_text(strip=True) if price_p else 'N/A'

    # Store the extracted data
    data.append({
        'domain': domain,
        'name': name,
        'profile_url': profile_url,
        'price': price
    })

# Print the extracted data
for item in data:
    print("here")
    print(item)
