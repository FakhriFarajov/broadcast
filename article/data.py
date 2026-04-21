ARTICLES = [
    {
        "id": 0,
        "title": "Sample Article",
        "category": "AI",
        "description": "This is a sample article description.",
        "content": "This is the content of the sample article.",
        "author": "John Doe",
        "image_url": "https://res.cloudinary.com/dtzt9nrt9/image/upload/v1776626196/htu64nn2v2xnmtphhrmj.png",
        "created_at": "2024-06-01 12:00:00"
    }
]

id_init = 0

def get_articles():
    return ARTICLES

def get_article(id):
    for article in ARTICLES:
        if article["id"] == id:
            return article

def create_article(title, content, description, image_url,category, author, created_at):
    global id_init
    article = {
        "id": id_init,
        "title": title,
        "description": description,
        "content": content,
        "category": category,
        "author": author,
        "image_url": image_url,
        "created_at": created_at
    }
    ARTICLES.append(article)
    id_init += 1
    return article

