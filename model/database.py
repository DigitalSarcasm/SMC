from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import create_engine, Column, Integer, String, Float, select, delete

_DATABASE_PATH = "sqlite:///data.db"

Base = declarative_base()
engine = create_engine(_DATABASE_PATH)

class Region(Base):
    """Model of a regional weather data set. Describes a small region of 1-50 km
       describing all pertinent weather data"""
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    coord_long = Column(Float)
    coord_lat = Column(Float)
    temperature = Column(Float)
    wind_speed = Column(Integer)
    humidity = Column(Integer)
    size = Column(Integer)

    def __repr__(self):
        return f"{self.id}:\t[{self.coord_long}, {self.coord_lat}],\t{self.temperature}C,\t{self.wind_speed}km/h,\t{self.humidity},\t{self.size}km"

    def dict(self):
        mapping = dict()
        mapping["id"] = self.id
        mapping["longitude"] = self.coord_long
        mapping["latitude"] = self.coord_lat
        mapping["temperature"] = self.temperature
        mapping["wind_speed"] = self.wind_speed
        mapping["humidity"] = self.humidity
        mapping["size"] = self.size
        return mapping

def initialize_db():
    """ Create all the tables outlined"""
    Base.metadata.create_all(engine)

def get_all_regions():
    with Session(engine) as sess:
        regions = list(sess.execute(select(Region)).scalars())
        return regions

def add_region(coord_long, coord_lat, temperature, wind_speed, humidity, size):
    reg = Region(coord_long=coord_long, coord_lat=coord_lat,
                 temperature=temperature, wind_speed=wind_speed,
                 humidity=humidity, size=size)

    with Session(engine) as sess:
        sess.add(reg)
        sess.commit()


def delete_all_regions():
    with Session(engine) as sess:
        sess.execute(delete(Region))
        sess.commit()


def add_region_obj(reg):
    with Session(engine) as sess:
        sess.add(reg)
        sess.commit()


def update_region(region):
    """Update a regions data"""
    pass # todo


def add_multiple_regions(regions):
    """Take a list of regions and add them to the database"""
    pass # todo

# if __name__ == "__main__":
    # add_region(1, 1, 25, 10, 50)
    # regions = get_all_regions()
    # for region in regions:
    #     print(region)