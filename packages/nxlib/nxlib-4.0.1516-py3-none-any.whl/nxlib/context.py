from nxlib import api
from nxlib.command import NxLibCommand
from nxlib.constants import *
from nxlib.item import NxLibItem


class NxLib:
    """
    This class offers a simple to use interface for interacting with a normal
    NxLib. It implements the context manager protocol and thus can be used in a
    ``with`` statement, which automatically initializes the NxLib and takes care
    of the exception handling.

    Args:
        path (str, optional): The path to the NxLib shared library.
            Defaults to None.
    """
    def __init__(self, path=None):
        self._path = path

    def __enter__(self):
        api.initialize(path=self._path)
        return api

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Explicitly finalize! We cannot rely on the finalize() call in the
        # destructor of the global nxlib instance, because it is not guaranteed
        # that the garbage collector invokes it directly after exiting the
        # with-statement and before re-initializing the API with e.g. another
        # with-statement.
        api.finalize()


class NxLibRemote:
    """
    This class offers a simple to use interface for interacting with a remote
    NxLib. It implements the context manager protocol and thus can be used
    in a ``with`` statement, which automatically loads the remote NxLib,
    connects to the given hostname (and port) when entering the scope and
    automatically disconnects when exiting the scope. It also takes care of the
    exception handling.

    Args:
        hostname (str): The hostname of the remote NxLib.
        port (int): The port number of the remote NxLib.

    """
    def __init__(self, hostname, port):
        self._hostname = hostname
        self._port = int(port)

    def __enter__(self):
        api.load_remote_lib()
        api.connect(self._hostname, self._port)
        return api

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Explicitly disconnect! We cannot rely on the disconnect() call in the
        # destructor of the global nxlib instance, because it is not guaranteed
        # that the garbage collector invokes it directly after exiting the
        # with-statement and before re-initializing the API with e.g. another
        # with-statement.
        api.disconnect()


class Camera:
    @classmethod
    def from_serial(cls, serial, expected_types=None, open_params={}):
        if expected_types is None:
            expected_types = [VAL_MONOCULAR, VAL_STEREO, VAL_STRUCTURED_LIGHT]
        camera = Camera._get_camera_node(serial)
        camera_type = camera[ITM_TYPE].as_string()
        if camera_type not in expected_types:
            raise CameraTypeError(f"{serial} is of type {camera_type}, "
                f"expected one of {expected_types}")
        if camera_type == VAL_MONOCULAR:
            return MonoCamera(serial, open_params)
        elif camera_type == VAL_STEREO:
            return StereoCamera(serial, open_params)
        elif camera_type == VAL_STRUCTURED_LIGHT:
            return StructuredLightCamera(serial, open_params)

    def __init__(self, serial, open_params):
        self._serial = serial
        self._open_params = open_params
        self._node = Camera._get_camera_node(serial)

    def __getitem__(self, value):
        """
        The ``[]`` access operator.

        Args:
            value (int, str, bool or float): The value to access.

        Returns:
            ``NxLibItem``: The resulting node.
        """
        return self._node[value]

    def get_node(self):
        """
        Get the camera tree node of the stereo camera the context object opens
        and represents.

        Returns:
            `NxLibItem`: The camera node of the stereo camera.
        """
        return self._node

    def capture(self):
        """ Capture the image(s). """
        self._execute(CMD_CAPTURE)

    def rectify(self):
        """
        Rectify the captured images (requires :meth:`capture` to be called
        first). Use this method only if you want to have the rectified raw
        images and no further data.
        """
        self._execute(CMD_RECTIFY_IMAGES)

    def __enter__(self):
        if self._node[ITM_STATUS][ITM_AVAILABLE].as_bool() is False:
            raise CameraOpenError(f"{self._serial} not available")
        self._execute(CMD_OPEN, self._open_params)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._execute(CMD_CLOSE)

    def _execute(self, command_name, params={}):
        cmd = NxLibCommand(command_name, params=params)
        cmd.parameters()[ITM_CAMERAS] = self._serial
        cmd.execute()

    def _check_type(self, expected_type):
        camera_type = self._node[ITM_TYPE].as_string()
        if camera_type != expected_type:
            raise CameraTypeError(f"{self._serial} is of type {camera_type}, "
                                  f"expected {expected_type}")

    @classmethod
    def _get_camera_node(cls, serial):
        camera = NxLibItem()[ITM_CAMERAS][serial]
        if not camera.exists():
            raise CameraNotFoundError(f"No camera found for serial {serial}")

        return camera


class MonoCamera(Camera):
    """
    This class implements the context manager protocol and simplifies the
    handling of a mono camera.

    It provides the camera tree node by calling :meth:`get_node` or lets you
    directly access an ``NxLibItem`` within the camera node by using the ``[]``
    operator.

    Args:
        serial (str): The serial number of the target camera.
        open_params (dict): Optional parameters for opening the target camera.

    Raises:
        CameraTypeError: If the camera with the given serial number is not a
            monocular camera.
        CameraNotFoundError: If no camera was found for the given serial number.
        CameraOpenError: If the camera with the given serial cannot be opened.
    """
    def __init__(self, serial, open_params={}):
        super().__init__(serial, open_params)
        self._check_type(VAL_MONOCULAR)


