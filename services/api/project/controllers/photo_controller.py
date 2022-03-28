
from exceptions import AlbumNotFound, UnauthorizedPhotoUpdate
from project.repositories.models import Album


def create_photo(user_id: str, album_id: str, photo_data: dict):
    album = Album.get_album_by_id(album_id)
    
    if not album:
        raise AlbumNotFound(message="No Album Found")

    if not album.check_user_has_permission(user_id):
        raise UnauthorizedPhotoUpdate(message="You dont have permission to upload.")
