from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField

REQUEST_SIGN_IN = "SIGN_IN"
REQUEST_ORDINARY = "ORDINARY"
request_types = ((REQUEST_SIGN_IN, REQUEST_SIGN_IN), (REQUEST_ORDINARY, REQUEST_ORDINARY))


class UserRequest(models.Model):
	time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = JSONField(default=dict)
	request_type = models.CharField(max_length=20, choices=request_types, default=REQUEST_SIGN_IN)

	def __str__(self):
		return f"{self.user} | {self.time}"
