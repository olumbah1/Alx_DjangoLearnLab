from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Document  # 👈 Your app name is correct here

def setup_groups_and_permissions():
    content_type = ContentType.objects.get_for_model(Document)

    permissions = {
        'can_view': Permission.objects.get(codename='can_view', content_type=content_type),
        'can_create': Permission.objects.get(codename='can_create', content_type=content_type),
        'can_edit': Permission.objects.get(codename='can_edit', content_type=content_type),
        'can_delete': Permission.objects.get(codename='can_delete', content_type=content_type),
    }

    group_permissions = {
        'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        'Editors': ['can_create', 'can_edit'],
        'Viewers': ['can_view'],
    }

    for group_name, perm_list in group_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        group.permissions.clear()
        for perm_codename in perm_list:
            group.permissions.add(permissions[perm_codename])
        group.save()
        print(f"Group '{group_name}' configured.")
setup_groups_and_permissions()
