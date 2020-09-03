'''
Tool to animate an existing object over a given nurbs curve

To run:
from AnimateBugTool import AnimateBugDialog

try:
    dialog.close()
    dialog.deleteLater()
except:
    pass
    
dialog = AnimateBugDialog()
dialog.show()
'''

from PySide2 import QtCore, QtWidgets, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI
import pymel.core
import random

PI = 3.14159265

def get_maya_window():
    maya_window_ptr = maya.OpenMayaUI.MQtUtil.mainWindow()
    
    # Take this pointer and make it a long and create an instance of the pointer that is a QWidget
    return wrapInstance(long(maya_window_ptr), QtWidgets.QWidget)


class AnimateBugDialog(QtWidgets.QDialog):
    def __init__(self):
        maya_window = get_maya_window()
        super(AnimateBugDialog, self).__init__(maya_window)

        self.setWindowTitle("Animate Bug")
        self.setMinimumHeight(100)
        self.setMinimumWidth(400)
        self.setModal(False)

        self._create_widgets()
        self._create_layouts()
        self._create_connections()


    def _create_widgets(self):
        self._main_text = QtWidgets.QLabel("Select a curve to animate an object along")
        self._main_text.setAlignment(QtCore.Qt.AlignHCenter)

        # Selection widgets
        self._create_curve_widgets()
        self._create_object_widgets()

        # Settings widgets
        self._is_loop_checkbox = QtWidgets.QCheckBox("Loop Animation")

        start_time = pymel.core.playbackOptions(q=True, min=True)
        end_time = pymel.core.playbackOptions(q=True, max=True)

        self._create_frame_widgets(start_time, end_time)
        self._create_num_keys_widgets(start_time, end_time)
        self._create_radius_widgets()
        self._create_axis_widgets()

        self._animate_button = QtWidgets.QPushButton("Animate")

    def _create_curve_widgets(self):
        self._curve_label = QtWidgets.QLabel("Curve")
        self._curve_input = QtWidgets.QLineEdit()
        self._curve_button = QtWidgets.QPushButton("Choose selected")

    def _create_object_widgets(self):
        self._object_label = QtWidgets.QLabel("Object")
        self._object_input = QtWidgets.QLineEdit()
        self._object_button = QtWidgets.QPushButton("Choose selected")

    def _create_frame_widgets(self, start_time, end_time):
        self._start_frame_label = QtWidgets.QLabel("Start Frame")
        self._start_frame_input = QtWidgets.QSpinBox()
        self._start_frame_input.setRange(start_time, end_time)
        self._start_frame_input.setValue(start_time)

        self._end_frame_label = QtWidgets.QLabel("End Frame")
        self._end_frame_input = QtWidgets.QSpinBox()
        self._end_frame_input.setRange(start_time, end_time)
        self._end_frame_input.setValue(end_time)

    def _create_num_keys_widgets(self, start_time, end_time):
        self._number_keys_label = QtWidgets.QLabel("Number of keys")
        self._number_keys_input = QtWidgets.QSpinBox()
        self._number_keys_input.setRange(1, end_time-start_time + 1)
        self._number_keys_input.setValue(self._number_keys_input.maximum()//5)

    def _create_radius_widgets(self):
        self._radius_label = QtWidgets.QLabel("Radius around curve")
        self._radius_input = QtWidgets.QDoubleSpinBox()
        self._radius_input.setSingleStep(0.5)
        self._radius_input.setValue(1.0)
    
    def _create_axis_widgets(self):
        self._axis_label = QtWidgets.QLabel("Object Up Axis")

        self._x_axis_checkbox = QtWidgets.QCheckBox("X")
        self._y_axis_checkbox = QtWidgets.QCheckBox("Y")
        self._z_axis_checkbox = QtWidgets.QCheckBox("Z")
        self._negx_axis_checkbox = QtWidgets.QCheckBox("-X")
        self._negy_axis_checkbox = QtWidgets.QCheckBox("-Y")
        self._negz_axis_checkbox = QtWidgets.QCheckBox("-Z")
        self._y_axis_checkbox.setChecked(True)

        self._axis_group = QtWidgets.QButtonGroup()
        self._axis_group.setExclusive(True)
        self._axis_group.addButton(self._x_axis_checkbox, id=0)
        self._axis_group.addButton(self._y_axis_checkbox, id=1)
        self._axis_group.addButton(self._z_axis_checkbox, id=2)
        self._axis_group.addButton(self._negx_axis_checkbox, id=3)
        self._axis_group.addButton(self._negy_axis_checkbox, id=4)
        self._axis_group.addButton(self._negz_axis_checkbox, id=5)

    def _create_layouts(self):
        # Create main layout
        self._main_layout = QtWidgets.QVBoxLayout(self)

        # Create sub layouts
        self._create_curve_layout()
        self._create_object_layout()

        # Setup settings layout
        self._setup_settings_layout()

        # Setup main layouts
        self._setup_main_layout()
        
    def _create_curve_layout(self):
        self._curve_layout = QtWidgets.QHBoxLayout(self)
        self._curve_layout.addWidget(self._curve_label)
        self._curve_layout.addWidget(self._curve_input)
        self._curve_layout.addWidget(self._curve_button)

    def _create_object_layout(self):
        self._object_layout = QtWidgets.QHBoxLayout(self)
        self._object_layout.addWidget(self._object_label)
        self._object_layout.addWidget(self._object_input)
        self._object_layout.addWidget(self._object_button)

    def _setup_settings_layout(self):
        self._settings_layout = QtWidgets.QVBoxLayout(self)
        self._settings_col_layout = QtWidgets.QHBoxLayout(self)

        # Setup sub settings layouts
        self._create_settings_col1_layout()
        self._create_settings_col2_layout()
        self._create_axis_layout()

        self._settings_col_layout.addLayout(self._settings_c1_layout)
        self._settings_col_layout.addLayout(self._settings_c2_layout)

        # Add components to main settings layout
        self._settings_layout.addLayout(self._settings_col_layout)
        self._settings_layout.addSpacing(5)
        self._settings_layout.addLayout(self._axis_layout)
        self._settings_layout.addSpacing(5)
        self._settings_layout.addWidget(self._is_loop_checkbox)

    def _create_settings_col1_layout(self):
        self._settings_c1_layout = QtWidgets.QVBoxLayout(self)
        self._settings_c1_layout.addWidget(self._start_frame_label)
        self._settings_c1_layout.addWidget(self._start_frame_input)

        self._settings_c1_layout.addWidget(self._number_keys_label)
        self._settings_c1_layout.addWidget(self._number_keys_input)

    def _create_settings_col2_layout(self):
        self._settings_c2_layout = QtWidgets.QVBoxLayout(self)

        self._settings_c2_layout.addWidget(self._end_frame_label)
        self._settings_c2_layout.addWidget(self._end_frame_input)
  
        self._settings_c2_layout.addWidget(self._radius_label)
        self._settings_c2_layout.addWidget(self._radius_input)

    def _create_axis_layout(self):
        self._axis_layout = QtWidgets.QVBoxLayout(self)
        self._checkbox_layout = QtWidgets.QHBoxLayout(self)

        self._checkbox_layout.addWidget(self._x_axis_checkbox)
        self._checkbox_layout.addWidget(self._y_axis_checkbox)
        self._checkbox_layout.addWidget(self._z_axis_checkbox)
        self._checkbox_layout.addWidget(self._negx_axis_checkbox)
        self._checkbox_layout.addWidget(self._negy_axis_checkbox)
        self._checkbox_layout.addWidget(self._negz_axis_checkbox)

        self._axis_layout.addWidget(self._axis_label)
        self._axis_layout.addLayout(self._checkbox_layout)     

    def _setup_main_layout(self):
        self._main_layout.addWidget(self._main_text)
        self._main_layout.addLayout(self._curve_layout)
        self._main_layout.addLayout(self._object_layout)
        self._main_layout.addSpacing(5)
        self._main_layout.addLayout(self._settings_layout)
        self._main_layout.addWidget(self._animate_button)

    def _create_connections(self):
        self._curve_button.clicked.connect(self._get_selected_curve)
        self._object_button.clicked.connect(self._get_selected_object)
        self._animate_button.clicked.connect(self._animate)

    def _get_selected_curve(self):
        selected = pymel.core.ls(sl=True)

        if not selected:
            QtWidgets.QMessageBox.warning(self, "Error", "No curve was selected.")
            return

        self._curve_input.setText(str(selected[0]))

    def _get_selected_object(self):
        selected = pymel.core.ls(sl=True)

        if not selected:
            QtWidgets.QMessageBox.warning(self, "Error", "No object was selected.")
            return

        self._object_input.setText(str(selected[0]))

    def _animate(self):
        # Get frame range
        start_frame = self._start_frame_input.value()
        end_frame = self._end_frame_input.value()

        # Error checking
        if start_frame >= end_frame:
            QtWidgets.QMessageBox.warning(self, "Error", "The end frame must be greater than the start frame.")
            return

        try:
            curve = pymel.core.PyNode(self._curve_input.text())
            # Type check the curve
            if type(curve.listRelatives()[0]) != pymel.core.nt.NurbsCurve:
                QtWidgets.QMessageBox.warning(self, "Error", "The curve must be of type nurbs curve")

        except pymel.core.MayaNodeError:
            QtWidgets.QMessageBox.warning(self, "Error", "The curve selected does not exist")
            return

        try:
            object = pymel.core.PyNode(self._object_input.text())
        except pymel.core.MayaNodeError:
            QtWidgets.QMessageBox.warning(self, "Error", "The object selected does not exist")
            return

        # Get parameters based on settings and curve selected
        num_key_frames = self._number_keys_input.value()
        len_curve = curve.length()
        len_interval = len_curve/num_key_frames
        total_frames = end_frame - start_frame + 1
        frame_interval = total_frames//num_key_frames

        if len_curve == 0:
            QtWidgets.QMessageBox.warning(self, "Error", "The length of this curve could not be computed.")
            return

        # Remove all keys
        pymel.core.cutKey(object)

        # Key the object at increments along the curve
        for i, frame in enumerate(range(start_frame, end_frame, frame_interval)):
            length = len_interval*i
            self._key_object(curve, length, frame, object)

        if self._is_loop_checkbox.isChecked():
            self._handle_looping(start_frame, end_frame, object)
        else:
            # Key the last frame
            self._key_object(curve, len_curve, end_frame, object)

        # Add euler filter to smooth out rotations
        pymel.core.filterCurve(object+'_rotateX', object+'_rotateY', object+'_rotateZ')

        
    def _key_object(self, curve, length, frame, object):
        # Get characteristics of the curve at the specified length
        param = curve.findParamFromLength(length)
        curve_norm = curve.normal(param, space='world').normal()
        point = curve.getPointAtParam(param, space='world')
        curve_tangent = curve.tangent(param, space='world').normal()

        # Choose a random angle (in radians)
        angle = random.random()*2*PI
        rotated_normal = curve_norm.rotateBy(curve_tangent, angle)

        # Choose a random distance from the curve
        distance = random.random()*self._radius_input.value()

        # Get new point
        key_point = point + distance*rotated_normal

        # Set time
        pymel.core.currentTime(frame)

        # Rotate and translate object, then key
        # Create a new orthonormal basis to be set as the rotation axes
        up_axis = [pymel.core.datatypes.Vector(1,0,0),pymel.core.datatypes.Vector(0,1,0),
                    pymel.core.datatypes.Vector(0,0,1),pymel.core.datatypes.Vector(-1,0,0),
                    pymel.core.datatypes.Vector(0,-1,0),pymel.core.datatypes.Vector(0,0,1)][self._axis_group.checkedId()]
        x = -curve_tangent
        z = x.cross(up_axis)

        y = z.cross(x)
        object.setMatrix([  x.x, x.y, x.z, 0,
                            y.x, y.y, y.z, 0,
                            z.x, z.y, z.z, 0,
                            0, 0, 0, 1])

        # Rescale to offset new rotation axes
        object.scale.set([1,1,1])

        object.setTranslation(key_point, space='world')
        pymel.core.setKeyframe(object)

    def _handle_looping(self, start_key, end_key, object):
            pymel.core.copyKey(object, time=start_key)
            pymel.core.pasteKey(object, time=end_key+1)
            
            # Smooth out curves for a smoother transition
            pymel.core.keyTangent(object, inTangentType='linear', time=start_key)
            pymel.core.keyTangent(object, inTangentType='linear', time=end_key+1)



if __name__ == "__main__":
    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass
        
    dialog = AnimateBugDialog()
    dialog.show()
