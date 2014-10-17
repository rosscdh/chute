# -*- coding: utf-8 -*-
from django.http import Http404
from django.core import signing
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView, TemplateView, RedirectView
from django.views.generic.edit import BaseUpdateView
from django.shortcuts import get_object_or_404

from payments.models import Charge, Customer

from chute.apps.me.signals import send_welcome_email
#from chute.mixins import AjaxFormView, AjaxModelFormView, ModalView

from .models import UserProfile

from .mailers import ValidateEmailMailer

from .forms import (ConfirmAccountForm,
                    ChangePasswordForm,
                    AccountSettingsForm,
                    LawyerLetterheadForm,
                    PlanChangeForm,
                    AccountCancelForm)

import json

import logging
logger = logging.getLogger('django.request')


class ConfirmAccountView(UpdateView):
    form_class = ConfirmAccountForm
    model = User
    template_name = 'user/settings/account.html'

    def dispatch(self, request, *args, **kwargs):

        # check to see if they have already set their password
        if request.user.is_authenticated() and request.user.password not in [None, '', '!']:
            messages.warning(request, 'It looks like you have already confirmed your account. No need to access that form.')
            return redirect(reverse('public:home'))

        return super(ConfirmAccountView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(ConfirmAccountView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        # get target user, profile
        profile = self.request.user.profile

        # if user is new, has not set password
        sent_welcome_email = profile.data.get('sent_welcome_email', False)
        if sent_welcome_email is False:
            #
            # Send welcome email
            #
            send_welcome_email.send(sender=self.request.user._meta.model, instance=self.request.user, created=True)

            # store the json reciept
            profile.data['sent_welcome_email'] = True
            profile.save(update_fields=['data'])

        return super(ConfirmAccountView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Thank you. You have confirmed your account')
        try:
            first_invite_key = self.request.user.invitations.all().first()
            return first_invite_key.next

        except AttributeError:
            # was no invite key
            return reverse_lazy('public:home')


class SendEmailValidationRequest(BaseUpdateView):
    def post(self, request, *args, **kwargs):
        """
        Jsut send it; if the user has already validated then we will catch that
        on the confirmation view
        """
        mailer = ValidateEmailMailer(((request.user.get_full_name(), request.user.email,),))
        mailer.process(user=request.user)

        content = {
            'detail': 'Email sent'
        }
        return HttpResponse(json.dumps(content), content_type='application/json', **kwargs)


# ------------------------------------------
# Start Settings Change Confirmation Views
# ------------------------------------------


class BaseConfirmValidationRequest(RedirectView):
    url = '/'  # redirect to home

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        self.user = self.get_user(token=kwargs.get('token'))
        self.profile = self.user.profile

        self.save()
        return super(BaseConfirmValidationRequest, self).dispatch(request=request, *args, **kwargs)

    def get_user(self, token):
        try:
            pk = signing.loads(token, salt=settings.URL_ENCODE_SECRET_KEY)
        except signing.BadSignature:
            raise Http404
        return get_object_or_404(User, pk=pk)

    def save(self):
        raise NotImplementedError


class ConfirmEmailValidationRequest(BaseConfirmValidationRequest):

    def save(self):
        self.profile.validated_email = True
        self.profile.save(update_fields=['data'])

        messages.success(self.request, 'Thanks. You have confirmed your email address.')
        logger.info(u'User: %s has validated their email' % self.user)


class ConfirmEmailChangeRequest(BaseConfirmValidationRequest):
    """
    When a user confirms that they want to change their email they come
    here and it does that for them.
    """

    def save(self):
        email = self.profile.data.get('validation_required_temp_email', False)
        original_email = self.user.email

        if email and email is not False:
            self.user.email = email
            self.user.save(update_fields=['email'])

            # remove temp password
            del self.profile.data['validation_required_temp_email']
            # set validated_email to True
            self.profile.validated_email = True
            self.profile.save(update_fields=['data'])

        messages.success(self.request, 'Congratulations. Your email has been changed. Please login with your new email.')
        logger.info(u'User: %s has confirmed their change of email address from: %s to: %s' % (self.user, original_email, self.user.email))


class ConfirmPasswordChangeRequest(BaseConfirmValidationRequest):
    """
    When a user confirms that they want to change their password they come
    here and it does that for them.
    """

    def save(self):
        password = self.profile.data.get('validation_required_temp_password', False)

        if password and password is not False:
            self.user.password = password
            self.user.save(update_fields=['password'])
            # remove temp password
            del self.profile.data['validation_required_temp_password']
            self.profile.save(update_fields=['data'])

        messages.success(self.request, 'Congratulations. Your password has been changed. Please login with your new password.')
        logger.info(u'User: %s has confirmed their change of password' % self.user)

# ----------------------------
# End Confirmation Views
# ----------------------------


class AccountSettingsView(UpdateView):
    form_class = AccountSettingsForm
    model = User
    success_url = reverse_lazy('me:settings')
    template_name = 'user/settings/account.html'

    def get_form_kwargs(self):
        kwargs = super(AccountSettingsView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user


#class ChangePasswordView(AjaxModelFormView, FormView):
class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('me:settings')
    template_name = 'user/settings/change-password.html'

    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'user': self.request.user
        })
        return kwargs


class LawyerLetterheadView(UpdateView):
    """
    View that handles the Letterhead Setup Form for Lawyers
    get the initial form data form the users profile.data
    form will save that data
    """
    form_class = LawyerLetterheadForm
    model = UserProfile
    template_name = 'lawyer/lawyerletterhead_form.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_initial(self):
        kwargs = super(LawyerLetterheadView, self).get_initial()

        profile = self.request.user.profile

        kwargs.update({
            'firm_name': profile.data.get('firm_name'),
            'firm_address': profile.data.get('firm_address'),
            'firm_logo': profile.data.get('firm_logo'),
        })
        return kwargs

    def get_success_url(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        else:
            return self.object.get_absolute_url() if self.object is not None and hasattr(self.object, 'get_absolute_url') else reverse('matter:list')

    def get_form_kwargs(self):
        kwargs = super(LawyerLetterheadView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class PaymentListView(ListView):
    template_name = 'payments/payment_list.html'

    def get_queryset(self):
        try:
            return Charge.objects.filter(customer=self.request.user.customer).order_by('-created_at')
        except Customer.DoesNotExist:
            return Charge.objects.none()


class PlanListView(TemplateView):
    template_name = 'payments/plan_list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanListView, self).get_context_data(**kwargs)
        context.update({
            'object_list': [settings.PAYMENTS_PLANS['early-bird-monthly'],]
        })
        return context


#class PlanChangeView(ModalView, AjaxFormView, FormView):
class PlanChangeView(FormView):
    form_class = PlanChangeForm
    template_name = 'payments/plan_change.html'

    def get_initial(self):
        return {
            'plan': self.kwargs.get('plan', None)
        }

    def form_valid(self, form):
        form.save()
        return super(PlanChangeView, self).form_valid(form)

    def get_object(self, **kwargs):
        slug = self.kwargs.get('plan', None)
        try:
            obj = settings.PAYMENTS_PLANS[slug]
        except KeyError:
            raise Http404("No plan found matching the id: {0}".format(slug))
        return obj

    def get_form_kwargs(self):
        kwargs = super(PlanChangeView, self).get_form_kwargs()
        kwargs.update({
            'plan': self.get_object(),
            'user': self.request.user,
        })
        return kwargs

    def get_success_url(self):
        return reverse('me:welcome')


#class AccountCancelView(ModalView, AjaxFormView, FormView):
class AccountCancelView(FormView):
    form_class = AccountCancelForm

    def form_valid(self, form):
        form.save()
        logout(self.request)
        return super(AccountCancelView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AccountCancelView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

    def get_success_url(self):
        return reverse('public:welcome')


class WelcomeView(TemplateView):
    template_name = 'me/welcome.html'
