Glossary
========

======
Models
======

.. py:class:: MediaCategory

    A user created collection of :py:class:`Media`.

    .. py:attribute:: name

        **Required.** A short name.

        Maximum 64 characters.

        :type: :py:class:`str`

    .. py:attribute:: cover

        A cover image.

        :type: :py:class:`~django.core.files.File` | :py:obj:`None`
        :value: ``None``

.. py:class:: Media

    A user created published work.

    .. py:attribute:: title

        **Required**. A short title.

        Maximum 64 characters. Must be unique.

        :type: :py:class:`str`

    .. py:attribute:: source

        **Required**. A video or an image.

        :type: :py:class:`~django.core.files.File`

    .. py:attribute:: thumb

        A thumbnail image.

        Automatically generated on save if the media is a video.

        :type: :py:class:`~django.core.files.File` | :py:obj:`None`
        :value: ``None``

    .. py:attribute:: subtitle

        A medium-length subtitle.

        Maximum 128 characters.

        :type: :py:class:`str` | :py:obj:`None`
        :value: ``None``

    .. py:attribute:: desc

        A lengthy description.

        Maximum 2048 characters.

        :type: :py:class:`str` | :py:obj:`None`
        :value: ``None``

    .. py:attribute:: slug

        A slug generated from a title.

        :type: :py:class:`str` | :py:obj:`None`
        :value: ``None``

    .. py:attribute:: is_hidden

        Whether or not the media is hidden.

        :type: :py:class:`bool`
        :value: ``False``

    .. py:attribute:: is_image

        Whether or not the media is an image.

        Set on :py:meth:`~Media.save()`

        :type: :py:class:`bool` | :py:obj:`None`
        :value: ``None``

    .. py:attribute:: categories

        Categories the media is a member of.

        :type: :py:class:`~django.db.models.QuerySet`
        :value: :py:obj:`~django.db.models.QuerySet`

    .. py:attribute:: date_created

        The date the user created the media.

        :type: :py:class:`~datetime.date` | :py:obj:`None`
        :value: ``None``

    .. py:attribute:: datetime_published

        The date and time the user created the media.

        Cannot be modified after creation time.

        :type: :py:class:`~datetime.datetime` | :py:obj:`None`
        :value: ``None``

    .. py:method:: set_thumbnail([file=None]) -> None

        Sets the media's thumbnail to the file.

        If the file is ``None``, instead sets the media's thumbnail to the return value of :py:meth:`~Media.generate_thumbnail`.

        :param file: The new thumbnail.
        :type file: :py:class:`~django.core.files.File`
        :return: Nothing.
        :rtype: :py:obj:`None`
        :raises AssertionError: If the media is an image.

    .. py:method:: generate_thumbnail([loc=0]) -> File

        Generates a thumbnail at frame ``loc``.

        :param loc: The frame of the media to generate. Default is 0.
        :type loc: :py:class:`int`
        :return: A new thumbnail file.
        :rtype: :py:class:`~django.core.files.File`
        :raises AssertionError: If the media is an image.
        :raises ValueError: If frame ``loc`` was not captured.
