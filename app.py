from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Column,Integer,String, Sequence
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
engine = create_engine('sqlite:///storage.db',echo=True)
Session = sessionmaker(bind=engine)
Base=declarative_base()
class Apiuser(Base):
    __tablename__ = "apiusers"
    id = Column(String(20), primary_key=True) 
    real_name = Column(String(50))
    tz = Column(String(50))
    activity = relationship("Activity", 
        uselist=False, back_populates="apiuser")
class Activity(Base):
    __tablename__ = "activitys"
    id = Column(Integer, Sequence('seq_reg_id', start=1, increment=1),
               primary_key=True)
    start_time = Column(String(50))
    end_time = Column(String(50))
    apiuser_id = Column(Integer, ForeignKey('apiusers.id'))              
    apiuser = relationship("Apiuser", back_populates="activity") 
Base.metadata.create_all(engine)
session = Session()
user1 = Apiuser(id="W012A3CDE",real_name="Egon Spengler",tz="America/Los_Angeles")
activity1 = Activity(id=1,start_time="Feb 1 2020  1:33PM",
			end_time= "Feb 1 2020 1:54PM",apiuser=user1)
activity2 = Activity(id=2,start_time="Mar 1 2020  11:11AM",
			end_time= "Mar 1 2020 2:00PM",apiuser=user1)

activity3 = Activity(id=3,start_time="Mar 16 2020  5:33PM",
			end_time= "Mar 16 2020 8:02PM",apiuser=user1)
session.add(user1)
session.add(activity1)
session.add(activity2)
session.add(activity3)
session.commit()

user2 = Apiuser(id="W07QCRPA4",real_name="Glinda Southgood",tz="Asia/Kolkata")
activity1 = Activity(start_time= "Feb 1 2020  1:33PM",
			end_time= "Feb 1 2020 1:54PM",apiuser=user2)
activity2 = Activity(start_time="Mar 1 2020  11:11AM",
			end_time= "Mar 1 2020 2:00PM",apiuser=user2)

activity3 = Activity(start_time="Mar 16 2020  5:33PM",
			end_time= "Mar 16 2020 8:02PM",apiuser=user2)
session.add(user2)
session.add(activity1)
session.add(activity2)
session.add(activity3)
session.commit()


qry=session.query(Apiuser).all()
res=session.query(Activity).all()
store=dict()
for i in qry:
    store[i.id]={}
    store[i.id]['id']=i.id
    store[i.id]['real_name']=i.real_name
    store[i.id]['tz']=i.tz
    store[i.id]['activity_periods']=[]
for i in res:
    store[i.apiuser_id]['activity_periods'].append({'start_time':i.start_time,'end_time':i.end_time})
    
members=list(store.values())

final={'ok':True,'members':members}


from flask import *
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('show.html',dic=final)
app.run(port=3250,debug=True,use_reloader=False)








