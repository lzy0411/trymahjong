from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.utils import timezone
from mahjong.forms import LoginForm, RegisterForm, ProfileForm
from mahjong.models import Game, Tile, Room, Profile
import time
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
import random
from json import dumps


# Create your views here.
def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'mahjong/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.

    form = RegisterForm(request.POST)
    context['form'] = join_room

    # Validates the form.
    if not form.is_valid():
        return render(request, 'mahjong/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)

    return redirect(reverse('login'))


def login_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'mahjong/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'mahjong/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))


@login_required
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def lobby(request):
    return render(request, 'mahjong/lobby.html')


@login_required
def create_room(request):
    game = Game(game_state=0)
    game.save()
    new_room = Room(game_id=game.pk)
    new_room.room_time = timezone.now()

    new_room.user1 = request.user
    new_room.room_state = 0
    new_room.num_of_players = 1
    new_room.save()

    context = {"room": new_room}
    context["room_name"] = new_room.id
    return redirect(reverse('joinroom', args=[new_room.id]))


@login_required
def join_room(request, room_name):
    if room_name == "/":
        return redirect(reverse('home'))
    try:
        room = Room.objects.get(id=room_name)
        nums = room.num_of_players
    except:
        context = {"error": "Invalid room number. Try another room"}
        return redirect(reverse('home'))


    # when the user already in the room, redirect to the room
    if room.user1 == request.user:
        context = {"error": "You are already in the room. Please start the game"}
        context["room_name"] = room.id
        context['game_id'] = room.game.id
        context["user1"] = room.user1.id
        context["user1_username"] = room.user1.username        
        if (room.user2):
            context["user2"] = room.user2.id
            context["user2_username"] = room.user2.username
        if (room.user3):
            context["user3"] = room.user3.id
            context["user3_username"] = room.user3.username
        if (room.user4):
            context["user4"] = room.user4.id
            context["user4_username"] = room.user4.username
        context["current_user"] = request.user.id
        context["current_username"] = request.user.username
        context["current_user_num"] = "user1_status"
        return render(request, 'mahjong/gamepage.html', {"data": context})

    if room.user2 == request.user or room.user3 == request.user or room.user4 == request.user:
        context = {"error": "You are already in the room. Please wait the host start the game"}
        context["room_name"] = room.id
        context['game_id'] = room.game.id
        context["user1"] = room.user1.id
        context["user1_username"] = room.user1.username

        context["current_user"] = request.user.id
        context['current_username'] = request.user.username        
        
        if (room.user2 == request.user):
            context["current_user_num"] = "user2_status"
        if (room.user3 == request.user):
            context["current_user_num"] = "user3_status"
        if (room.user4 == request.user):
            context["current_user_num"] = "user4_status"

        if (room.user2):
            context["user2"] = room.user2.id
            context["user2_username"] = room.user2.username            
        if (room.user3):
            context["user3"] = room.user3.id
            context["user3_username"] = room.user3.username
        if (room.user4):
            context["user4"] = room.user4.id
            context["user4_username"] = room.user4.username
        return render(request, 'mahjong/gamepage.html', {"data": context})

    # when the room is full, redirect to the lobby
    if nums == 4:
        context = {"error": "Room is Full. Try another room"}
        return render(request, 'mahjong/lobby.html', context)

    room.num_of_players += 1

    context = {}
    context["room_name"] = room.id
    context["user1"] = room.user1.id
    context["user1_username"] = room.user1.username
    context['game_id'] = room.game.id
    context["current_user"] = request.user.id
    context["current_user_num"] = "user1_status"
    context['current_username'] = request.user.username
    context['notification'] = "Can Only Start The Game When The Room Is Full"

    if nums == 1:
        room.user2 = request.user
        context["user2"] = room.user2.id
        context["user2_username"] = room.user2.username
        context["current_user_num"] = "user2_status"
    if nums == 2:
        room.user3 = request.user
        context["user2"] = room.user2.id
        context["user2_username"] = room.user2.username
        context["user3"] = room.user3.id
        context["user3_username"] = room.user3.username
        context["current_user_num"] = "user3_status"
    if nums == 3:
        room.user4 = request.user
        context["user2"] = room.user2.id
        context["user2_username"] = room.user2.username
        context["user3"] = room.user3.id
        context["user3_username"] = room.user3.username
        context["user4"] = room.user4.id
        context["user4_username"] = room.user4.username
        context["current_user_num"] = "user4_status"
        context['notification'] = "Can Start the Game Now!"
    room.save()
    print("&&&&&&&&&&& INSIDE JOIN ROOM &&&&&&&&&&&&&&&")
    print(context)
    
    return render(request, 'mahjong/gamepage.html', {"data": context})


