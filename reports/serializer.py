# serializers.py
import boto3
import re

from rest_framework import serializers
from .models import PatientReport
from django.conf import settings
from datetime import datetime

from .utils import s3_client


class PatientReportSerializer(serializers.ModelSerializer):
    clinic_logo = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = PatientReport
        exclude = ('clinic_logo_key', )

    def validate_patient_contact(self, value):
        # Check if the value matches a pattern for valid contact numbers
        if not re.match(r'^\+?1?\d{6,15}$', value):
            raise serializers.ValidationError("Enter a valid contact number.")
        return value

    def validate_physician_contact(self, value):
        if not re.match(r'^\+?1?\d{6,15}$', value):
            raise serializers.ValidationError(
                "Enter a valid physician contact number.")
        return value

    def create(self, validated_data):
        clinic_logo = validated_data.pop('clinic_logo', None)
        patient_report = PatientReport.objects.create(**validated_data)

        if clinic_logo:
            file_name = clinic_logo.name.rsplit('.', 1)[0]
            file_ext = clinic_logo.name.rsplit('.', 1)[-1]
            modified_file_name = file_name + '_' + datetime.now().strftime(
                "%Y%m%d%H%M%S") + '.' + file_ext

            s3 = s3_client()
            file_key = f'clinic_logos/{modified_file_name}'
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
