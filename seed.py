from models import Restaurant,Customer,Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine('sqlite:///restaurant.db')

Session=sessionmaker(bind=engine)
session=Session()

#Sample Data
restaurant1=Restaurant(name='Social House', price=18000)
restaurant2=Restaurant(name='Karen Blixen',price=11000)
restaurant3=Restaurant(name='Cultiva', price=20000)

customer1=Customer(first_name='Paton',last_name='Bortolozzi')
customer2=Customer(first_name='Barb',last_name='Delacroux')
customer3=Customer(first_name='Diana',last_name='Fotitt')
customer4=Customer(first_name='Nat',last_name='Scotcher')
customer5=Customer(first_name='Bailie',last_name='Kornel')

review1=Review(restaurant=restaurant3,customer=customer5,star_rating=4)
review2=Review(restaurant=restaurant1,customer=customer2,star_rating=5)
review3=Review(restaurant=restaurant1,customer=customer3,star_rating=1)
review4=Review(restaurant=restaurant2,customer=customer5,star_rating=2)

session.add_all([restaurant1,restaurant2,restaurant3,customer1,customer2,customer3,customer4,customer5,review1,review2,review3,review4])
session.commit()

session.close