def create_tile(numindex):
    tile_type = ""
    tile_num = ""
    index = -1
    if numindex <= 35:
        tile_type = "BAMBOO"
        tile_num = numindex % 9 + 1
        index = tile_num
        # 1-9
    elif numindex <= 71:
        tile_type = "DOTS"
        tile_num = (numindex - 35) % 9 + 1
        index = 10 + tile_num
        # 11-19
    elif numindex <= 107:
        tile_type = "CHARACTERS"
        tile_num = (numindex - 71) % 9 + 1
        index = 20 + tile_num
        # 21-29
    elif numindex <= 123:
        tile_type = "WIND"
        times = (numindex - 107) // 4
        print(numindex)
        print(time)
        if times == 0:
            tile_num = 'EAST'
            index = 40
        elif times == 1:
            tile_num = 'SOUTH'
            index = 50
        elif times == 2:
            tile_num = 'WEST'
            index = 60
        else:
            tile_num = 'NORTH'
            index = 70
    elif numindex <= 127:
        tile_type = "DRAGON"
        tile_num = "ZHONG"
        index = 80
    elif numindex <= 131:
        tile_type = "DRAGON"
        tile_num = "FA"
        index = 90
    else:
        tile_type = "DRAGON"
        tile_num = "WHITE"
        index = 100
    # print(index)
    # print(tile_type)
    # print(tile_num)


    tile = Tile(tile_index=index, tile_type=tile_type, tile_num=tile_num, tile_status=-1)
    tile.save()
    return tile


@login_required
def initialize_game(request):
    print("************")
    if not request.POST['game_id']:
        return _my_json_error_response("No Game ID",status=404)
    if not (request.POST['id_user1_status'] and request.POST['id_user2_status'] and request.POST['id_user3_status'] and request.POST['id_user4_status']):
        return redirect('joinroom',room_name = request.POST['room_id'])
    if request.POST['id_user1_status'] == "/" or request.POST['id_user2_status'] =="/" or request.POST['id_user3_status'] == "/" or request.POST['id_user4_status'] =="/":
        return redirect('joinroom',room_name =request.POST['room_id'])

    game = Game.objects.get(id=request.POST["game_id"])
    print("gamestate")
    print(game.game_state)
    if game.game_state == "1":
        return redirect('refresh_game', game_id=game.pk, message="Game starts!")
    if game.game_state == "2":
        return _my_json_error_response("Game has ended!",status=404)


    print(request.POST['id_user1_status'])
    print(request.POST['id_user2_status'])
    print(request.POST['id_user3_status'])
    print(request.POST['id_user4_status'])


    user1 = User.objects.get(id = request.POST['id_user1_status'])
    user2 = User.objects.get(id = request.POST['id_user2_status'])
    user3 = User.objects.get(id = request.POST['id_user3_status'])
    user4 = User.objects.get(id = request.POST['id_user4_status'])
    game.user1 = user1
    game.user2 = user2
    game.user3 = user3
    game.user4 = user4
    game.game_time = timezone.now()
    game.game_time = timezone.now()
    game.game_state = 1
    game.current_user = user1
    total = 136
    array_tiles = list(range(1, total + 1))
    print("initialize random number")
    print(array_tiles)
    twist_curr = 0
    while twist_curr < 40:
        n = random.randint(0, total - 1)
        m = random.randint(0, total - 1)
        if n + 3 < total and m + 3 < total and abs(m-n)>3:
            tmp1 = array_tiles[n]
            tmp2 = array_tiles[n+1]
            tmp3 = array_tiles[n+2]
            array_tiles[n] = array_tiles[m]
            array_tiles[n+1] = array_tiles[m+1]
            array_tiles[n+2] = array_tiles[m+2]
            array_tiles[m] = tmp1
            array_tiles[m+1] = tmp2
            array_tiles[m+2] = tmp3
            print(array_tiles)

        else:
            tmp = array_tiles[n]

            array_tiles[n] = array_tiles[m]
            array_tiles[m] = tmp
        twist_curr += 1

    tiles = []
    print(array_tiles)


    for i in range(0, len(array_tiles)):
        index = array_tiles[i]
        tile = create_tile(index)

        tiles.append(tile)

    for i in range(0, 52, +4):
        tile1 = tiles[i]

        game.list_in_user1.add(tile1)

        tile2 = tiles[i + 1]
        game.list_in_user2.add(tile2)

        tile3 = tiles[i+2]
        game.list_in_user3.add(tile3)

        tile4 = tiles[i+3]
        game.list_in_user4.add(tile4)

    game.list_in_user1.add(tiles[52])
    count = 0
    for i in range(53, 136):
        game.list_to_be_assigned.add(array_tiles[i])
        count += 1

    game.num_of_tiles_tba = count
    game.save()
    print(game)
    print(game.list_in_user1)
    print(game.list_in_user2)
    print(game.list_to_be_assigned)
    print(game.list_discarded)
    print(game.list_in_user1.all)
    return redirect('refresh_game', game_id=game.pk, message="Game starts!")


