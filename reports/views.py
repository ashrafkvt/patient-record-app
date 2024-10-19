from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .serializer import PatientReportSerializer

from .utils import s3_client, create_presigned_url


class PatientReportView(APIView):
    def generate_patient_report_filename(self, patient_report):
        last_name = patient_report.patient_last_name
        first_name = patient_report.patient_first_name
        dob = patient_report.patient_dob
        return f'CR_{last_name}_{first_name}_{dob}.pdf'

    def get(self, request):
        # Render the form template
        return render(request, 'reports/patient_form.html')

    def post(self, request):
        # Handle form submission and create patient report
        serializer = PatientReportSerializer(data=request.data)
        if serializer.is_valid():
            patient_report = serializer.save()

            logo_url = create_presigned_url(
                patient_report.clinic_logo_key)
            html_string = render_to_string(
                'reports/report_template.html',
                {'report': patient_report, 'logo': logo_url})
            pdf_file = HTML(string=html_string).write_pdf()
            file_name = self.generate_patient_report_filename(patient_report)

            # Return the PDF as a downloadable file
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = \
                f'attachment; filename={file_name}'
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
