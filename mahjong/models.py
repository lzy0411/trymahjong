from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tile(models.Model):
    tile_index = models.IntegerField()
    tile_type = models.CharField(max_length=50, blank=True)
    tile_num = models.CharField(max_length=50, blank=True)
    tile_pic = models.FileField(blank = False)
    tile_status = models.CharField(max_length=50, blank=True) # -1: to be assigned；



class Game(models.Model):
    game_time = models.DateTimeField( null=True,blank=True,default=None,)
    user1 = models.ForeignKey(User,  null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="game_user1")
    user2 = models.ForeignKey(User,  null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="game_user2")
    user3 = models.ForeignKey(User,  null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="game_user3")
    user4 = models.ForeignKey(User,  null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="game_user4")
    winner = models.ForeignKey(User, null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="winner")

    game_state =  models.CharField(null=True, blank=True, default=None, max_length=50) # START1 END2 not start 0
    num_of_tiles_tba = models.IntegerField( null=True,blank=True,default=None)
    current_user = models.ForeignKey(User,  null=True,blank=True,default=None, on_delete=models.PROTECT)
    list_to_be_assigned = models.ManyToManyField('Tile',related_name = 'unassigned')
    list_in_user1 = models.ManyToManyField('Tile', related_name = 'user1')
    list_in_user2 = models.ManyToManyField('Tile', related_name = 'user2')
    list_in_user3 = models.ManyToManyField('Tile', related_name = 'user3')
    list_in_user4 = models.ManyToManyField('Tile', related_name = 'user4')
    list_discarded = models.ManyToManyField('Tile', related_name = 'discarded')
    last_tile = models.ForeignKey(Tile, null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="lasttile")
    list_of_triple_1 =  models.ManyToManyField('Tile', related_name = 'triple1')
    list_of_triple_2 =  models.ManyToManyField('Tile', related_name = 'triple2')
    list_of_triple_3 =  models.ManyToManyField('Tile', related_name = 'triple3')
    list_of_triple_4 =  models.ManyToManyField('Tile', related_name = 'triple4')
    new_added = models.ForeignKey(Tile,  null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="new_added")



class Room(models.Model):
    game =  models.ForeignKey(Game, null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="room_game")
    room_time = models.DateTimeField()
    user1 = models.ForeignKey(User, default=None, on_delete=models.PROTECT, related_name="room_user1")
    user2 = models.ForeignKey(User, null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="room_user2")
    user3 = models.ForeignKey(User, null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="room_user3")
    user4 = models.ForeignKey(User, null=True,blank=True,default=None, on_delete=models.PROTECT, related_name="room_user4")
    room_state =  models.CharField(max_length=50, blank=True) # 0: just created 1: has been destroyed 2： start a game
    num_of_players  = models.IntegerField()

class Profile(models.Model):
    username = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User,default = None,on_delete=models.PROTECT)
    content_type = models.CharField(max_length=50, blank=True)
    profile_picture = models.FileField(blank = True)
    game_history = models.ManyToManyField('Game', related_name = 'past_game') #optional
