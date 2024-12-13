from django.dispatch import receiver
from wbcore.contrib.agenda.signals import complete_post_delete, complete_post_save
from wbcrm.typings import Activity as ActivityDTO
from wbcrm.typings import ParticipantStatus as ParticipantStatusDTO

from .controller import ActivityController


@receiver(complete_post_save, sender="wbcrm.Activity")
def pre_save_activity(sender, activity_dto: ActivityDTO, pre_save_activity_dto: ActivityDTO = None, **kwargs):
    ActivityController().handle_outbound(activity_dto, old_activity_dto=pre_save_activity_dto)


@receiver(complete_post_delete, sender="wbcrm.Activity")
def pre_delete_activity(sender, activity_dto: ActivityDTO, pre_delete_activity_dto: ActivityDTO, **kwargs):
    ActivityController().handle_outbound(activity_dto, old_activity_dto=pre_delete_activity_dto, is_deleted=True)


@receiver(complete_post_save, sender="wbcrm.ActivityParticipant")
def pre_save_activity_participant(
    sender, participant_dto: ParticipantStatusDTO, pre_save_participant_dto: ParticipantStatusDTO = None, **kwargs
):
    ActivityController().handle_outbound_participant(participant_dto, old_participant_dto=pre_save_participant_dto)


@receiver(complete_post_delete, sender="wbcrm.ActivityParticipant")
def pre_delete_activity_participant(sender, participant_dto: ParticipantStatusDTO, **kwargs):
    ActivityController().handle_outbound_participant(participant_dto, is_deleted=True)
