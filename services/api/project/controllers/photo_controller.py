
import uuid
from posixpath import basename

from sqlalchemy.orm.exc import NoResultFound

from exceptions import AlbumNotFound, PhotoNotFound, UnauthorizedPhotoUpdate
from project.repositories.models import Album, Photo
from project.repositories.s3_repository import upload_file


def create_photo(user_id: str, album_id: str, photo_data: dict):

    album = Album.get_album_by_id(album_id)
    if not album:
        raise AlbumNotFound(message="No Album Found")

    if not album.check_user_has_permission(user_id):
        raise UnauthorizedPhotoUpdate(message="You dont have permission to upload.")
    try:
        id = str(uuid.uuid4())
        output = upload_file(file=photo_data["photo_file"], album_id=album_id, user_id=user_id,
                             file_name=id)

        photo = Photo(id=id, name=basename(output), description=photo_data["description"],
                      url=output, user=user_id)

        photo.save()
        album.add_photo(photo)
        album.save()
    except Exception as e:
        return UnauthorizedPhotoUpdate(message="Problem to Upload Photo", payload=e)
    return None, 201

def like_picture(album_id: str, photo_id: str) -> bool:
    album = Album.get_album_by_id(id=album_id)

    if not album:
        raise AlbumNotFound(message="Album Not Found")

    try:
        photo = album.photos.filter(id=photo_id)
        photo.get().likes += 1
        photo.save()
        return True
    except NoResultFound:
        raise PhotoNotFound("Photo not Found")
