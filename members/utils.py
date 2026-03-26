

from izitoast.functions import izitoast
from django.http import HttpResponse

def showAlert(request, message, alert_type):
    
    diversify = {
        "position": "topRight",
        "transition_in": "flipInX",
        "transition_out": "flipOutX",
        "time_out": 3000,
    }

    izitoast(
        request=request,
        model="success",  # or "error", "warning", "info"
        message="Operation completed successfully!",
        diversify=diversify
    )

    return HttpResponse("Alert triggered")
from izitoast.functions import izitoast

