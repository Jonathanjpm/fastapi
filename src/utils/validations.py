from fastapi import HTTPException, status

def validate_unique_constrain(article, db_article):
    if article.title == db_article.title:
        article.title = None
    
    if article.author == db_article.author:
        article.author = None

    return article

def validate_content(item, message):
    if not item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
def validate_page(article_filters):
    if article_filters.page <= 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"The pagination value must be greater than 0"
        )