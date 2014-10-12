from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from CaseEntry.models import PatientRecord, PatientRecordForm, Case, PatientRecordReadOnlyForm
from CaseNotes.models import Note
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from Surgeon.models import Surgeon
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages


@login_required
def case_form(request, id=None):
    this_user = request.user
    form_editable = True
    import cStringIO
    from PIL  import Image
    if request.method == 'POST':
        PatientData = PatientRecordForm(request.POST)
        if PatientData.is_valid():
            # this saves the sketc
            canvasData = request.POST.get('canvasData', '')
            # img_string = canvasData.replace("data:image/jpeg;base64,", "");
            img_string = canvasData.replace("data:image/png;base64,", "");
            img_data = img_string.decode("base64")
            img_file = open("photo.png", "wb")
            img_file.write(img_data)
            img_file.close()
            # now merge with the background
            from PIL import Image

            background = Image.open("test2.png")
            foreground = Image.open("photo.png")
            Image.alpha_composite(background, foreground).save("test3.png")
            # this also works..
            # background.paste(foreground, (0, 0), foreground)
            # background.save('photo2b.png')
            new_case = Case()
            new_case.patientrecord = PatientData.save()
            new_case.surgeon = this_user.surgeon
            new_case.save()
            messages.add_message(request, messages.INFO, '%s: new case created' % new_case.patientrecord.patient)
            return HttpResponseRedirect(reverse_lazy('caselist'))
    else:
        if id:
            PatientData = PatientRecordReadOnlyForm(
                instance=PatientRecord.objects.get(pk=int(id)),
            )
            form_editable = False
        else:
            PatientData = PatientRecordForm()
    return render(request, 'case_form.html', {'form': PatientData,
                                              'path':request.META['PATH_INFO'],
                                              'form_editable': form_editable,
                                              'user': this_user})




class StatusForm(ModelForm):
    class Meta:
        model = Case
        fields = ['status', ]


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['message', ]


def view_case(request, id):
    id = int(id)
    this_user = request.user
    try:
        case = Case.objects.get(id=id)
        if request.method == 'POST':
            NoteData = NoteForm(request.POST)
            StatusData = StatusForm(request.POST)
            if StatusData.is_valid() and this_user.is_superuser:
                case.status = StatusData.cleaned_data['status']
                case.save()
            if NoteData.is_valid():
                new_note = NoteData.save()
                new_note.case = case
                new_note.commenter = this_user
                new_note.save()
        noteform = NoteForm()
        statusform = StatusForm(instance=case)
        return render(request, 'case.html', {'case': case,
                                             'user': this_user,
                                             'path':request.META['PATH_INFO'],
                                             'noteform': noteform,
                                             'statusform': statusform})
    except Case.DoesNotExist:
        return HttpResponse('case not accessible')


class CaseList(ListView):
    model = Case
    context_object_name = 'cases'
    template_name = 'surgeon_home.html'

    def get_context_data(self, **kwargs):
        # a superuser created in python might not have 1-1 Surgeon model associated
        this_user = self.request.user
        try:
            thissurgeon = this_user.surgeon
        except Surgeon.DoesNotExist:
            this_user.surgeon = Surgeon()
            this_user.surgeon.save()
            this_user.save()
        context = super(CaseList, self).get_context_data(**kwargs)
        context['surgeon'] = self.request.user
        context['path'] = self.request.META['PATH_INFO']
        if context['surgeon'].is_superuser:
            context['cases'] = Case.objects.all()
        else:
            context['cases'] = context['surgeon'].surgeon.case_set.all()
        return context