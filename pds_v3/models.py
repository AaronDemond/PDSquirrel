from django.db import models
import random
import subprocess
import wave
import os
from django.contrib.auth.models import User

class Address(models.Model):
    street_address = models.CharField(max_length=255, blank=True, null=True)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True)
    po_box = models.CharField(max_length=10, blank=True, null=True)
    municipality = models.CharField(max_length = 255, blank=True, null=True)
    province = models.CharField(max_length=10, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.street_address

#default law societies
class LawSociety(models.Model):
    name = models.CharField(max_length=60)
    eligibility = models.TextField()
    overview = models.TextField()
    website = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

from pds_v3.managers import AppUserManager
#every user must be an app user


class Presenter(models.Model):
    user = models.OneToOneField(User, related_name="presenter")
    date_approved = models.DateField()
    bio = models.TextField(null=True, blank=True)
    credentials = models.TextField(null=True, blank=True)
    phone = models.CharField(null=True,blank=True,max_length=100)
    image = models.FileField(upload_to='pds_v3/static/presenter_pics', blank=True, null=True)
    law_firm = models.CharField(null=True,blank=True, max_length=100)
    public_email = models.CharField(null=True,blank=True,max_length=200)
    url = models.CharField(null=True,blank=True,max_length=200)

    # Allows user to set their placeholder img. 0=female, 1=male.
    placeholder_type = models.IntegerField(blank=True, null=True)

    female_placeholder = '/static/presenter_pics/Female-Placeholder1.jpg'
    male_placeholder = '/static/presenter_pics/speaker-placeholder-male.png'

    def image_name(self):
        return os.path.basename(self.image.name)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def imagePlaceholderUrl(self):
        ''' Returns relative url of a placeholder img for presenters '''

        if random.randint(1,2) == 1:
            return '/static/presenter_pics/Female-Placeholder1.jpg'
        else:
            return '/static/presenter_pics/speaker-placeholder-male.png'








class AppUser(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    address = models.ForeignKey(Address, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    society = models.ManyToManyField(LawSociety,blank=True)
    terms = models.BooleanField(blank=True)
    img = models.ImageField(blank=True)
    is_presenter = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    remaining_pd = models.IntegerField(default=1)
    stripe_id = models.CharField(max_length = 100, blank=True, null=True)
    date_premium = models.DateTimeField(blank=True, null=True)
    has_card = models.BooleanField(default=False)

    increment_task_id = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def create(cls,first_name,last_name, email, password, terms, society):
        usr = User.objects.create(username=email, email=email, password=password,
                                  first_name=first_name, last_name=last_name,
                                  is_active = False)

        foo = LawSociety.objects.get(pk=society)
        user = AppUser(user=usr, terms=terms)
        user.save()
        user.society.add(foo)
        user.save()
        return user



    objects = AppUserManager()



    def save(self, *args, **kwargs):
        super(AppUser,self).save(*args, **kwargs)
    def __str__(self):
        return self.user.username


#ovverride societies
class LawSocietyOverride(models.Model):
    parent = models.ForeignKey(LawSociety, null=True)
    name = models.CharField(max_length=60)
    eligibility = models.TextField(default=False)
    description = models.TextField(blank=True)
    short_name = models.TextField(blank=True)
    web_address = models.TextField(blank=True)
    def __str__(self):
        return self.name


class PdSessionManager(models.Manager):
    def get_pd_by_presenter(self):
        return True
    def get_pd_list(self,query=False,subject=False,):
        if subject:
            subject_filtered = PdSession.objects.filter(subject=subject, approved=True)
            return subject_filtered
        if query:
            query_filtered = PdSession.objects.filter(description__contains=query, approved=True)
            return query_filtered


            #return intersect(subject_filtered,query_filtered)


class Subject(models.Model):
    name = models.CharField(max_length=60)
    image = models.FileField(upload_to='pds_v3/static/img/subject', blank=True, null=True)

    def image_name(self):
        return os.path.basename(self.image.name)

    def __str__(self):
        return self.name

class PdAudio(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    audio = models.FileField(upload_to='audio_files', blank=True, null=True)
    appuser = models.ForeignKey(AppUser, blank=True, null=True)
    hidden = models.BooleanField(default=False, blank=True)
    used = models.BooleanField(default=False, blank=True)


    def getMp3Location(self):
        #return self.audio.name
        return '%s.mp3' % self.audio.name

    def convertToMp3(self):
        call = 'lame %s %s.mp3' % (self.audio.name, self.audio.name)
        subprocess.call(call, shell=True)


    def insert(self, start_ms, pdaudio):
        '''
        Takes a start_ms int and PdAudio obj. Inserts the audio
        at the start time. Updates parent audio.
        '''

        #Opens self audio file, gets wav metadata
        w = wave.open(self.audio.name, 'r')
        framerate = w.getframerate()
        framerate_ms = framerate / 1000
        frames = w.getnframes()
        channels = w.getnchannels()
        sample_width = w.getsampwidth()
        start_frame = start_ms * framerate_ms

        #slices audio into two sections
        start_chunk = w.readframes(start_frame)
        end_chunk = w.readframes(frames-start_frame)

        #gets raw frames of new recorded audio
        new_audio = wave.open(pdaudio.audio.name, 'r')
        middle_chunk = new_audio.readframes(new_audio.getnframes())

        #concats three audio sections
        full_chunk = start_chunk + middle_chunk + end_chunk

        #build wave file
        w = wave.open(self.audio.name, 'w')
        w.setnchannels(channels)
        w.setsampwidth(sample_width)
        w.setframerate(framerate)
        w.writeframes(full_chunk)


    def trim(self, start_ms, end_ms):
        '''
        Takes start and end in ms (int). Removes the selected range
        and updates the audio
        '''

        #opens file for editing, pulls info from it
        w = wave.open(self.audio.name, 'r')
        framerate = w.getframerate()
        framerate_ms = framerate / 1000
        frames = w.getnframes()
        channels = w.getnchannels()
        sample_width = w.getsampwidth()
        start_frame = start_ms * framerate_ms
        end_frame = end_ms * framerate_ms

        #get start and end chunks
        start_chunk = w.readframes(start_frame)
        w.setpos(end_frame)
        end_chunk = w.readframes(frames - end_frame)

        #data is just a string of characters, so we combine them
        full_chunk = start_chunk + end_chunk

        #create new wav with identical metadeta as input
        #write the combined data to create the new audio

        #todo: naming, save back to parent
        w = wave.open(self.audio.name, 'w')
        w.setnchannels(channels)
        w.setsampwidth(sample_width)
        w.setframerate(framerate)
        w.writeframes(full_chunk)
        return

    def __str__(self):
        return self.name


class PdAttachment(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    attachment = models.FileField(upload_to='attachments', blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    mark_for_delete = models.BooleanField(default=False)

    def filename(self):
        return os.path.basename(self.attachment.name)



class PdSessionEdit(models.Model):
    description = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='audio_files', blank=True, null=True)
    name = models.CharField(max_length=60, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    presenter_approved = models.BooleanField(default=False)
    attachments = models.ManyToManyField(PdAttachment, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        get_latest_by = "date"





class PdSession(models.Model):
    name = models.CharField(max_length=60)
    approved = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    subject = models.ManyToManyField(Subject, blank=True)
    audio_file = models.FileField(upload_to='audio_files')
    pdaudio = models.ForeignKey(PdAudio, null=True, blank=False)
    upload_date = models.DateTimeField(auto_now_add=True, null=True)
    release_date = models.DateTimeField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    duration = models.TextField(null=True)
    suspended = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    lawsocietyoverrides = models.ManyToManyField(LawSocietyOverride, blank=True)
    presenters = models.ManyToManyField(Presenter, blank=True)
    edited = models.BooleanField(default=False)
    edits = models.ManyToManyField(PdSessionEdit, blank=True)
    last_edited = models.DateTimeField(blank=True, null=True)
    presenter_approved = models.BooleanField(default=False)
    suspend_request = models.BooleanField(default=False)
    suspend_reason = models.CharField(max_length = 255, null=True, blank=True)
    objects = PdSessionManager()
    total_sales = models.FloatField(default = 0)
    total_credits = models.IntegerField(default = 0)
    locked = models.BooleanField(default = False)
    attachments = models.ManyToManyField(PdAttachment, blank=True)
    total_takes = models.IntegerField(default=0)


    def __str__(self):
        return self.name

    def getAudioLocation(self):
        if self.pdaudio:
            return self.pdaudio.getMp3Location()
        else:
            return self.audio_file

    class Meta:
        verbose_name = "PD Session"
        verbose_name_plural = "PD Sessions"

    def save(self, *args, **kwargs):
        super(PdSession, self).save(*args, **kwargs)



class Comment(models.Model):
    message = models.TextField(null=True, blank=True)
    user = models.ForeignKey(AppUser, blank=False, null=True)
    pd = models.ForeignKey(PdSession, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    parent = models.ForeignKey('Comment', blank=True, null=True)
    is_removed = models.BooleanField(default=False)

    def get_children(self):
        return Comment.objects.filter(parent_id = self.id)

    def __str__(self):
        name = self.user.user.username
        msg = self.message
        if len(msg) > 10:
            return "%s: %s..." % (name, msg[:20])
        else:
            return "%s: %s" % (name, msg)




class Completed(models.Model):
    date = models.DateField(auto_now_add=True)
    proof = models.TextField(blank=True)



from datetime import datetime
class Purchase(models.Model):
    user = models.ForeignKey(AppUser)
    pdsession = models.ForeignKey(PdSession)
    date = models.DateTimeField(default=datetime.now())
    price = models.FloatField()
    method = models.TextField()
    completed = models.BooleanField(default=False)
    credit_used = models.BooleanField(default=False)
    success = models.BooleanField(default=True)
    def __str__(self):
        name = self.user.user.username
        pd = self.pdsession.name
        return  "%s purchased %s" % (name, pd)

    def save(self, *args, **kwargs):

        if self.credit_used:
            self.pdsession.total_credits += 1
        else:
            self.pdsession.total_sales += float(self.price)

        self.pdsession.total_takes += 1
        self.pdsession.save()

        super(Purchase, self).save(*args, **kwargs)



class report(models.Model):
    user = models.ManyToManyField(AppUser)
    PdSession = models.ManyToManyField(PdSession)
    purchase = models.ManyToManyField(Purchase)


class Notice(models.Model):
    title = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments', null=True, blank=True)
    password = models.CharField(max_length = 100, null=True, blank=True)
    member_recipients = models.ManyToManyField(AppUser, blank=True)
    presenter_recipients = models.ManyToManyField(Presenter, blank=True)
    is_read = models.BooleanField(default=False)


class MembershipPaymentRecord(models.Model):
    user = models.ForeignKey(AppUser, blank=True)
    ammount = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=200, blank=True, null=True)
    success = models.BooleanField(blank=True)
    monthly_credits = models.IntegerField(blank=True, null=True)

class MembershipCancellationRecord(models.Model):
    user = models.ForeignKey(AppUser, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
