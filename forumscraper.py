import requests
from bs4 import BeautifulSoup
import csv

def save_soup_to_text(soup, filename='soup_data.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def scrape_forum_posts(url, num_posts):
    all_posts = []
    page_num = 1

    while len(all_posts) < num_posts:
        print(f"iteration {page_num}")
        page_url = f"{url}/{page_num}" if page_num > 1 else url
        response = requests.get(page_url)
        if response.status_code != 200:
            print(f"Failed to fetch {page_url}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        save_soup_to_text(soup)
        post_elements = soup.find_all('div', class_='topic-body crawler-post')

        for post in post_elements:
            post_data = {}
            post_data['author'] = post.find('span', class_='creator').find('span', itemprop='name').text.strip()
            post_data['date'] = post.find('time', class_='post-time')['datetime']
            post_data['content'] = post.find('div', class_='post').text.strip()
            all_posts.append(post_data)
            if len(all_posts) == num_posts:
                break

        page_num += 1

    return all_posts[:num_posts]

def write_to_csv(posts_data, filename='forum_posts.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['author', 'date', 'content'])
        writer.writeheader()
        for post in posts_data:
            writer.writerow(post)

def main():
    url = "https://forums.t-nation.com/t/the-westside-method-thread/172488"
    num_posts = 21
    posts_data = scrape_forum_posts(url, num_posts)
    if posts_data:
        write_to_csv(posts_data)
        print("CSV file generated successfully.")
    else:
        print("Failed to scrape forum posts.")

if __name__ == "__main__":
    main()
