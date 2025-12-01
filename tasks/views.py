from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response

from tasks.serializers import TaskInputSerializer
from tasks.models import Task
from .utils import calculate_priority


@require_GET
def index(request):
    # Regular Django view for the HTML frontend
    return render(request, "tasks/index.html")


@api_view(["POST"])
def analyze_tasks(request):
    """
    POST /api/tasks/analyze/

    Accepts a JSON array of tasks and returns a scored/sorted list.
    Also stores the tasks in the database so that /api/tasks/suggest/ can use them.
    """
    if not isinstance(request.data, list) or len(request.data) == 0:
        return Response(
            {"detail": "Provide a non-empty JSON array of tasks."},
            status=400,
        )

    serializer = TaskInputSerializer(data=request.data, many=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    validated_tasks = serializer.validated_data

    results = []

    with transaction.atomic():
        # For this simple demo we clear the table and replace it with the new batch.
        Task.objects.all().delete()

        for idx, data in enumerate(validated_tasks, start=1):
            deps = data.get("dependencies") or []

            metrics = calculate_priority(
                due_date=data["due_date"],
                estimated_hours=data["estimated_hours"],
                importance=data["importance"],
                dependencies=deps,
                self_id=idx,
            )

            # Store in DB
            Task.objects.create(
                title=data["title"],
                due_date=data["due_date"],
                estimated_hours=data["estimated_hours"],
                importance=data["importance"],
                dependencies=deps,
            )

            results.append(
                {
                    "id": idx,
                    "title": data["title"],
                    "due_date": data["due_date"],
                    "estimated_hours": data["estimated_hours"],
                    "importance": data["importance"],
                    "dependencies": deps,
                    "score": metrics["score"],
                    "explanation": metrics["explanation"],
                }
            )

    # Sort by score descending
    results.sort(key=lambda t: t["score"], reverse=True)
    return Response(results)


@api_view(["GET"])
def suggest_tasks(request):
    """
    GET /api/tasks/suggest/

    Uses the tasks stored by the last /api/tasks/analyze/ call
    and returns the top 3 tasks with natural-language explanations.
    """
    qs = Task.objects.all()
    if not qs.exists():
        return Response(
            {
                "detail": "No tasks found. Call POST /api/tasks/analyze/ with your task list first."
            },
            status=400,
        )

    items = []
    for obj in qs:
        deps = obj.dependencies or []
        metrics = calculate_priority(
            due_date=obj.due_date,
            estimated_hours=obj.estimated_hours,
            importance=obj.importance,
            dependencies=deps,
            self_id=obj.id,
        )
        items.append(
            {
                "id": obj.id,
                "title": obj.title,
                "due_date": obj.due_date,
                "estimated_hours": obj.estimated_hours,
                "importance": obj.importance,
                "dependencies": deps,
                "score": metrics["score"],
                "explanation": metrics["explanation"],
            }
        )

    items.sort(key=lambda t: t["score"], reverse=True)
    top3 = items[:3]
    return Response(top3)
