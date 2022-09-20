# 2) celery -A website worker -l INFO                           просто запуск
# 3) celery -A website worker -l INFO --pool=solo               для того, чтобы он уже выполнял действия
from datetime import datetime
from celery import shared_task
from .models import Board, DeletedAds

# 1) celery -A website beat 
@shared_task
def delete_24h():
    print('shared task')
    h24_obj = Board.objects.all()
    publications_list = []
    for obj in h24_obj:
        publication_lifetime = (datetime.today() - obj.published).days*24 + ((datetime.today() - obj.published).seconds/(60*60))
        if publication_lifetime <= 24:
            deleted_adt = DeletedAds.objects.create(title = obj.title, content = obj.content, price = obj.price, 
                published = obj.published, rubric = obj.rubric, region = obj.region, city = obj.city, age = obj.age, 
                currency = obj.currency, workers_amount = obj.workers_amount, author = obj.author, author_name = obj.author_name, 
                phone_number = obj.phone_number, email = obj.email, views = obj.views, status = obj.status, 
            )
            deleted_adt.save()

            obj.delete()
            publications_list.append(f'{obj.pk} : {obj.slug}')
    return publications_list
