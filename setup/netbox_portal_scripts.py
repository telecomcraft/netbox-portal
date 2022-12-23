from django.contrib.contenttypes.models import ContentType

from extras.choices import CustomFieldTypeChoices
from extras.models.customfields import CustomField
from extras.scripts import Script


name = 'Netbox Portal Scripts (0.1)'


# We'll need the IDs of the content types we will attach the custom
# fields to.
contact_id = ContentType.objects.get(model='contact').id


def get_portal_fields():
    fields = CustomField.objects.filter(group_name='Portal Settings')
    return fields


class CreateCustomFieldsScript(Script):

    class Meta:
        name = "Create Netbox Portal Custom Fields"
        description = "Creates the Netbox Portal custom fields"
        commit_default = True

    def run(self, data, commit):

        # TODO: Add exception check to ensure these fields don't already exist

        if CustomField.objects.filter(name='portal_username').exists():
            self.log_failure('portal_username custom field already exists')
        else:
            portal_username = CustomField.objects.create(
                name='portal_username',
                label='Portal Username',
                group_name='Portal Settings',
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The portal username for the contact.",
            )
            portal_username.content_types.set([contact_id])
            portal_username.save()
            self.log_info("portal_username custom field created")

        if CustomField.objects.filter(name='portal_password').exists():
            self.log_failure('portal_password custom field already exists')
        else:
            portal_password = CustomField.objects.create(
                name='portal_password',
                label='Portal Password',
                group_name='Portal Settings',
                type=CustomFieldTypeChoices.TYPE_TEXT,
                description="The portal password for the contact.",
            )
            portal_password.content_types.set([contact_id])
            portal_password.save()
            self.log_info("portal_password custom field created")

        # Return the output to the script page
        self.log_success('Generation of custom fields complete')


class UpdateCustomFieldsScript(Script):

    class Meta:
        name = "Update Netbox Portal Custom Fields"
        description = "Updates the Netbox Portal custom fields"
        commit_default = False

    def run(self, data, commit):

        portal_username = CustomField.objects.get(name='portal_username')
        portal_username.label = 'Portal Username'
        portal_username.group_name = 'Portal Settings'
        portal_username.type = CustomFieldTypeChoices.TYPE_TEXT
        portal_username.description = "The portal username for the contact."
        portal_username.content_types.set([contact_id])
        portal_username.save()
        self.log_info("portal_username custom field updated")

        portal_password = CustomField.objects.get(name='portal_password')
        portal_password.label = 'Portal Password'
        portal_password.group_name = 'Portal Settings'
        portal_password.type = CustomFieldTypeChoices.TYPE_TEXT
        portal_password.description = "The portal password for the contact."
        portal_password.content_types.set([contact_id])
        portal_password.save()
        self.log_info("portal_password custom field updated")

        self.log_success('All portal fields updated')


class RemoveCustomFieldsScript(Script):

    class Meta:
        name = "Remove Netbox Portal Custom Fields"
        description = "Removes the Netbox Portal custom fields"
        commit_default = False

    def run(self, data, commit):
        fields = get_portal_fields()

        for field in fields:
            CustomField.objects.filter(id=field.id).delete()
            self.log_info(f"{field.name} removed")

        self.log_success('All portal fields removed')


script_order = (
    CreateCustomFieldsScript,
    UpdateCustomFieldsScript,
    RemoveCustomFieldsScript
)
