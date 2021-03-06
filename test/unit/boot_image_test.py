from mock import patch

import mock

from .test_helper import raises

from kiwi.exceptions import KiwiBootImageSetupError
from kiwi.boot.image import BootImage


class TestBootImage(object):
    def setup(self):
        self.xml_state = mock.Mock()
        self.xml_state.build_type.get_initrd_system = mock.Mock()

    @raises(KiwiBootImageSetupError)
    def test_boot_image_not_implemented(self):
        self.xml_state.build_type.get_initrd_system.return_value = 'foo'
        BootImage(self.xml_state, 'target_dir')

    @patch('kiwi.boot.image.BootImageKiwi')
    def test_boot_image_default_system(self, mock_kiwi):
        self.xml_state.build_type.get_initrd_system.return_value = None
        BootImage(self.xml_state, 'target_dir')
        mock_kiwi.assert_called_once_with(
            self.xml_state, 'target_dir', signing_keys=None
        )

    @patch('kiwi.boot.image.BootImageKiwi')
    def test_boot_image_task_kiwi(self, mock_kiwi):
        self.xml_state.build_type.get_initrd_system.return_value = 'kiwi'
        BootImage(self.xml_state, 'target_dir')
        mock_kiwi.assert_called_once_with(
            self.xml_state, 'target_dir', signing_keys=None
        )

    @patch('kiwi.boot.image.BootImageDracut')
    def test_boot_image_task_dracut(self, mock_dracut):
        self.xml_state.build_type.get_initrd_system.return_value = 'dracut'
        BootImage(self.xml_state, 'target_dir', 'root_dir')
        mock_dracut.assert_called_once_with(
            self.xml_state, 'target_dir', 'root_dir'
        )