class StereoCamera(Camera):
    """
    This class implements the context manager protocol and simplifies the
    handling of an Ensenso stereo camera.

    It provides the camera tree node by calling :meth:`get_node` or lets you
    directly access an ``NxLibItem`` within the camera node by using the ``[]``
    operator.

    Args:
        serial (str): The serial number of the target camera.
        open_params (dict): Optional parameters for opening the target camera.

    Raises:
        CameraTypeError: If the camera with the given serial number is not a
            stereo camera.
        CameraNotFoundError: If no camera was found for the given serial number.
        CameraOpenError: If the camera with the given serial cannot be opened.
    """
    def __init__(self, serial, open_params={}):
        super().__init__(serial, open_params)
        self._check_type(VAL_STEREO)

    def compute_disparity_map(self):
        """
        Compute the disparity map (requires :meth:`capture` to be called first).

        Returns:
            ``NxLibItem``: The disparity map node.
        """
        self._execute(CMD_COMPUTE_DISPARITY_MAP)
        return self._node[ITM_IMAGES][ITM_DISPARITY_MAP]

    def compute_point_map(self):
        """
        Compute the point map (requires :meth:`compute_disparity_map` to be
        called first).

        Returns:
            ``NxLibItem``: The point map node.
        """
        self._execute(CMD_COMPUTE_POINT_MAP)
        return self._node[ITM_IMAGES][ITM_POINT_MAP]

    def compute_texture(self):
        """
        Compute the rectified texture image (requires :meth:`rectify` or
        :meth:`compute_disparity_map` to be called first).

        Returns:
            ``NxLibItem``: The node containing the rectified texture image for
                           the camera's left sensor.
        """
        self._execute(CMD_COMPUTE_TEXTURE)
        return self._node[ITM_IMAGES][ITM_RECTIFIED_TEXTURE][ITM_LEFT]

    def get_disparity_map(self):
        """
        The computed disparity map (requires :meth:`compute_disparity_map`).

        Returns:
            `Object`: A byte buffer containing the disparity map.
        """
        return self._node[ITM_IMAGES][ITM_DISPARITY_MAP].get_binary_data()

    def get_point_map(self):
        """
        The computed point map (requires :meth:`compute_point_map`).

        Returns:
            `Object`: A byte buffer containing the point map.
        """
        return self._node[ITM_IMAGES][ITM_POINT_MAP].get_binary_data()

    def get_texture(self):
        """
        The computed rectified texture image (requires :meth:`compute_texture`).

        Returns:
            `Object`: A byte buffer containing the rectified texture image for
                      the camera's left sensor.
        """
        return self._node[ITM_IMAGES][ITM_RECTIFIED_TEXTURE][ITM_LEFT].get_binary_data()


class StructuredLightCamera(StereoCamera):
    """
    This class implements the context manager protocol and simplifies the
    handling of an Ensenso structured light camera and has the same
    functionality as a stereo camera except that it does not have a disparity
    map.

    It provides the camera tree node by calling :meth:`get_node` or lets you
    directly access an ``NxLibItem`` within the camera node by using the ``[]``
    operator.

    Args:
        serial (str): The serial number of the target camera.
        open_params (dict): Optional parameters for opening the target camera.

    Raises:
        CameraTypeError: If the camera with the given serial number is not a
            structured light camera.
        CameraNotFoundError: If no camera was found for the given serial number.
        CameraOpenError: If the camera with the given serial cannot be opened.
        CameraDisparityMapError: If a disparity map is requested.
    """
    def __init__(self, serial, open_params={}):
        Camera.__init__(self, serial, open_params)
        self._check_type(VAL_STRUCTURED_LIGHT)

    def compute_disparity_map(self):
        """
        Does nothing, because a structured light camera does not have a
        disparity map. Existing for compatibility reasons.
        """
        pass

    def compute_point_map(self):
        """
        Compute the point map (requires :meth:`capture` to be called first).

        Returns:
            ``NxLibItem``: The point map node.
        """
        super().compute_disparity_map()
        return super().compute_point_map()

    def get_disparity_map(self):
        raise CameraDisparityMapError("A structured light camera does not have"
                                      "a disparity map.")


class CameraTypeError(Exception):
    """ Raised if camera has the wrong type (Mono/Stereo/StructuredLight). """
    pass


class CameraNotFoundError(Exception):
    """ Raised if no camera is found for a given serial number. """
    pass


class CameraOpenError(Exception):
    """ Raised if a camera cannot be opened. """
    pass


class CameraDisparityMapError(Exception):
    """ Raised if a non-existing disparity map is requested. """
    pass
