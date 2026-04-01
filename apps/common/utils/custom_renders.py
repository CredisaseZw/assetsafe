from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

def _create_rendered_response(data, status_code=status.HTTP_200_OK,get_renderer_context=None):
    """Helper to create and render a DRF Response."""
    rendered_content = JSONRenderer().render(data)
    response = Response(rendered_content, status=status_code, content_type='application/json')
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = 'application/json'
    response.renderer_context = get_renderer_context() 
    response.render()
    return response