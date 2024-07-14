import requests
from collections import Counter
from multiprocessing import Pool
import matplotlib.pyplot as plt
import re


def download_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return Counter(words)


def reduce_function(counter1, counter2):
    return counter1 + counter2


def visualize_top_words(word_count, top_n=10):
    most_common = word_count.most_common(top_n)
    words, counts = zip(*most_common)

    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title(f'Top {top_n} слів')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main(url):
    text = download_text(url)

    chunk_size = len(text) // 4
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    with Pool(processes=4) as pool:
        word_counters = pool.map(map_function, chunks)

    total_word_count = Counter()
    for counter in word_counters:
        total_word_count = reduce_function(total_word_count, counter)

    # Візуалізуємо топ-слова
    visualize_top_words(total_word_count)


if __name__ == '__main__':
    url = 'http://example.com'
    main(url)
