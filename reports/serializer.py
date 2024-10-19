# serializers.py
import boto3
from rest_framework import serializers
from .models import PatientReport
from django.conf import settings


class PatientReportSerializer(serializers.ModelSerializer):
    # clinic_logo = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = PatientReport
        exclude = ('clinic_logo_key', )

    def create(self, validated_data):
        # Handle file upload to S3
        clinic_logo = validated_data.pop('clinic_logo', None)
        patient_report = PatientReport.objects.create(**validated_data)

        if clinic_logo:
            # Upload file to S3
            s3 = boto3.client('s3')
            file_key = f'clinic_logos/{clinic_logo.name}'
            s3.upload_fileobj(
                clinic_logo.file,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_key,
                ExtraArgs={'ContentType': clinic_logo.content_type}
            )
            # Store the S3 file key in the model
            patient_report.clinic_logo_key = file_key
            patient_report.save()

        return patient_report