def automaticSort(list):
    newList = sorted(list, key=lambda tile: tile.tile_index)
    return newList


def verify_win(tiles):
    if len(tiles) % 3 != 2:
        print("not correct number of tiles")
        return False
    nums = []
    for tile in tiles:
        nums.append(tile.tile_index)
    nums = sorted(nums)
    print("###################")
    print(nums)
    doubles = []
    set_of_nums = set(nums)
    for num in set_of_nums:
        if nums.count(num) >= 2:
            doubles.append(num)
    if len(doubles) == 0:
        return False
    # seven pairs:
    is_seven_pairs = True
    for num in set_of_nums:
        if not (nums.count(num) == 2 or nums.count(num) == 4):
            is_seven_pairs = False
            break

    if is_seven_pairs:
        return True


    res = []
    for pair_num in doubles:
        nums_copy = nums.copy()
        nums_copy.remove(pair_num)
        nums_copy.remove(pair_num)

        res.append((pair_num, pair_num))
        for first in range(int(len(nums_copy) / 3)):
            first = nums_copy[0]
            if nums_copy.count(first) == 3:
                res.append((first, first, first))
                nums_copy = nums_copy[3:]
            elif first + 1 in nums_copy and first + 2 in nums_copy:
                res.append((first, first + 1, first + 2))
                nums_copy.remove(first)
                nums_copy.remove(first + 1)
                nums_copy.remove(first + 2)
            else:
                nums_copy = nums.copy()
                res = []
                break
        print(res)
        if len(res) == 5:
            return True

    return False


def canTriple(list, index):
    print("inside the cantriple:")
    print("index")
    print(index)
    count = 0
    print()
    for tile in list:
        print(tile.tile_index)
        if tile.tile_index == index:
            count += 1
    return count ==2 or count ==3


def discard_tile_grab_with_id(request,discard_tile_id,game_id):
    print("!@#$%^&*(*&^%$#@#$%^&*&^%$#@#$%^&^%$#@#$%^&")
    print("~~~~~~~ game id ~~~~~~~~~~~`")
    print(game_id)

    if not discard_tile_id or not game_id:
        return
    game = Game.objects.get(id=game_id)
    print(game)

    discarded_tile = Tile.objects.get(id = discard_tile_id)
    if game.user1 == request.user:
        game.list_in_user1.remove(discarded_tile)
    elif game.user2 == request.user:
        game.list_in_user2.remove(discarded_tile)

    elif game.user3 == request.user:
        game.list_in_user3.remove(discarded_tile)

    elif game.user4 == request.user:
        game.list_in_user4.remove(discarded_tile)
    game.list_discarded.add(discarded_tile)
    game.save()
    return redirect('refresh_game', game_id = game.pk, message="A tile is discarded with id")

