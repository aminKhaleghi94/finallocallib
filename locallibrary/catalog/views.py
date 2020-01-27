from django.shortcuts import render
from django.views import generic
from . import models
from .models import Author, Book
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from django.views import generic
from django.urls import reverse_lazy
from .forms import RenewBookForm
from .serializers import BookSerializer,AuthorSeializer,BookInstancesSeializer
from rest_framework import generics



class Index(generic.TemplateView):
    template_name ='catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = models.Book.objects.all().count()
        context['num_instances'] = models.BookInstance.objects.all().count()
        context['num_instances_available'] = models.BookInstance.objects.filter(status__exact='a').count()
        context['num_authors'] = models.Author.objects.count()
        return context

class BookListView(generic.ListView):
    model = models.Book
    template_name = 'catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = models.Book
    template_name = 'catalog/book_detail.html'

class AuthorListView(generic.ListView):
    model = models.Author
    template_name = 'catalog/author_list.html'

class AuthorDetailView(generic.DetailView):
     model = models.Author
     template_name = 'catalog/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = models.BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(models.BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:my-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})

class AuthorCreate(generic.CreateView):
    model = models.Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018', }

class AuthorUpdate(generic.UpdateView):
    model = models.Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(generic.DeleteView):
    model = models.Author
    success_url = reverse_lazy('catalog:authors')


class APIListCreateBook(generics.ListCreateAPIView):
	queryset = Book.objects.all()
	serializer_class = BookSerializer

class APIRetrieveUpdateDestroyBook(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class APIListCreateAuthor(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSeializer

class APIRetrieveUpdateDestroyAuthor(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSeializer


class APIListCreateBookInstances(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = BookInstancesSeializer


class APIRetrieveUpdateDestroyBookInstances(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = BookInstancesSeializer