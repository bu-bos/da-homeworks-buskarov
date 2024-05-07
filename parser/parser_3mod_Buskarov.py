from types import NoneType
import requests
from bs4 import BeautifulSoup as BS
from bs4 import BeautifulSoup
import pandas as pd

products = []
categories = []
id_category = 0
id_prod = 0
url_link = 'https://kenwood.ru'
url = 'https://kenwood.ru/shop'
response_url = requests.get(url).text
soup_url = BeautifulSoup(response_url, 'html.parser')
category_items_url = soup_url.find_all(class_='shop-cart')


for item in category_items_url:   
    id_category = id_category + 1                                                           # Получаем название категрии товаров
    title_category = item.find(class_='shop-cart__title').text
    link_category = url_link + item['href']                                                 # Получем ссылку категории

    for i in range(1, 10):                                                                  #Чекаем каждую станицу раздела link_category
        url = link_category + '/' + str(i)
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        products_item = soup.find_all(class_='product-card--shop')

        for item in products_item:                                                          #Бегаем по i странице
    
            if item.find(class_='card-item__display-title') != None:                        # "Если карточка товара была обнаружена", т.к там есть рекламные контейнеры с таким классом
                title = item.find(class_='card-item__display-title').text                   # Наименование товара
                full_title = item.find(class_='card-item__title').text                      # Полное наименование товара
                link_product = url_link + item.select_one('.card-item > a')['href']         # Ссылка на товар
                id_prod = id_prod + 1
                
                if item.find(class_='prev') != None:                                        # Если есть 2 цены выводим по отдельности 
                    full_cost = item.find(class_='prev').text
                    full_cost = ''.join(full_cost.split())
                    lower_price = item.find(class_='curr').text
                    lower_price = ''.join(lower_price.split())

                else:                                                                       # Иначе выводим одну цену
                    full_cost = item.find(class_='curr').text
                    full_cost = ''.join(full_cost.split())
                    lower_price = full_cost


                if item.find(class_='label label-orange') != None:                          # Если есть дополнительная информация в карточке
                    additional = item.find(class_='label label-orange').text
                    if additional == 'Хит продаж':
                        additional = 'Хит продаж'
                    elif additional == 'New': 
                        additional = 'Новинка'
                    else:
                        pass                                                                # Иначе пропускаем условие
                else:
                    additional = 'Нет информации'


                if item.find(class_='label label-purple') != None:                          # Предзаказ\скидка - указываются в одном классе
                    percent = item.find(class_='label label-purple').text
                    if percent == 'Предзаказ':
                        sale = 'Предзаказ'
                    else: 
                        sale = percent
                else:
                    sale = 'В ниличии'


                if item.find(class_='not-available') != None:                               # Указано ли отсутствие товара
                    not_available = item.find(class_='not-available').text               
                    if not_available == 'Нет в наличии':
                        not_available == 'Нет в наличии'
                else:
                    not_available = 'В наличии'                                              # Иначе в наличии

                product = pd.DataFrame([{
                'id' : id_prod,
                'product_name' : full_title.strip(),
                'full_cost' : full_cost[:-1],
                'lower_price' : lower_price[:-1],
                'pre_order_sale' : sale,
                'id_category' : id_category,
                'category_name' : title_category.strip(),
                'additional' : additional,
                'availability' : not_available,
                'product_link' : link_product 
                }])
                products.append(product)

            else:
                pass



    category = pd.DataFrame([{
    'id_category' : id_category,
    'category_name' : title_category.strip()
    }])
    categories.append(category)

final_data = pd.concat(products)
final_data.to_csv('data.csv', encoding='utf-8', index=False)                                    #Первая табличка

final_categories = pd.concat(categories)
final_categories.to_csv('category.csv', encoding='utf-8', index= False)                         #Вторая табличка