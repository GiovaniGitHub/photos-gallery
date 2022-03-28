from typing import List

from exceptions import AlbumCreateException, AlbumNotFound

from project.repositories.models import Album


def create_album(owner_id: str, album_title: str):
    try:
        album = Album(title=album_title, owner_id=owner_id)
        album.save()
    except Exception as e:
        raise AlbumCreateException(message="Create Album Failured", payload=e)

def get_albums_by_owner(owner_id: str) -> List[Album]:
    albums = Album.query.filter(Album.owner_id==owner_id).all()
    if not albums:
        raise AlbumNotFound(message="No Album Found")
    return albums

def get_photos_by_album_and_owner(album_id: str, owner_id: str):
    album = Album.get_album_by_id_and_owner(album_id=album_id, owner_id=owner_id)
    if not album:
        raise AlbumNotFound(message="No Album Found")

    return album.photos

def add_permission_to_user(album_id: str, user_email: str, owner_id: str):
    album = Album.get_album_by_id_and_owner(id=album_id, owner_id=owner_id)
    if not album:
        raise AlbumNotFound(message="No Album Found")
    print(album.friends)
    return album.add_friend(user_email)
    