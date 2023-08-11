import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
from pprint import pprint
import configparser
from model import create_tables, Publisher, Book, Shop, Sale, Stock

with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

DSN = 'postgresql://postgres:123@localhost:5432/sqlalchemy_bd'

engine = sq.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()

def insert():
    with open('data.json', 'r') as file:
        data = json.load(file)
    object_t = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }
    for insert in data:
        md = object_t[insert['model']]
        session.add(md(id=insert['pk'], **insert['fields']))
    session.commit()

def digit_name(vvod):
    if vvod.isdigit():
        return vvod
    else:
        return session.query(Publisher.id).filter(Publisher.name == vvod).scalar()

def zapros(publisher):
    for ansver in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)\
        .join(Sale.stock).join(Stock.shop).join(Stock.book)\
        .filter(Book.id_publisher == publisher).all():
        print(ansver[0].ljust(40), "|",\
            ansver[1].ljust(10), "|",\
            str(ansver[2]).ljust(4), "|",\
            ansver[3].strftime("%d-%m-%Y"))
    session.commit()

if __name__ == '__main__':
    create_tables(engine)
    insert()
    zapros(digit_name(input('Введите номер или имя: ')))
    session.close()