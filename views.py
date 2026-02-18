import os
import json
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from openai import OpenAI
from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by("-created_at")
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["category", "priority", "status"]
    search_fields = ["title", "description"]


class TicketStatsView(APIView):
    def get(self, request):
        total = Ticket.objects.count()
        open_count = Ticket.objects.filter(status="open").count()

        per_day = (
            Ticket.objects
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
            .aggregate(avg=Avg("count"))
        )

        priority_breakdown = dict(
            Ticket.objects.values("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )

        category_breakdown = dict(
            Ticket.objects.values("category")
            .annotate(count=Count("id"))
            .values_list("category", "count")
        )

        return Response({
            "total_tickets": total,
            "open_tickets": open_count,
            "avg_tickets_per_day": per_day["avg"] or 0,
            "priority_breakdown": priority_breakdown,
            "category_breakdown": category_breakdown,
        })


class ClassifyTicketView(APIView):
    def post(self, request):
        description = request.data.get("description")

        if not description:
            return Response({"error": "Description required"}, status=400)

        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            prompt = f"""
You are a support ticket classifier.

Categories: billing, technical, account, general
Priorities: low, medium, high, critical

Return ONLY valid JSON:
{{"category": "...", "priority": "..."}}

Ticket:
{description}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)

            return Response({
                "suggested_category": parsed.get("category"),
                "suggested_priority": parsed.get("priority"),
            })

        except Exception:
            return Response({
                "suggested_category": None,
                "suggested_priority": None,
            })
