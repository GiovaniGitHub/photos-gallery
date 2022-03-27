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