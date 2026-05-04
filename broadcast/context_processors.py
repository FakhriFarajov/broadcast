from article.models import Category


def global_context(request):
    """Add global context variables available to all templates"""
    return {
        'categories': Category.objects.all().order_by('name'),
        'selected_category': request.GET.get('category'),
        'search_query': request.GET.get('q', ''),
    }

