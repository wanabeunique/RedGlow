from django.shortcuts import render


def testView(request, *args, **kwargs):
    return render(request, template_name='mm_test.html')
