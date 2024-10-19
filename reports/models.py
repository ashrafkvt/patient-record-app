from django.db import models


class PatientReport(models.Model):
    clinic_name = models.CharField(max_length=255)
    clinic_logo_key = models.CharField(max_length=255, blank=True, null=True)
    physician_name = models.CharField(max_length=255)
    physician_contact = models.CharField(max_length=255)
    patient_first_name = models.CharField(max_length=255)
    patient_last_name = models.CharField(max_length=255)
    patient_dob = models.DateField()
    patient_contact = models.CharField(max_length=255)
    chief_complaint = models.TextField(max_length=5000)
    consultation_note = models.TextField(max_length=5000)

    def __str__(self):
        return f"{self.patient_first_name} {self.patient_last_name}"
