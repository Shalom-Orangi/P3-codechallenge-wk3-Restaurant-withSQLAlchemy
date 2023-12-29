from sqlalchemy import create_engine,Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship

engine=create_engine('sqlite:///restaurant.db', echo=True)


Session=sessionmaker(bind=engine)
session=Session()

Base=declarative_base()

class Restaurant(Base):
    __tablename__='restaurants'

    #columns 
    id=Column(Integer,primary_key=True)
    name=Column(String)
    price=Column(Integer)

    #one to many rel
    reviews=relationship('Review', back_populates='restaurant')

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by((cls.price)).first()
 
    def all_reviews(self):
        return[review.full_review()for review in self.reviews]

class Customer(Base):
    __tablename__='customers'

    #columns
    id=Column(Integer,primary_key=True)
    first_name=Column(String)
    last_name=Column(String)

    #one-to-many rel
    reviews=relationship('Review',back_populates='customer')
    
    #many-to-many rel
    restaurants=relationship('Restaurant',secondary='reviews',back_populates='customers')

    def full_name(self):
        return f"{self.first_name}{self.last_name}"
    
    def favourite_restaurant(self):
        return (
            session.query(Restaurant)
            .join(Review)
            .filter(Review.customer_id==self.id)
            .order_by(Review.star_rating.desc())
            .limit(1)
        )
    
    def add_review(self,restaurant,rating):
        new_review=Review(customer_id=self.id,restaurant_id=restaurant.id,star_rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self,restaurant):
        reviews_to_delete=session.query(Review).filter(Review.restaurant ==restaurant, Review.customer ==self).all()
        for review in reviews_to_delete:
            session.delete(review)
        session.commit()


class Review(Base):
    __tablename__='reviews'

    #columns
    id=Column(Integer,primary_key=True)
    restaurant_id=Column(Integer,ForeignKey('restaurants.id'))
    customer_id=Column(Integer,ForeignKey('customers.id'))
    star_rating=Column(Integer)

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name}: {self.star_rating} stars."

  