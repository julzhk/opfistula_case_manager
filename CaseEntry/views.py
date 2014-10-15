import StringIO

from Core.models import paginate
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from CaseEntry.models import PatientRecord, PatientRecordForm, Case, PatientRecordReadOnlyForm
from CaseNotes.models import Note
from django.views.generic import ListView
from Surgeon.models import Surgeon
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from PIL import Image
from django.conf import settings


def save_sketch(request,id):
    # this saves the sketch
    canvasData = request.POST.get('canvasData', None)
    if not canvasData:
        return
    img_string = canvasData.replace("data:image/png;base64,", "")
    img_data = img_string.decode("base64")
    img_file = StringIO.StringIO(img_data)
    # now merge with the background
    backimgfn = '%s/static/case_form_background.png' % (settings.BASE_DIR)
    background = Image.open(backimgfn)
    foreground = Image.open(img_file)
    fn = '%s/uploads/sketch%s.png' % (settings.BASE_DIR,id)
    Image.alpha_composite(background, foreground).save(fn)
    img_file.close()


@login_required
def case_form(request, id=None):
    this_user = request.user
    form_editable = True
    if request.method == 'POST':
        PatientData = PatientRecordForm(request.POST)
        if PatientData.is_valid():
            new_case = Case()
            new_case.patientrecord = PatientData.save()
            new_case.surgeon = this_user.surgeon
            new_case.save()
            save_sketch(request,new_case.pk)
            messages.add_message(request, messages.INFO, '%s: new case created' % new_case.patientrecord.patient)
            return HttpResponseRedirect(reverse_lazy('caselist'))
    else:
        if id:
            PatientData = PatientRecordReadOnlyForm(
                instance=PatientRecord.published_objects.get(pk=int(id)),
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
        case = Case.published_objects.get(id=id)
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
    queryset = Case.published_objects.all()
    paginate_by = settings.PAGE_SIZE

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
            cases = Case.published_objects.all()
        else:
            cases = context['surgeon'].surgeon.case_set.all()
        page = self.request.GET.get('page', 1)
        context['cases'] = paginate(cases, page)
        return context

def serve_img(request,pk=12):
    import os.path
    import mimetypes
    mimetypes.init()
    try:
        id = int(pk)
        fn = '%s/uploads/sketch%s.png' % (settings.BASE_DIR,id)
        file_path = fn
        fsock = open(file_path,"r")
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        print "file size is: " + str(file_size)
        mime_type_guess = mimetypes.guess_type(file_name)
        if mime_type_guess is not None:
            response = HttpResponse(fsock, mimetype=mime_type_guess[0])
        # response['Content-Disposition'] = 'attachment; filename=' + file_name
    except IOError:
        from django.http.response import HttpResponseNotFound
        response = HttpResponseNotFound()
    return response