def discard_tile_grab(request):
    discard_tile_id = request.POST['discard_tile_id']
    game_id = request.POST['game_id']
    print("~~~~~~~ game id ~~~~~~~~~~~`")
    print(game_id)

    if not discard_tile_id or not game_id:
        return
    game = Game.objects.get(id=game_id)
    print(game)
    curr_user = None
    new_list_toassigned  = game.list_to_be_assigned.all()
    newTile = new_list_toassigned[0]
    game.list_to_be_assigned.remove(newTile)
    print("newTile")
    print(newTile.tile_index)
    discarded_tile = Tile.objects.get(id = discard_tile_id)
    if game.user1 == request.user:
        game.list_in_user1.remove(discarded_tile)
        curr_user = game.user2
        game.list_in_user2.add(newTile)
    elif game.user2 == request.user:
        game.list_in_user2.remove(discarded_tile)
        curr_user = game.user3
        game.list_in_user3.add(newTile)
    elif game.user3 == request.user:
        game.list_in_user3.remove(discarded_tile)
        game.list_in_user4.add(newTile)
        curr_user = game.user4
    elif game.user4 == request.user:
        game.list_in_user4.remove(discarded_tile)
        curr_user = game.user1
        game.list_in_user1.add(newTile)

    game.new_added = newTile
    game.num_of_tiles_tba = game.num_of_tiles_tba - 1
    game.last_tile = discarded_tile
    game.current_user = curr_user
    game.list_discarded.add(discarded_tile)
    game.save()
    return redirect('refresh_game', game_id = game.pk, message="A tile is discarded")


def refresh_game_test(request):

    return redirect('refresh_game', game_id=request.POST['game_id'], message="Game starts!")
    #return redirect(reverse('refresh_game', args=[game_id, "Game starts!"]))


def refresh_game(request, game_id, message):
    print("~~~~~~~~~~~~~~~~~~` inside the refresh game ~~~~~~~~~~~~~~~~~~~~")
    print("request user")
    print(request.user)

    game = Game.objects.get(id=game_id)
    if game.game_state == 0:
        return _my_json_error_response("Game has not started!", status=404)
    if game.game_state == 2:
            return _my_json_error_response("Game has ended!", status=404)


    list_in_user = None
    if game.current_user == request.user:
        can_discard = True
        if message == "" or message == "Game starts!":
            message = "Choose a tile to discard"
    else:
        can_win = False
        can_discard = False
    if game.user1 == request.user:
        list_in_user = game.list_in_user1.all()

    if  game.user2 == request.user:
        list_in_user = game.list_in_user2.all()
    elif game.user3 == request.user:
        list_in_user = game.list_in_user3.all()
    elif game.user4 == request.user:
        list_in_user = game.list_in_user4.all()

    if len(list_in_user) == 14:
        message = "Choose a tile to discard!"

    list_of_triple_1 = game.list_of_triple_1.all()
    list_of_triple_2 = game.list_of_triple_2.all()
    list_of_triple_3 = game.list_of_triple_3.all()
    list_of_triple_4 = game.list_of_triple_4.all()
    # ## TODO automatic sort assignment
    # print(list_in_user)
    if list_in_user :
        tiles = [value for value in list_in_user]
    else:
        tiles = game.list_in_user1.all()
    list_in_user = automaticSort(tiles)
    print("length of list in user")
    print(len(list_in_user))

    if game.last_tile is not None and game.current_user == request.user:
        last_tile_index = game.last_tile.tile_index
        list_copy = list_in_user.copy()
        list_copy.remove(game.new_added)
        can_triple = canTriple(list_copy,last_tile_index)
        if can_triple:
            message = "If you choose to triple or eat, the newly added tile will be discarded!"
    else:
        can_triple = False
    if game.last_tile is None or game.current_user != request.user:
        can_eat = False
    else:
        can_eat = True
    can_win = verify_win(list_in_user)
    print("canTriple:" )
    print(can_triple)
    print("new Added")
    newAdded = None
    if game.new_added is not None:
        newAdded = game.new_added
        print(game.new_added.tile_index)

    context = {'user': request.user, 
                'canDiscard': can_discard, 
                'canTriple': can_triple, 
                'canWin': can_win,
                'message': message,
                'current_user': game.current_user, 
                'num_of_tiles_tba': game.num_of_tiles_tba,
                'last_tile': game.last_tile, 
                'list_in_user': list_in_user,
                'new_added':newAdded,
                'list_of_triple_1': list_of_triple_1,
                'list_of_triple_2': list_of_triple_2,
                'list_of_triple_3': list_of_triple_3,
                'list_of_triple_4': list_of_triple_4,
                'user1': game.user1, 
                'user2': game.user2, 
                'user3': game.user3, 
                'user4': game.user4, 
                'gameId': game.id,
               'canEat':can_eat,
                'userId': request.user.id,
                'username': request.user.username, }
    print("~~~~~~~~~~~~~~~~~~~~~~~~~  context in refresh game ~~~~~~~~~~~~~~~~~~~~~~~")
    print(context)
    return render(request, 'mahjong/game.html', context)


