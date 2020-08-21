# Maya Animate Bug Tool
This tool will animate the object along the whole curve.

## Settings

* Start frame: frame number to start the animation at
* End frame: frame number to end the animation at
* Number of keys: number of keyframes
* Radius around curve: maximum prependicular distance from the curve
* Looping Animation: if checked, the animation will loop from the end frame back to the start frame

Note: Keys are set at equal increments along the curve so the object moves at constant speed and only translate attributes will be keyed.

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
