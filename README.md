# Maya Animate Bug Tool
This tool will animate the object along the whole curve.

## Settings

* Start frame: frame number to start the animation at
* End frame: frame number to end the animation at
* Number of keys: number of keyframes
* Radius around curve: maximum perpendicular distance from the curve
* Object up axis: the direction that the object's up axis will align closest with
* Looping Animation: if checked, the animation will loop from the end frame back to the start frame

Note: Keys are set at equal increments along the curve so the object moves at constant speed.

Assumptions: The object's front and top are facing the -x and y directions and its scale at the start is [1, 1, 1].

## UI

![alt text](./AnimateBugUI.png?raw=true "Animate Bug UI")

## Run the UI

    from AnimateBugTool import AnimateBugDialog
    
    try:
        dialog.close()
        dialog.deleteLater()
    except:
        pass

    dialog = AnimateBugDialog()
    dialog.show()