def triple_tile(request):
    game_id = request.POST['game_id']
    game = Game.objects.get(id=game_id)
    to_triple = game.last_tile
    print("~~~~~~~~~~~~ inside the triple tile ~~~~~~~~~~~~~~~")
    print(to_triple.tile_index)
    list = None
    if request.user == game.user1:
        list = game.list_in_user1.all()
    elif request.user == game.user2:
        list = game.list_in_user2.all()
    elif request.user == game.user3:
        list = game.list_in_user3.all()
    elif request.user == game.user4:
        list = game.list_in_user4.all()

    list = [tile for tile in list]
    newAdded = game.new_added
    list.remove(game.new_added)

    for i in list:
        print(i.tile_index)

    if not canTriple(list, to_triple.tile_index):
        print("can not triple")
        return redirect('refresh_game', game_id=request.POST['game_id'], message="Triple Failure")

    count = 0
    triples = []
    for tile in list:
        if tile.tile_index == to_triple.tile_index:
            triples.append(tile)
        if count == 3:
            break

    if request.user == game.user1:
        game.list_in_user1.add(to_triple)
        for i in triples:
            game.list_of_triple_1.add(i)
    elif request.user == game.user2:

        game.list_in_user2.add(to_triple)
        for i in triples:
             game.list_of_triple_2.add(i)
    elif request.user == game.user3:

        game.list_in_user3.add(to_triple)
        for i in triples:
            game.list_of_triple_3.add(i)
    elif request.user == game.user4:

        game.list_in_user4.add(to_triple)
        for i in triples:
            game.list_of_triple_4.add(i)
    game.list_discarded.remove(to_triple)
    game.last_tile = None
    game.current_user = request.user
    game.save()
    return redirect('discard_tile_grab_with_id',discard_tile_id = newAdded.id,game_id =game_id)

def win_game_redirect(request,game_id):
    print(game_id)

    game = Game.objects.get(id=game_id)
    print("winner")
    print(game.winner)
    win_list = None
    if game.winner == game.user1:
        win_list = game.list_in_user1.all()
    elif game.winner == game.user2:
        win_list = game.list_in_user2.all()
    elif game.winner == game.user3:
        win_list = game.list_in_user3.all()
    elif game.winner == game.user4:
        win_list = game.list_in_user4.all()
    if win_list is None:
        return redirect('refresh_game', game_id=request.POST['game_id'],message ="")
    win_list = automaticSort(win_list)
    return render(request, 'mahjong/winpage.html', {"win_list": win_list, "winner_id": game.winner.id, "winner_name": game.winner.username})

