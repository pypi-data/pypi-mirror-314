from datetime import date, datetime
from typing import Optional

from django.http import HttpRequest, HttpResponse

from rules.contrib.views import permission_required

from aleksis.core.util.pdf import render_pdf

from .util.chronos_helpers import (
    get_substitutions_context_data,
)


@permission_required("chronos.view_substitutions_rule")
def substitutions_print(
    request: HttpRequest,
    day: Optional[str] = None,
) -> HttpResponse:
    """View all substitutions on a specified day."""
    day = datetime.strptime(day, "%Y-%m-%d").date() if day else date.today()
    context = get_substitutions_context_data(day)
    return render_pdf(request, "chronos/substitutions_print.html", context)
