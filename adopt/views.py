from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic, View
from django.core.exceptions import PermissionDenied, BadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import AdoptionRequest
from cats.models import Cat

@login_required
def my_adoptions(request):
    context = {}

    # Display only the adoption request for this user
    user_adoptions = AdoptionRequest.objects.filter(user=request.user)

    # Separate the adoption requests in three lists depending on the
    # status, so that they can be displayed separately
    context["has_requests"] = user_adoptions.exists()
    context["approved_list"] = user_adoptions.filter(status=AdoptionRequest.Status.APPROVED).all()
    context["pending_list"] = user_adoptions.filter(status=AdoptionRequest.Status.PENDING).all()
    context["rejected_list"] = user_adoptions.filter(status=AdoptionRequest.Status.REJECTED).all()

    return render(request, "adopt/my_adoptions.html", context)

@login_required
def request_adoption(request, cat_id):
    # This view creates an adoption request object in the backend, so
    # the POST method must be used
    if request.method != "POST":
        messages.error(request, 'Adoption requests have to be POSTed!')
        return render(request, "405.html", status=405)

    # Check if a request by that user for that cat already exists
    if AdoptionRequest.objects.filter(user__id=request.user.id, cat__id=cat_id).exists():
        messages.error(request, 'You have already requested to adopt this cat!')
        return redirect("cats:detail", pk=cat_id)

    # Create the adoption request for the specified cat
    adoption_request = AdoptionRequest(user=request.user, cat=Cat.objects.get(pk=cat_id))
    adoption_request.save()

    # Redirect user to the "My Adoptions" page
    return redirect("adopt:my_adoptions")

@login_required
def delete_adoption(request):
    # This view deletes an adoption request object in the backend, so
    # the POST method must be used
    if request.method != "POST":
        messages.error(request, 'Adoption deletion requests have to be POSTed!')
        return render(request, "405.html", status=405)

    # A list of adoption request ids to delete is given in the url parameter <to_delete>
    ids_to_delete = request.POST.getlist("to_delete")
    if not ids_to_delete:
        raise BadRequest()

    # If a mistake such as trying to delete a request id belonging to another user, or
    # not existing at all was made in the URL, don't delete anything

    # 1st pass checks that all ids to delete are valid
    adoption_requests = []
    for adoption_id in ids_to_delete:
        adoption_request = get_object_or_404(AdoptionRequest, pk=adoption_id)

        if adoption_request.user.id != request.user.id:
            raise PermissionDenied()

        adoption_requests.append(adoption_request)

    # 2nd pass actually performs the deletions
    for adoption_request in adoption_requests:
        adoption_request.delete()

    # Redirect user to the "My Adoptions" page
    return redirect("adopt:my_adoptions")
    

