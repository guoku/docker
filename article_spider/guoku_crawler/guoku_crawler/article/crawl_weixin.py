from sqlalchemy import or_, and_

from guoku_crawler.db import session
from guoku_crawler.tasks import RequestsTask, app
from guoku_crawler.article.crawler import crawl_user_articles
from guoku_crawler.models import CoreGkuser, AuthGroup, CoreArticle
from guoku_crawler.models import CoreAuthorizedUserProfile as Profile
from guoku_crawler.config import logger

@app.task(base=RequestsTask, name='crawl_all_weixin')
def crawl_all_weixin():
    users = get_weixin_users()
    for user in users:
        try :
            crawl_user_articles.delay(user.profile.id, only_weixin=True)
        except Exception as e :
            logger.error('fatal , exception when crawl %s' %user)


def get_weixin_users():
    users = session.query(CoreGkuser).filter(
        CoreGkuser.authorized_profile.any(Profile.weixin_id.isnot(None)),
        CoreGkuser.groups.any(AuthGroup.name == 'Author')
    ).order_by(CoreGkuser.id.desc()).all()
    return users

if __name__ == '__main__':
    crawl_all_weixin()

