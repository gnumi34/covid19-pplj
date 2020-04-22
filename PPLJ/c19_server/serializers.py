from rest_framework import serializers
from django.contrib.auth.models import User
from c19_server.models import Form, UserID, UserPhone


class FormSerializer(serializers.ModelSerializer):
    kategori = serializers.ReadOnlyField()

    class Meta:
        model = Form
        fields = ['id', 'gejala_demam', 'usia', 'kontak',
                  'aktivitas', 'gejala_lain', 'kategori']


class UserIDSerializer(serializers.ModelSerializer):
    forms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def validate_nik(self, value):
        """
        Memastikan NIK memiliki panjang 16 digit
        """
        if len(value) != 16:
            raise serializers.ValidationError("Panjang NIK tidak sama 16 digit")
        return value

    class Meta:
        model = UserID
        fields = ['id', 'nama', 'nik', 'alamat', 'tanggal_lahir', 'forms']


class UserPhoneSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    userid = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def validate_no_HP(self, value):
        """
        Memastikan No. HP memiliki panjang antara 10-12 digit
        """
        if len(value) > 12 & len(value) < 10:
            raise serializers.ValidationError("Panjang No. HP salah (antara 10-12 digit)")
        return value

    class Meta:
        model = UserPhone
        fields = ['id', 'owner', 'no_HP', 'userid']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
