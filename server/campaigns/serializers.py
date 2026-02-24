from rest_framework import serializers
from .models import Campaign, CampaignSubmission


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = "__all__"
        read_only_fields = ["company", "status"]

# Creator submits content
class CampaignSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSubmission
        fields = ["campaign", "content_url"]

    def validate_campaign(self, campaign):
        # 1️⃣ Campaign must be LIVE
        if campaign.status != Campaign.Status.LIVE:
            raise serializers.ValidationError(
                "Submissions are allowed only for LIVE campaigns."
            )

        user = self.context["request"].user

        # 2️⃣ Check existing submission
        existing_submission = CampaignSubmission.objects.filter(
            campaign=campaign,
            creator=user
        ).first()

        if existing_submission:
            # ❌ Block resubmission unless NEED_IMPROVEMENT
            if existing_submission.status != CampaignSubmission.Status.NEED_IMPROVEMENT:
                raise serializers.ValidationError(
                    f"You have already submitted content for this campaign. "
                    f"Current status: {existing_submission.status}"
                )

        return campaign

    def create(self, validated_data):
        user = self.context["request"].user
        campaign = validated_data["campaign"]

        # 3️⃣ If NEED_IMPROVEMENT → UPDATE existing submission
        existing_submission = CampaignSubmission.objects.filter(
            campaign=campaign,
            creator=user,
            status=CampaignSubmission.Status.NEED_IMPROVEMENT
        ).first()

        if existing_submission:
            existing_submission.content_url = validated_data["content_url"]
            existing_submission.status = CampaignSubmission.Status.SUBMITTED
            existing_submission.feedback = ""
            existing_submission.save()
            return existing_submission

        # 4️⃣ First-time submission
        validated_data["creator"] = user
        return super().create(validated_data)
    

# Creator sees content status
class CreatorSubmissionStatusSerializer(serializers.ModelSerializer):
    campaign_title = serializers.CharField(source="campaign.title")
    company = serializers.SerializerMethodField()

    class Meta:
        model = CampaignSubmission
        fields = [
            "id",
            "campaign_title",
            "company",
            "content_url",
            "status",
            "feedback",
            "created_at",
        ]

    def get_company(self, obj):
        user = obj.campaign.company
        return getattr(user, "email", None) or getattr(user, "full_name", None)


# Creator reviews submission
class CompanySubmissionReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignSubmission
        fields = ["status", "feedback"]