from pathlib import Path

import napari
import pandas as pd
from magicgui.widgets import Container, create_widget
from skimage.util import img_as_float

from qi2lab_datastore_viewer.qi2labDataStore import qi2labDataStore


class TileViewer(Container):
    def __init__(self, viewer: 'napari.viewer.Viewer') -> None:
        super().__init__()
        self._viewer = viewer
        self._qi2lab_datastore_folder_picker = create_widget(
            label='Select qi2lab datastore folder',
            annotation=Path,
            widget_type='FileEdit',
            options={'mode': 'd'},
        )
        self._qi2lab_datastore_name_displayer = create_widget(
            # label="Datastore name:", widget_type="Label"
            widget_type='Label'
        )
        self.datastore_state_displayer = create_widget(
            label='Qi2lab Datastore state:', widget_type='Table', value=None
        )
        self._image_layer_combo = create_widget(
            label='Image', annotation='napari.layers.Image'
        )
        self._threshold_slider = create_widget(
            label='Threshold', annotation=float, widget_type='FloatSlider'
        )

        # connect your own callbacks
        self._threshold_slider.changed.connect(self._threshold_im)
        self._qi2lab_datastore_folder_picker.changed.connect(
            self._load_qi2lab_datastore
        )

        # append into/extend the container with your widgets
        self.extend(
            [
                self._qi2lab_datastore_folder_picker,
                self._qi2lab_datastore_name_displayer,
                self.datastore_state_displayer,
                self._image_layer_combo,
                self._threshold_slider,
            ]
        )

    def _threshold_im(self) -> None:
        image_layer = self._image_layer_combo.value
        if image_layer is None:
            return

        image = img_as_float(image_layer.data)
        name = image_layer.name + '_thresholded'
        threshold = self._threshold_slider.value
        thresholded = image > threshold
        # Update existing layer (if present) or add new labels layer
        if name in self._viewer.layers:
            self._viewer.layers[name].data = thresholded
        else:
            self._viewer.add_labels(thresholded, name=name)

    def _load_qi2lab_datastore(self) -> None:
        qi2lab_datastore_path = self._qi2lab_datastore_folder_picker.get_value()
        qi2lab_datastore = qi2labDataStore(qi2lab_datastore_path)
        self._qi2lab_datastore_name_displayer.value = '/'.join(
            qi2lab_datastore_path.parts[-4:-1]
        )
        self._qi2lab_datastore_name_displayer.value = qi2lab_datastore_path.parent.stem
        self.datastore_state_displayer.value = pd.DataFrame.from_dict(
            qi2lab_datastore._datastore_state, orient='index'
        ).rename(columns={0: 'Value'})


def main() -> None:
    # Create a `viewer`
    viewer = napari.Viewer()
    # Instantiate your widget
    my_widg = TileViewer(viewer=viewer)
    # Add widget to `viewer`
    viewer.window.add_dock_widget(my_widg)
    test_datastore_path = Path(
        r'//wsl.localhost/Ubuntu/home/hblanc01/Data/qi2lab_HOB_16bit_MERFISH_crp_6_fov/qi2labdatastore'
    )
    assert test_datastore_path.exists()
    my_widg._qi2lab_datastore_folder_picker.value = test_datastore_path

    napari.run()


if __name__ == '__main__':
    main()
