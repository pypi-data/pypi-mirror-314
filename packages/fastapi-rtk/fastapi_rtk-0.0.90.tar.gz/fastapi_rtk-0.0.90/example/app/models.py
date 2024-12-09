from fastapi_rtk import Model, db
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

AssetApplication = Table(
    "AssetApplication",
    db.get_metadata("assets"),
    Column("id", Integer, primary_key=True),
    Column("asset_id", Integer, ForeignKey("Asset.id")),
    Column("application_id", Integer, ForeignKey("Application.id")),
)


class Application(Model):
    __bind_key__ = "assets"
    __tablename__ = "Application"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    assets = relationship("Asset", secondary=AssetApplication)
    # assets = relationship('Asset', secondary=AssetApplication, backref='Application')

    def __repr__(self):
        return self.name


class Asset(Model):
    __bind_key__ = "assets"
    __tablename__ = "Asset"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512), nullable=False)
    owner_id = Column(Integer, ForeignKey("unit.id"))
    owner = relationship("Unit", backref="owner")
    date_time = Column(DateTime())
    date = Column(Date())
    applications = relationship("Application", secondary=AssetApplication)
    # applications = relationship('Application', secondary=AssetApplication, backref='Asset')

    def __repr__(self):
        return self.name


class Unit(Model):
    __bind_key__ = "assets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(512), nullable=False)

    def __repr__(self):
        return self.name


class StringPk(Model):
    id = Column(String, primary_key=True)
    name = Column(String(512), nullable=False)

    def __repr__(self):
        return self.name
