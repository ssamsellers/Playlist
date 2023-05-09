"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models
class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)

    def __repr__(self):
        return "@" + self.username

class Song(Base):
    __tablename__ = "songs"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.username"), nullable=False)
    title = Column("title", TEXT, nullable=False)
    artist = Column("artist", TEXT, nullable=False)
    playlist_id = Column("playlist_id", ForeignKey("playlists.title"), nullable=False)


    def __repr__(self):
        return self.title + " by " + self.artist


class Playlist(Base):
    __tablename__ = "playlists"

    # Columns
    title = Column("title", TEXT, primary_key=True)
    num_songs = Column("num_songs", INTEGER, nullable=False)

class PlaylistSongs(Base):
    __tablename__ = "playlistsongs"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    playlist_id = Column("playlist_id", ForeignKey("playlists.title"), nullable=False)
    song_id = Column("song_id", ForeignKey("songs.id"), nullable=False)

class PlaylistSuggestions(Base):
    __tablename__ = "playlistsuggestions"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    user_id = Column("user_id", ForeignKey("users.username"), nullable=False)
    title = Column("title", TEXT, nullable=False)
    description = Column("description", TEXT, nullable=False)
    

