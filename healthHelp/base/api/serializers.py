from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from base.models import (
    User,
    Patient,
    Police,
    Driver,
    Hospital,
    EmergencyRequest,
    MedicalHistory,
    PatientTreatment,
    MobileNumber,
)


class DriverSerializer(serializers.ModelSerializer):
    face_image_url = serializers.SerializerMethodField()
    driving_license_document_url = serializers.SerializerMethodField()
    car_insurance_document_url = serializers.SerializerMethodField()
    car_rc_document_url = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = [
            'username', 'email', 'first_name', 'last_name', 'gender', 'address',
            'license_number', 'license_expiry', 'face_image', 'driving_license_document',
            'car_insurance_document', 'car_rc_document', 'face_image_url',
            'driving_license_document_url', 'car_insurance_document_url', 'car_rc_document_url'
        ]

    def get_face_image_url(self, obj):
        request = self.context.get('request')
        if obj.face_image and hasattr(obj.face_image, 'url'):
            return request.build_absolute_uri(obj.face_image.url)
        return None

    def get_driving_license_document_url(self, obj):
        request = self.context.get('request')
        if obj.driving_license_document and hasattr(obj.driving_license_document, 'url'):
            return request.build_absolute_uri(obj.driving_license_document.url)
        return None

    def get_car_insurance_document_url(self, obj):
        request = self.context.get('request')
        if obj.car_insurance_document and hasattr(obj.car_insurance_document, 'url'):
            return request.build_absolute_uri(obj.car_insurance_document.url)
        return None

    def get_car_rc_document_url(self, obj):
        request = self.context.get('request')
        if obj.car_rc_document and hasattr(obj.car_rc_document, 'url'):
            return request.build_absolute_uri(obj.car_rc_document.url)
    
        return None
    

class MedicalHistorySerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = MedicalHistory
        fields = ["id", "description", "document_url"]  # Added "id"

    def get_document_url(self, obj):
        if obj.document and hasattr(obj.document, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.document.url)
            # Fallback for development
            return f"https://healthhelp-backend.onrender.com/{obj.document.url}"
        return None


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"

    def validate(self, data):
        if data.get('available_beds', 0) > data.get('total_beds', 0):
            raise serializers.ValidationError("Available beds cannot exceed total beds.")
        return data


class MobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileNumber
        fields = ['id', 'mobile_number', 'is_primary']

class PatientSerializer(ModelSerializer):
    face_image_url = serializers.SerializerMethodField()
    insurance_document_url = serializers.SerializerMethodField()
    medical_histories = MedicalHistorySerializer(many=True, read_only=True)  # Fixed
    mobile_numbers = MobileNumberSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'gender', 'address',
            'insurance_document', 'face_image', 'age', 'blood_group',
            'face_image_url', 'insurance_document_url', 'medical_histories', 'mobile_numbers'
        ]

    class Meta:
        model = Patient
        fields = "__all__"

    def get_user(self, obj):
        return {
            "username",
            "email",
            "first_name",
            "last_name",
            "gender",
            "address",
            "face_image_url",
            "insurance_document_url",
            "medical_histories",
        }

    def get_face_image_url(self, obj):
        if obj.face_image and hasattr(obj.face_image, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.face_image.url)
            # Fallback for development (optional)
            return f"https://healthhelp-backend.onrender.com/{obj.face_image.url}"
        return None

    def get_insurance_document_url(self, obj):
        if obj.insurance_document and hasattr(obj.insurance_document, 'url'):
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.insurance_document.url)
            # Fallback for development (optional)
            return f"https://healthhelp-backend.onrender.com/{obj.insurance_document.url}"
        return None


class DriverSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"


class PoliceSerializer(ModelSerializer):
    badge_document_url = serializers.SerializerMethodField()

    class Meta:
        model = Police
        fields = [
            'username', 'email', 'first_name', 'last_name', 'gender',
            'badge_number', 'station_name', 'rank', 'latitude', 'longitude',
            'badge_document', 'badge_document_url', 'police_active'
        ]
        extra_kwargs = {
            'latitude': {'required': False},
            'longitude': {'required': False},
        }

    def get_badge_document_url(self, obj):
        request = self.context.get('request')
        if obj.badge_document and hasattr(obj.badge_document, 'url'):
            return request.build_absolute_uri(obj.badge_document.url)
        return None


class EmergencyRequestSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    class Meta:
        model = EmergencyRequest
        fields = [
            "id",
            "patient",
            "start_location_latitude",
            "start_location_longitude",
            "start_location_name",
            "end_location_latitude",
            "end_location_longitude",
            "end_location_name",
            "emergency_type",
            "description",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "hospital" 
        ]


class PatientTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientTreatment
        fields = '__all__'
        read_only_fields = ['hospital']
