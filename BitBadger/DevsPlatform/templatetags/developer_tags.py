from django import template
from DevsPlatform.models import ProjectParticipant

register = template.Library()

@register.simple_tag(takes_context=True)
def UserIsNotProjectMember(context):
    request = context.get("request")
    project_details = context.get('project_details')
    is_user_in_the_project = ProjectParticipant.objects.filter(participant_name = request.user, project = project_details)
    join_type = project_details.add_priviledge
    print(join_type)
    if is_user_in_the_project:
        return False
    elif join_type == 3:
        return True
    else: 
        return False
