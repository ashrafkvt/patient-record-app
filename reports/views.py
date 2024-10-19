from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .serializer import PatientReportSerializer


class PatientReportView(APIView):
    def get(self, request):
        # Render the form template
        return render(request, 'reports/patient_form.html')

    def post(self, request):
        # Handle form submission and create patient report
        serializer = PatientReportSerializer(data=request.data)
        if serializer.is_valid():
            patient_report = serializer.save()

            html_string = render_to_string(
                'reports/report_template.html', {'report': patient_report})
            pdf_file = HTML(string=html_string).write_pdf()

            # Return the PDF as a downloadable file
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = \
                f'attachment; filename="patient_report_{patient_report.id}.pdf"'
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
