import random

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission

from Customers.models import Client
from django.db import connection
from rest_framework import permissions


class RootPermission(permissions.BasePermission):
    message = 'No root'

    def has_permission(self, request, view):
        if request.user.client_source.categorie == Client.ROOT:
            return request.user.is_superuser
        return False

# Mis à l'extérieur pour pouvoir être utilisé
# tout seul dans les class view de Django sans RESTframework
def TenantAdminPermissionWithRequest(request):
    if request.user.is_authenticated:
        return any([
            all([
                connection.tenant in request.user.client_admin.all(),
                request.user.is_staff,
                request.user.is_active,
                request.user.espece == TibilletUser.TYPE_HUM
            ]),
            # Pour l'user ROOT qui peut tout faire
            all([
                request.user.client_source.categorie == Client.ROOT,
                request.user.is_superuser,
            ]),
        ])
    else:
        return False


class TenantAdminPermission(permissions.BasePermission):
    message = 'No admin in tenant'

    def has_permission(self, request, view):
        return TenantAdminPermissionWithRequest(request)


class TerminalScanPermission(permissions.BasePermission):
    message = "Termnal must be validated by an admin"

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return any([
                all([
                    connection.tenant in request.user.client_admin.all(),
                    request.user.is_active,
                    request.user.user_parent().is_staff,
                    request.user.espece == TibilletUser.TYPE_TERM
                ]),
                # Pour l'user ROOT qui peut tout faire
                all([
                    request.user.client_source.categorie == Client.ROOT,
                    request.user.is_superuser,
                ]),
            ])
        else:
            return False


class TibilletManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        # import ipdb; ipdb.set_trace()
        if not email:
            raise ValueError(_("email obligatoire"))

        email = self.normalize_email(email)
        user = self.model(**extra_fields)
        user.username = email
        user.email = email
        user.set_password(password)

        user.client_source = connection.tenant
        user.save()

        user.client_achat.add(connection.tenant)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self.set_permission_staff(self._create_user(email, password, **extra_fields))

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('can_create_tenant', True)
        return self._create_user(email, password, **extra_fields)

    def set_permission_staff(self, user):
        staff_group = Group.objects.get_or_create(name="staff")[0]
        user.groups.add(staff_group)


class TibilletUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS

    email = models.EmailField(_('email'), unique=True)  # changes email to unique and blank to false
    email_error = models.BooleanField(default=False)

    username = models.CharField(max_length=200, unique=True)

    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)

    phone = models.CharField(max_length=20, null=True, blank=True)

    last_see = models.DateTimeField(auto_now=True)
    accept_newsletter = models.BooleanField(
        default=True, verbose_name=_("J'accepte de recevoir la newsletter"))
    postal_code = models.IntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    can_create_tenant = models.BooleanField(default=False, verbose_name=_("Peux créer des tenants"))

    TYPE_TERM, TYPE_HUM, TYPE_ANDR = 'TE', 'HU', 'AN'
    ESPECE_CHOICES = (
        (TYPE_TERM, 'Terminal'),
        (TYPE_ANDR, 'Android'),
        (TYPE_HUM, 'Humain'),
    )

    espece = models.CharField(max_length=2,
                              choices=ESPECE_CHOICES,
                              default=TYPE_HUM)

    PUBLIC, FREE, PREMIUM, ENTREPRISE, CUSTOM = 'PU', 'FR', 'PR', 'EN', 'CU'
    OFFRE_CHOICES = (
        (PUBLIC, 'Public'),
        (FREE, 'Gratuit'),
        (PREMIUM, 'Premium'),
        (ENTREPRISE, 'Entreprise'),
        (CUSTOM, 'Custom'),
    )

    offre = models.CharField(max_length=2,
                             choices=OFFRE_CHOICES,
                             default=PUBLIC)

    # Inscription depuis :
    client_source = models.ForeignKey(Client,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      verbose_name=_("Inscription depuis"),
                                      related_name="user_principal",
                                      )

    # ou as t il acheté ?
    client_achat = models.ManyToManyField(Client,
                                          related_name="user_achats", blank=True)

    # sur quelle interface d'admin peut-il aller ?
    client_admin = models.ManyToManyField(Client,
                                          related_name="user_admin", blank=True)

    # is_active = models.BooleanField(
    #     _('active'),
    #     default=False,
    #     help_text=_(
    #         'Designates whether this user should be treated as active. '
    #         'Unselect this instead of deleting accounts.'
    #     ),
    # )

    ##### Pour les user terminaux ####

    user_parent_pk = models.UUIDField(
        null=True,
        blank=True,
        verbose_name=_("Utilisateur parent"),
    )

    def user_parent(self):
        if self.user_parent_pk:
            return TibilletUser.objects.get(pk=self.user_parent_pk)
        else:
            class user_vide:
                is_staff = False

            return user_vide

    local_ip_sended = models.GenericIPAddressField(blank=True, null=True)
    mac_adress_sended = models.CharField(blank=True, null=True, max_length=17)
    terminal_uuid = models.CharField(blank=True, null=True, max_length=200)

    ##### END user terminaux ####

    ##### Pour les user humain ####

    ##### END user humain ####

    def achat(self):
        return " ".join([achat["schema_name"] for achat in self.client_achat.values("schema_name")])

    def administre(self):
        return " ".join([admin["schema_name"] for admin in self.client_admin.values("schema_name")])

    # def new_tenant_authorised(self):
    #
    #     # si l'user est déja staff ou root, c'est qu'il a déja une billetterie.
    #     if self.offre in [self.PUBLIC, self.FREE, self.PREMIUM]:
    #         if len(self.client_admin.all()) > 0:
    #             # superuser peut toujours.
    #             return self.is_superuser
    #         else:
    #             return True
    #
    #     elif self.offre == self.ENTREPRISE:
    #         if len(self.client_admin.all()) > 4:
    #             # superuser peut toujours.
    #             return self.is_superuser
    #         else:
    #             return True
    #
    #     elif self.offre == self.CUSTOM:
    #         return True

    def as_p(self):
        return bool(self.password)

    def set_staff(self, tenant):
        self.client_admin.add(tenant)
        self.is_staff = True
        self.groups.add(Group.objects.get(name="staff"))
        self.save()

    def __str__(self):
        return self.email

    objects = TibilletManager()


# ---------------------------------------------------------------------------------------------------------------------


class TermUserManager(TibilletManager):
    def get_queryset(self):
        return super().get_queryset().filter(espece=TibilletUser.TYPE_TERM,
                                             client_admin__pk__in=[connection.tenant.pk, ],
                                             )


class TermUser(TibilletUser):
    class Meta:
        proxy = True
        verbose_name = "Terminal"
        verbose_name_plural = "Terminaux"

    objects = TermUserManager()

    def save(self, *args, **kwargs):
        # Si création :

        self.espece = TibilletUser.TYPE_TERM
        self.email = self.email.lower()

        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------------------------------------------------

class HumanUserManager(TibilletManager):

    def get_queryset(self):
        return super().get_queryset().filter(espece=TibilletUser.TYPE_HUM,
                                             is_staff=False,
                                             is_superuser=False,
                                             client_achat__pk__in=[connection.tenant.pk, ],
                                             )


class HumanUser(TibilletUser):
    class Meta:
        proxy = True
        verbose_name = "Utilisateur"

    objects = HumanUserManager()

    def save(self, *args, **kwargs):
        # Si création :
        if not self.pk:
            self.client_source = connection.tenant

        self.espece = TibilletUser.TYPE_HUM

        self.is_staff = False
        self.is_superuser = False
        self.email = self.email.lower()

        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------------------------------------------------

class SuperHumanUserManager(TibilletManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            espece=TibilletUser.TYPE_HUM,
            is_staff=True,
            is_superuser=False,
            client_admin__pk__in=[connection.tenant.pk, ],
        )


class SuperHumanUser(TibilletUser):
    class Meta:
        proxy = True
        verbose_name = "Administrateur"

    objects = SuperHumanUserManager()

    def save(self, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        # Si création :
        # if not self.pk:
        self.espece = TibilletUser.TYPE_HUM

        self.is_staff = True
        self.is_superuser = False
        self.email = self.email.lower()

        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------------------------------------------------


class TerminalPairingToken(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(TermUser, on_delete=models.CASCADE)
    token = models.PositiveIntegerField()
    used = models.BooleanField(default=False)
