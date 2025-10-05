from django.db import models

from RECRUITER.models import RecruiterRegister
from USER.models import JobSeeker


class ChatRoom(models.Model):
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='jobseeker_rooms')
    recruiter = models.ForeignKey(RecruiterRegister, on_delete=models.CASCADE, related_name='recruiter_rooms')
    room_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.room_name


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=True)
    # sender can be either JobSeeker or Recruiter
    job_seeker_sender = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, null=True, blank=True)
    recruiter_sender = models.ForeignKey(RecruiterRegister, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.job_seeker_sender:
            return f"{self.job_seeker_sender.full_name}: {self.message[:20]}"
        elif self.recruiter_sender:
            return f"{self.recruiter_sender.company_name}: {self.message[:20]}"
        else:
            return f"Message {self.id}"
