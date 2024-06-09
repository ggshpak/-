import requests
from bs4 import BeautifulSoup


class DromParser:
    def __init__(self):
        self.url = "https://auto.drom.ru/all/page1/"  # Стартовая страница
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

    def parse_drom_latest(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            car_listings = soup.find_all('a', class_='css-4zflqt e1huvdhj1')
            car_data = []
            for car_listing in car_listings[:20]:  # Берем первые 20 объявлений
                car_info = {}
                name_element = car_listing.find('div', class_='css-16kqa8y e3f4v4l2').find('span')
                if name_element:
                    car_info['name'] = name_element.text.strip()
                price_element = car_listing.find('span', class_="css-46itwz e162wx9x0")
                if price_element:
                    car_info['price'] = price_element.text[:-2]
                city_element = car_listing.find('span', class_="css-1488ad e162wx9x0")
                if city_element:
                    car_info['city'] = city_element.text.split()[0]
                car_info['link'] = car_listing['href']

                car_data.append(car_info)

            return car_data

        else:
            print(f"Ошибка запроса: {response.status_code}")
            return None

if __name__ == "__main__":
    drom_parser = DromParser()
    car_data = drom_parser.parse_drom_latest()
    if car_data:
        with open('latest_cars.txt', 'w', encoding='utf-8') as f:
            for car in car_data:
                if "name" in car:
                    f.write(f"Название: {car['name']}\n")
                if "price" in car:
                    f.write(f"Цена: {car['price']}\n")
                if "city" in car:
                    f.write(f"Город: {car['city']}\n")
                f.write(f"Ссылка: {car['link']}\n\n")
        print("Данные сохранены в файл latest_cars.txt")
    else:
        print("Не удалось получить данные")