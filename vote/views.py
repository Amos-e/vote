import json
import random

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from . import models
from main import models as main_models

def index(request):

    try:
        active_poll = models.Poll.objects.get(active=True)
    except:
        active_poll = models.Poll.objects.create(title="Generic Poll", active=True)
        members = main_models.Member.objects.exclude(code="KYDI/000")
        
        for member in members:
            models.Eligible.objects.create(member=member)

    generic_poll = models.Poll.objects.first()
    #polls = models.Poll.objects.exclude(id=generic_poll.id)
    polls = models.Poll.objects.all()

    context = {
        "polls": polls,
        "active_poll": active_poll,
    }

    return render(request, "vote/vote.html", context)


def manage_view(request):

    if request.GET.get("action") == "deactivate":
        member_id = request.GET.get("id")
        member = models.Eligible.objects.get(id=member_id)
        member.active = False
        member.save()
        return redirect("/vote/manage")
    
    if request.GET.get("action") == "activate":
        member_id = request.GET.get("id")
        member = models.Eligible.objects.get(id=member_id)
        member.active = True
        member.save()
        return redirect("/vote/manage")

    generic_poll = models.Poll.objects.first()
    #polls = models.Poll.objects.exclude(id=generic_poll.id)
    polls = models.Poll.objects.all()
    active_poll = models.Poll.objects.get(active=True)

    eligible_voters = models.Eligible.objects.filter(active=True)
    ineligible_voters = models.Eligible.objects.filter(active=False)

    context = {
        "polls": polls,
        "active_poll": active_poll,
        "eligible_voters": eligible_voters,
        "ineligible_voters": ineligible_voters,
    }

    return render(request, "vote/manage.html", context)



def poll_view(request, slug):

    poll = models.Poll.objects.get(id=slug)
    votes = models.Vote.objects.filter(poll=poll)
    
    generic_poll = models.Poll.objects.first()

    #polls = models.Poll.objects.exclude(id=generic_poll.id)
    polls = models.Poll.objects.all()
    active_poll = models.Poll.objects.get(active=True)

    context = {
        "poll": poll,
        "votes": votes,
        "polls": polls,
        "active_poll": active_poll,
    }

    return render(request, "vote/poll.html", context)


def activate_poll(request, slug):
    polls = models.Poll.objects.all()
    poll = models.Poll.objects.get(id=slug)

    for poli in polls:
        poli.active = False
        poli.save()

    poll.active = True
    poll.save()

    return redirect("/vote")


def members(request):

    members = list(models.Eligible.objects.filter(active=True).values("member__code", "member__full_names"))

    data = json.dumps(members)
    
    return JsonResponse(data, safe=False)


@csrf_exempt
def cast_vote(request):   
    members = models.Eligible.objects.filter(active=True)
    poll = models.Poll.objects.get(active=True)
    votes = models.Vote.objects.filter(poll=poll).values_list("vote__member__code", flat=True)
    members_voted = models.Vote.objects.filter(poll=poll).values_list("voter__member__code", flat=True)

    voter_member_code = json.loads(request.body)["member_code"]

    try:
        voter = models.Eligible.objects.get(member__code=voter_member_code)
    except:
        context = {
            "status": 404,
            "description": "Voter Could not be found",
        }
        context = json.dumps(context)
        return JsonResponse(context, safe=False)

    context = {}

    while True:
        vote = random.choice(members)

        if vote.member.code == voter.member.code or vote.member.code in votes:
            continue
        
        if voter.member.code in members_voted:
            context.update({
                "status": 403,
                "status_text": "Record already exists"
            })
            break

        voted_finished = models.Vote.objects.create(poll=poll, voter=voter, vote=vote)

        context.update({
            "status": 200,
            "voter_code": voter.member.code,
            "voter_name": voter.member.full_names,
            "vote_code": vote.member.code,
            "vote_name": vote.member.full_names,
            "vote_image": vote.member.image.url,
        })

        break

    context = json.dumps(context)
    return JsonResponse(context, safe=False)


@csrf_exempt
def api_view(request):

    data = json.loads(request.body)

    if data.get("operation") == "search_members":
        search_term = data.get("search_term")
        members = list(models.Eligible.objects.filter(member__full_names__icontains=search_term).values('member__code', 'member__full_names'))

        context = json.dumps(members)
        return JsonResponse(context, safe=False)


    if data.get("operation") == "search_member":
        search_term = data.get("search_term")
        code = search_term
        context = {}

        try:
            member = models.Eligible.objects.get(member__code=code)
        except:
            context.update({
                "status": "404 Failed"
            })

        context.update({
            "code": member.member.code,
            "full_names": member.member.full_names,
            "image": member.member.image.url,
        })
        
        context = json.dumps(context)
        return JsonResponse(context, safe=False)
    
    if data.get("operation") == "create_poll":
        title = data.get("title")
        description = data.get("description")
        poll = models.Poll.objects.create(title=title, description=description)

        context = {
            "status": 200
        }

        context = json.dumps(context)
        return JsonResponse(context, safe=False)
    
    else:
        context = {
            "status": "404 Not Found"
        }

        context = json.dumps(context)
        return JsonResponse(context, safe=False)

        
