from sqlalchemy.orm import Session, joinedload
from . import models, schemas

def get_news(db: Session, news_id: int):
    return db.query(models.News).filter(models.News.id == news_id).first()

def get_news_list(db: Session, skip: int = 0, limit: int = 10):
    print(db, skip, limit)
    return db.query(models.News).offset(skip).limit(limit).all()

def get_or_create_category(db: Session, name: str, description: str):
    category = db.query(models.Category).filter(models.Category.name == name).first()
    if category is None:
        category = models.Category(name=name, description=description)
        db.add(category)
        db.commit()
        db.refresh(category)
    return category

def get_or_create_reporter(db: Session, name: str, email: str):
    reporter = db.query(models.Reporter).filter(models.Reporter.name == name).first()
    if reporter is None:
        reporter = models.Reporter(name=name, email=email)
        db.add(reporter)
        db.commit()
        db.refresh(reporter)
    return reporter

# def get_or_create_publisher(db: Session, name: str, website: str):
#     publisher = db.query(models.Publisher).filter(models.Publisher.name == name).first()
#     if publisher is None:
#         publisher = models.Publisher(name=name, website=website)
#         db.add(publisher)
#         db.commit()
#         db.refresh(publisher)
#     return publisher

def get_or_create_publisher(db: Session, name: str, website: str, email: str = None):
    # Automatically set the email to "name@gmail.com" if not provided
    if email is None:
        # email = f"{name.lower().replace(' ', '')}@gmail.com"
        # email= "hfujsfb@gmail.com"
        email= f"{name.lower().replace(' ', '')}@gmail.com"
        print(email)
        print(name)

    publisher = db.query(models.Publisher).filter(models.Publisher.name == name).first()
    if publisher is None:
        publisher = models.Publisher(name=name, website=website, email=email)
        db.add(publisher)
        db.commit()
        db.refresh(publisher)
    return publisher


def get_news_existance(db: Session, news_title: str):
    return db.query(models.News).filter(models.News.title == news_title).first()

def create_image(db: Session, news_id: int, url: str):
    db_image = models.Image(news_id=news_id, url=url)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def create_news(db: Session, news: schemas.NewsCreate):
    category = get_or_create_category(db, news.news_category, f"{news.news_category} description")
    reporter = get_or_create_reporter(db, news.news_reporter, f"{news.news_reporter}@example.com")
    publisher = get_or_create_publisher(db, news.news_publisher, f"https://{news.publisher_website}")
    news_exist = get_news_existance(db, news_title=news.title)

    if news_exist:
        return news_exist

    db_news = models.News(
        # publisher_website=news.publisher_website,
        title=news.title,
        datetime=news.datetime,
        body=news.body,
        link=news.link,
        category_id=category.id,
        reporter_id=reporter.id,
        publisher_id=publisher.id
    )
    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    for image_url in news.images:
        create_image(db, news_id=db_news.id, url=image_url)

    # Force load all necessary relationships
    db_news = db.query(models.News).options(
        joinedload(models.News.category),
        joinedload(models.News.reporter),
        joinedload(models.News.publisher)
    ).filter(models.News.id == db_news.id).first()

    return db_news


# db_summary = crud.get_summary(db, summary_id=summary_id)
def get_summary(db: Session, summary_id: int):
    return db.query(models.SummaryCreate).filter(models.SummaryCreate.id == summary_id).first()
# summaries

# db_summary = crud.create_summary(db=db, summary=summary)
def create_summary(db: Session, summary: schemas.SummaryCreate):
    db_summary = models.SummaryCreate(**summary.dict())
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary


def insert_summary(db: Session, news_id: int, summary_text: str):
    db_summary = models.Summary(news_id=news_id, summary_text=summary_text)
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary