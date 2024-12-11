from dcim.models import Device
from django import forms
from django.utils.translation import gettext_lazy as _
from utilities.forms.widgets import APISelectMultiple
from virtualization.models import VirtualMachine

from netbox_authorized_keys.models import AuthorizedKey, AuthorizedKeyDevice, AuthorizedKeyVirtualMachine


class BaseAuthorizedKeyForm(forms.Form):
    authorized_keys = forms.ModelMultipleChoiceField(
        queryset=AuthorizedKey.objects.all(),
        widget=APISelectMultiple(api_url="api/plugins/authorized-keys/authorized-keys/"),
        required=True,
        label=_("Authorized Keys"),
    )

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        if obj:
            self.fields["authorized_keys"].queryset = self.get_queryset(obj)

    def get_queryset(self, obj):
        raise NotImplementedError("Subclasses must implement get_queryset method")


class AuthorizedKeyAddForm(BaseAuthorizedKeyForm):
    def get_queryset(self, obj):
        if isinstance(obj, Device):
            assigned_keys = AuthorizedKeyDevice.objects.filter(device=obj).values_list("authorized_key_id", flat=True)
        elif isinstance(obj, VirtualMachine):
            assigned_keys = AuthorizedKeyVirtualMachine.objects.filter(virtual_machine=obj).values_list(
                "authorized_key_id", flat=True
            )
        else:
            return AuthorizedKey.objects.none()

        return AuthorizedKey.objects.exclude(id__in=assigned_keys)


class AuthorizedKeyRemoveForm(BaseAuthorizedKeyForm):
    def get_queryset(self, obj):
        return obj.authorized_keys.all()
