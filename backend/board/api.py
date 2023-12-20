from datetime import datetime, timedelta
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from board.models import Board

from consts.consts import UA_CITIES

@csrf_exempt
def main_page_ads(request):
    # time.sleep(3)
    page = int(request.GET.get('page', 1))
    posts = [
        {
            "id": 1,
            "title": 'A minor assistant is needed at the university at the department of CCD',
            "slug": '',
            "url": '',
            "rubric": 'Side hustle',
            "image_link": 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://images.ctfassets.net/wp1lcwdav1p1/3sg913Z9ssjN46MA7AuhJB/4b3d808dad5ebd280a49e22f07c23892/TcR0k5AA.jpeg?w=1500&h=680&q=60&fit=fill&f=faces&fm=jpg&fl=progressive&auto=format%2Ccompress&dpr=1&w=1000&h=',
            "age": '',
            "city": 'Dnipro, Dnipropetrovsk Region',
            "published_date": datetime.today() - timedelta(days=10),
            "content": "\nVacancy: Assistant for moving things at the university\n\nResponsibilities:\n\nCarrying out the transfer of belongings of university students and staff to new premises.\nPacking and placing items according to the instructions.\nCareful handling of personal belongings and common items.\nOrganizing the work of the team of movers and assigning tasks.\nAdherence to the moving schedule and deadlines.\n\nRequirements:\n\nPhysical endurance and ability to work under pressure.\nResponsible attitude to the performance of assigned tasks.\nOrganizational skills for effective teamwork.\nPolite and friendly communication with customers and colleagues.\nWillingness to perform physical work in different conditions (stairs, corridors, etc.).\nAbility to work in accordance with instructions and follow safety rules.\n\nWe offer:\n\nA friendly and supportive team.\nOpportunity to develop skills in the organization of relocations.\nCompetitive salary and bonus rewards.\nUnique work experience in a university environment.\n\nIf you are looking for an opportunity to contribute to the improvement of the university environment and help students and staff with the transfer of their belongings, we are waiting for your application. Join our team of porters where your physical strength, organization and friendliness will help make the moving process more comfortable and efficient.\n",
            "price": '20',
            "currency": '$',
            "owner": {
                "profile_link": "",
                "name": "Dmitry Buslov",
                "phone_number": "+380987654321",
                "email": "user@gmail.com",
                "is_official": False,
            },
            "is_added_to_favourites": False,
        },
        {
            "id": 2,
            "title": "Part-time Research Assistant Position Available in Biology Department",
            "slug": "",
            "url": "",
            "rubric": "Academic Opportunities",
            "image_link": "https://health.clevelandclinic.org/wp-content/uploads/sites/3/2021/10/tiredWomanDeskWork-1158202021-770x533-1-745x490.jpg",
            "age": "",
            "city": "San Francisco, California",
            "published_date": "2023-11-15T00:00:00",
            "content": "\nVacancy: Research Assistant for Biology Department\n\nResponsibilities:\n\nAssisting faculty in conducting biological research projects.\nCollecting and analyzing data under supervision.\nPreparing laboratory materials and maintaining equipment.\nCollaborating with team members on research initiatives.\nAssisting in literature reviews and documentation.\n\nRequirements:\n\nBackground in biology or related fields (coursework or experience).\nStrong organizational and research skills.\nAbility to work in a team and follow research protocols.\nProficiency in data analysis tools and software.\nExcellent written and verbal communication skills.\n\nWe offer:\n\nValuable experience in biological research projects.\nFlexible hours suitable for students.\nCompensation based on experience and contribution.\nOpportunity to work with esteemed faculty.\n\nJoin our team and contribute to exciting research endeavors in the field of biology!",
            "price": "25",
            "currency": "$",
            "owner": {
                "profile_link": "",
                "name": "Dr. Sarah Johnson",
                "phone_number": "+1 (123) 456-7890",
                "email": "sjohnson@example.com",
                "is_official": False
            },
            "is_added_to_favourites": False
        },
        {
            "id": 3,
            "title": "Remote Coding Instructor Needed for Online Learning Platform",
            "slug": "",
            "url": "",
            "rubric": "Education",
            "image_link": "https://media.istockphoto.com/id/1477041008/uk/%D1%84%D0%BE%D1%82%D0%BE/%D1%89%D0%B0%D1%81%D0%BB%D0%B8%D0%B2%D1%96-%D0%B1%D0%B0%D0%B3%D0%B0%D1%82%D0%BE%D0%BD%D0%B0%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%96-%D1%83%D1%81%D0%BC%D1%96%D1%85%D0%BD%D0%B5%D0%BD%D1%96-%D0%B4%D1%96%D0%BB%D0%BE%D0%B2%D1%96-%D0%B6%D1%96%D0%BD%D0%BA%D0%B8-%D1%8F%D0%BA%D1%96-%D0%BF%D1%80%D0%B0%D1%86%D1%8E%D1%8E%D1%82%D1%8C-%D1%80%D0%B0%D0%B7%D0%BE%D0%BC-%D0%B2-%D0%BE%D1%84%D1%96%D1%81%D1%96.jpg?s=2048x2048&w=is&k=20&c=90DkJzlf4RYv9-sp3WYHPqso3GvaMjpvvOnVulcaid0=",
            "age": "",
            "city": "Remote",
            "published_date": "2023-11-20T00:00:00",
            "content": "\nVacancy: Coding Instructor for Online Learning\n\nResponsibilities:\n\nTeaching coding fundamentals and advanced concepts remotely.\nCreating engaging coding lessons and exercises.\nProviding feedback and guidance to students.\nAssisting in curriculum development.\nEncouraging collaborative learning among students.\n\nRequirements:\n\nProficiency in programming languages like Python, JavaScript, etc.\nExperience in teaching or mentoring coding students.\nStrong communication and presentation skills.\nAbility to adapt teaching methods to different learning styles.\nPassion for education and technology.\n\nWe offer:\n\nFlexible schedule with remote work opportunities.\nCompetitive compensation based on teaching hours.\nChance to impact students globally through online education.\nSupportive team and resources for lesson planning.\n\nJoin our platform and help aspiring coders achieve their learning goals!",
            "price": "30",
            "currency": "$",
            "owner": {
                "profile_link": "",
                "name": "Emily Rodriguez",
                "phone_number": "+1 (234) 567-8901",
                "email": "erodriguez@example.com",
                "is_official": False
            },
            "is_added_to_favourites": False
        }
    ]
    data = {
        "result": [posts[page-1] if page <= len(posts) else None],
        "nextPage": page + 1 if page < len(posts) else None
    }
    return JsonResponse(data)


@csrf_exempt
def ua_cities(request):
    return JsonResponse({
        "cities": UA_CITIES,
    })



from rest_framework import permissions, viewsets
from board.serializers import BoardSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