def win_game(request):
    print("win the game!!!!!!!!!!!!!")
    # method == "GET" is just for test


    if not request.POST['game_id']:
        return redirect('refresh_game', game_id=request.POST['game_id'],message ="Can Not Win")
    try:
        game = Game.objects.get(id=request.POST['game_id'])
    except:
        return redirect('refresh_game', game_id=request.POST['game_id'],message ="Can Not Win")

    # return error
    if not game:
        return
    win_list = None
    if request.user == game.user1:
        win_list = game.list_in_user1.all()
    elif request.user == game.user2:
        win_list = game.list_in_user2.all()
    elif request.user == game.user3:
        win_list = game.list_in_user3.all()
    elif request.user == game.user4:
        win_list = game.list_in_user4.all()
    win_list = automaticSort(win_list)

    if verify_win(win_list):
        print("here!!!!")
        game.winner = request.user
    else:
        if game.num_of_tiles_tba <= 0:
            context = {"win_list": None,
                       "winner_id": None,
                       "winner": "",
                       "gameId":game.id,
                       "message": "Winner",
                       "user1": game.user1,
                       "user2": game.user2,
                       "user3": game.user3,
                       "user4": game.user4,
                       "room": room,
                       "game": game}
            return render(request, 'mahjong/winpage.html', context)

        return redirect('refresh_game', "Game Continue!")

    game.game_state = 2
    game.save()

    context = {"win_list": win_list, 
                "winner_id": request.user.id, 
                "winner": request.user.username,
                "gameId":game.id,
                "message": "Winner",
                "user1": game.user1,
                "user2": game.user2,
                "user3": game.user3,
                "user4": game.user4,
                "room": room,
                "game": game}
    return render(request, 'mahjong/winpage.html', context)



def game_instruction(request):
    return render(request, 'mahjong/game_instruction.html')


def index(request):
    return render(request, 'mahjong/index.html')


def room(request, room_name):
    return render(request, 'mahjong/room.html', {
        'room_name': room_name,
        'user1': 1,
        "user2": 2,
        'user3': 3,
        'user4': 4,
    })

def _my_json_error_response(message, status=200):

    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

def eat_tile(request):
    print("~~~~~~~~~~!!!! INSIDE EAT TILE !!!! ~~~~~~~~~~~~~~~~")

    game = Game.objects.get(id = request.POST['game_id'])
    try:
        if (not request.POST['eat_tile_1_id'] )or (not request.POST['eat_tile_2_id'] ):
            return redirect('refresh_game', game_id=game.pk, message="Cannot eat! Choose a tile to discard")
    except:
        return redirect('refresh_game', game_id=game.pk, message="Cannot eat! Choose a tile to discard")

    tile1 = Tile.objects.get(id = request.POST['eat_tile_1_id'])
    tile2 = Tile.objects.get(id = request.POST['eat_tile_2_id'])

    if request.user!= game.current_user:
        return redirect('refresh_game', game_id=game.pk, message="Cannot eat! Choose a tile to discard!")

    if game.last_tile is None:
        return redirect('refresh_game', game_id=game.pk, message="Cannot eat! Choose a tile to discard!")

    list = []
    list.append(tile1)
    list.append(tile2)
    list.append(game.last_tile)
    print("last tile ")
    print(game.last_tile.tile_index)

    newList = sorted(list, key=lambda tile: tile.tile_index)
    prev = None
    for i in newList:
        print(i.tile_index)
        if prev is None:
            prev = i.tile_index
        else:
            print(i.tile_index-prev)
            if i.tile_index-prev != 1:
                return redirect('refresh_game', game_id=game.pk, message="Cannot eat! Choose a tile to discard!")
            prev = i.tile_index

    newAdded = game.new_added
    print("newly added")
    print(newAdded.tile_index)

    if request.user == game.user1:
        game.list_in_user1.remove(newAdded)
        game.list_in_user1.add(game.last_tile)
        game.list_of_triple_1.add(game.last_tile)
        game.list_of_triple_1.add(tile1)
        game.list_of_triple_1.add(tile2)
    if request.user == game.user2:
        game.list_in_user2.remove(newAdded)
        game.list_in_user2.add(game.last_tile)
        game.list_of_triple_2.add(game.last_tile)
        game.list_of_triple_2.add(tile1)
        game.list_of_triple_2.add(tile2)
    if request.user == game.user3:
        game.list_in_user3.remove(newAdded)
        game.list_in_user3.add(game.last_tile)
        game.list_of_triple_3.add(game.last_tile)
        game.list_of_triple_3.add(tile1)
        game.list_of_triple_3.add(tile2)
    if request.user == game.user4:
        game.list_in_user4.remove(newAdded)
        game.list_in_user4.add(game.last_tile)
        game.list_of_triple_4.add(game.last_tile)
        game.list_of_triple_4.add(tile1)
        game.list_of_triple_4.add(tile2)
    game.last_tile = None
    game.save()



    return redirect('refresh_game', game_id=game.pk, message="Eat Success and Choose a tile to discard!")



