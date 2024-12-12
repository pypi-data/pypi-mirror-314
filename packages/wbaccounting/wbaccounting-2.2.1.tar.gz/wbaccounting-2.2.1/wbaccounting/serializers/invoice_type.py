from wbaccounting.models import InvoiceType
from wbcore import serializers


class InvoiceTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceType
        fields = ("id", "name", "processor")


class InvoiceTypeRepresentationSerializer(serializers.RepresentationSerializer):
    _detail = serializers.HyperlinkField(reverse_name="wbaccounting:invoicetype-detail")

    class Meta:
        model = InvoiceType
        fields = ("id", "name", "_detail")
